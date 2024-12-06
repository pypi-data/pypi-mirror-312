import asyncio
import json
import time
import traceback
from typing import Any, Dict, List

from fastapi import FastAPI, Header, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import Config, Server


class Settings(BaseModel):
    auto_run: bool
    custom_instructions: str
    model: str


class AsyncEmplode:
    def __init__(self, emplode):
        self.emplode = emplode

        self._input_queue = asyncio.Queue()  # Queue that .input will shove things into
        self._output_queue = asyncio.Queue()  # Queue to put output chunks into
        self._last_lmc_start_flag = None  # Unix time of last LMC start flag received
        self._in_keyboard_write_block = (
            False  
        )

        # self.loop = asyncio.get_event_loop()

    async def _add_to_queue(self, queue, item):
        await queue.put(item)

    async def clear_queue(self, queue):
        while not queue.empty():
            await queue.get()

    async def clear_input_queue(self):
        await self.clear_queue(self._input_queue)

    async def clear_output_queue(self):
        await self.clear_queue(self._output_queue)

    async def input(self, chunk):
        """
        Expects a chunk in streaming LMC format.
        """
        if isinstance(chunk, bytes):
            pass
        else:
            try:
                chunk = json.loads(chunk)
            except:
                pass

            if "start" in chunk:
                self._last_lmc_start_flag = time.time()
                self.emplode.computer.terminate()
            elif "end" in chunk:
                asyncio.create_task(self.run())
            else:
                await self._add_to_queue(self._input_queue, chunk)

    def add_to_output_queue_sync(self, chunk):
        asyncio.create_task(self._add_to_queue(self._output_queue, chunk))

    async def run(self):

        input_queue = list(self._input_queue._queue)
        message = [i for i in input_queue if i["type"] == "message"][0]["content"]

        def generate(message):
            last_lmc_start_flag = self._last_lmc_start_flag
            print("passing this in:", message)
            for chunk in self.emplode.chat(message, display=False, stream=True):
                if self._last_lmc_start_flag != last_lmc_start_flag:
                    # self.beeper.stop()
                    break

                # self.add_to_output_queue_sync(chunk) # To send text, not just audio

                content = chunk.get("content")

                # Handle message blocks
                if chunk.get("type") == "message":
                    self.add_to_output_queue_sync(
                        chunk.copy()
                    )  
                    if content:

                        yield content

                # Handle code blocks
                elif chunk.get("type") == "code":
                    pass
            self.add_to_output_queue_sync(
                {"role": "server", "type": "completion", "content": "DONE"}
            )

        # Feed generate to RealtimeTTS
        # self.tts.feed(generate(message))
        for _ in generate(message):
            pass
        # self.tts.play_async(on_audio_chunk=self.on_tts_chunk, muted=True)

    async def output(self):
        return await self._output_queue.get()


def server(emplode, port=8000):  # Default port is 8000 if not specified
    async_emplode = AsyncEmplode(emplode)

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )

    @app.post("/settings")
    async def settings(payload: Dict[str, Any]):
        for key, value in payload.items():
            print("Updating emplode settings with the following:")
            print(key, value)
            if key == "llm" and isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    setattr(async_emplode.emplode, sub_key, sub_value)
            else:
                setattr(async_emplode.emplode, key, value)

        return {"status": "success"}

    @app.websocket("/")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:

            async def receive_input():
                while True:
                    data = await websocket.receive()
                    print(data)
                    if isinstance(data, bytes):
                        await async_emplode.input(data)
                    elif "text" in data:
                        await async_emplode.input(data["text"])
                    elif data == {"type": "websocket.disconnect", "code": 1000}:
                        print("Websocket disconnected with code 1000.")
                        break

            async def send_output():
                while True:
                    output = await async_emplode.output()
                    if isinstance(output, bytes):
                        pass
                    elif isinstance(output, dict):
                        await websocket.send_text(json.dumps(output))

            await asyncio.gather(receive_input(), send_output())
        except Exception as e:
            print(f"WebSocket connection closed with exception: {e}")
            traceback.print_exc()
        finally:
            await websocket.close()

    config = Config(app, host="0.0.0.0", port=port)
    emplode.uvicorn_server = Server(config)
    emplode.uvicorn_server.run()
