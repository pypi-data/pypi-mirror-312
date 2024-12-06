import os
import re

from .utils.merge_deltas import merge_deltas
from .utils.parse_partial_json import parse_partial_json

tool_schema = {
    "type": "function",
    "function": {
        "name": "execute",
        "description": "Executes code on the user's machine **in the users local environment** and returns the output",
        "parameters": {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "description": "The programming language (required parameter to the `execute` function)",
                    "enum": [
                    ],
                },
                "code": {
                    "type": "string",
                    "description": "The code to execute (required)",
                },
            },
            "required": ["language", "code"],
        },
    },
}


def process_messages(messages):
    processed_messages = []
    last_tool_id = 0

    i = 0
    while i < len(messages):
        message = messages[i]

        if message.get("function_call"):
            last_tool_id += 1
            tool_id = f"toolu_{last_tool_id}"

            # Convert function_call to tool_calls
            function = message.pop("function_call")
            message["tool_calls"] = [
                {"id": tool_id, "type": "function", "function": function}
            ]
            processed_messages.append(message)

            # Process the next message if it's a function response
            if i + 1 < len(messages) and messages[i + 1].get("role") == "function":
                next_message = messages[i + 1].copy()
                next_message["role"] = "tool"
                next_message["tool_call_id"] = tool_id
                processed_messages.append(next_message)
                i += 1  # Skip the next message as we've already processed it
            else:
                # Add an empty tool response if there isn't one
                processed_messages.append(
                    {"role": "tool", "tool_call_id": tool_id, "content": ""}
                )

        elif message.get("role") == "function":
            # This handles orphaned function responses
            last_tool_id += 1
            tool_id = f"toolu_{last_tool_id}"

            # Add a tool call before this orphaned tool response
            processed_messages.append(
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tool_id,
                            "type": "function",
                            "function": {
                                "name": "execute",
                                "arguments": "# Automated tool call to fetch more output, triggered by the user.",
                            },
                        }
                    ],
                }
            )

            # Process the function response
            message["role"] = "tool"
            message["tool_call_id"] = tool_id
            processed_messages.append(message)

        else:
            # For non-tool-related messages, just add them as is
            processed_messages.append(message)

        i += 1

    return processed_messages


def run_tool_calling_llm(llm, request_params):
    ## Setup

    tool_schema["function"]["parameters"]["properties"]["language"]["enum"] = [
        i.name.lower() for i in llm.emplode.computer.terminal.languages
    ]
    request_params["tools"] = [tool_schema]

    request_params["messages"] = process_messages(request_params["messages"])

    accumulated_deltas = {}
    language = None
    code = ""
    function_call_detected = False
    accumulated_review = ""
    review_category = None
    buffer = ""

    for chunk in llm.completions(**request_params):
        if "choices" not in chunk or len(chunk["choices"]) == 0:
            # This happens sometimes
            continue

        delta = chunk["choices"][0]["delta"]

        # Convert tool call into function call, which we have great parsing logic for below
        if "tool_calls" in delta and delta["tool_calls"]:
            function_call_detected = True

            # import pdb; pdb.set_trace()
            if len(delta["tool_calls"]) > 0 and delta["tool_calls"][0].function:
                delta = {
                    # "id": delta["tool_calls"][0],
                    "function_call": {
                        "name": delta["tool_calls"][0].function.name,
                        "arguments": delta["tool_calls"][0].function.arguments,
                    }
                }

        # Accumulate deltas
        accumulated_deltas = merge_deltas(accumulated_deltas, delta)

        if "content" in delta and delta["content"]:
            if function_call_detected:
                # More content after a code block? This is a code review by a judge layer.

                # print("Code safety review:", delta["content"])

                if review_category == None:
                    accumulated_review += delta["content"]

                    if "<unsafe>" in accumulated_review:
                        review_category = "unsafe"
                    if "<warning>" in accumulated_review:
                        review_category = "warning"
                    if "<safe>" in accumulated_review:
                        review_category = "safe"

                if review_category != None:
                    for tag in [
                        "<safe>",
                        "</safe>",
                        "<warning>",
                        "</warning>",
                        "<unsafe>",
                        "</unsafe>",
                    ]:
                        delta["content"] = delta["content"].replace(tag, "")

                    if re.search("</.*>$", accumulated_review):
                        buffer += delta["content"]
                        continue
                    elif buffer:
                        yield {
                            "type": "review",
                            "format": review_category,
                            "content": buffer + delta["content"],
                        }
                        buffer = ""
                    else:
                        yield {
                            "type": "review",
                            "format": review_category,
                            "content": delta["content"],
                        }
                        buffer = ""

            else:
                yield {"type": "message", "content": delta["content"]}

        if (
            accumulated_deltas.get("function_call")
            and "name" in accumulated_deltas["function_call"]
            and (
                accumulated_deltas["function_call"]["name"] == "python"
                or accumulated_deltas["function_call"]["name"] == "functions"
            )
        ):
            if language is None:
                language = "python"

            # Pull the code string straight out of the "arguments" string
            code_delta = accumulated_deltas["function_call"]["arguments"][len(code) :]
            # Update the code
            code = accumulated_deltas["function_call"]["arguments"]
            # Yield the delta
            if code_delta:
                yield {
                    "type": "code",
                    "format": language,
                    "content": code_delta,
                }

        if (
            accumulated_deltas.get("function_call")
            and "arguments" in accumulated_deltas["function_call"]
            and accumulated_deltas["function_call"]["arguments"]
        ):
            if "arguments" in accumulated_deltas["function_call"]:
                arguments = accumulated_deltas["function_call"]["arguments"]
                arguments = parse_partial_json(arguments)

                if arguments:
                    if (
                        language is None
                        and "language" in arguments
                        and "code"
                        in arguments  # <- This ensures we're *finished* typing language, as opposed to partially done
                        and arguments["language"]
                    ):
                        language = arguments["language"]

                    if language is not None and "code" in arguments:
                        # Calculate the delta (new characters only)
                        code_delta = arguments["code"][len(code) :]
                        # Update the code
                        code = arguments["code"]
                        # Yield the delta
                        if code_delta:
                            yield {
                                "type": "code",
                                "format": language,
                                "content": code_delta,
                            }
                else:
                    if llm.emplode.verbose:
                        print("Arguments not a dict.")

    if os.getenv("EMPLODE_REQUIRE_AUTHENTICATION", "False").lower() == "true":
        print("function_call_detected", function_call_detected)
        print("accumulated_review", accumulated_review)
        if function_call_detected and not accumulated_review:
            print("WTF!!!!!!!!!")
            # import pdb
            # pdb.set_trace()
            raise Exception("Judge layer required but did not run.")
