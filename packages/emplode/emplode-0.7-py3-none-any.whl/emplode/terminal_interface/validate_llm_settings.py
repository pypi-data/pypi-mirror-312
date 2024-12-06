import os
import subprocess
import time

os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
import litellm
from prompt_toolkit import prompt

from emplode.terminal_interface.contributing_conversations import (
    contribute_conversation_launch_logic,
)


def validate_llm_settings(emplode):
    while True:
        if emplode.offline:
            break

        else:
            if emplode.llm.model in [
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
            ]:
                if (
                    not os.environ.get("OPENAI_API_KEY")
                    and not emplode.llm.api_key
                    and not emplode.llm.api_base
                ):
                    display_welcome_message_once(emplode)

                    emplode.display_message(
                        """---
                    > OpenAI API key not found

                    To use `gpt-4o` (recommended) please provide an OpenAI API key.

                    To use another language model, run `emplode --local`).
                    
                    ---
                    """
                    )

                    response = prompt("OpenAI API key: ", is_password=True)

                    if response == "emplode --local":
                        print(
                            "\nType `emplode --local` again to use a local language model.\n"
                        )
                        exit()

                    emplode.display_message(
                        """

                    **Tip:** To save this key for later, run one of the following and then restart your terminal. 
                    MacOS: `echo 'export OPENAI_API_KEY=your_api_key' >> ~/.zshrc`
                    Linux: `echo 'export OPENAI_API_KEY=your_api_key' >> ~/.bashrc`
                    Windows: `setx OPENAI_API_KEY your_api_key`
                    
                    ---"""
                    )

                    emplode.llm.api_key = response
                    time.sleep(2)
                    break
            break

    if (
        not emplode.auto_run
        and not emplode.offline
        and not (len(emplode.messages) == 1)
    ):
        emplode.display_message(f"> Model set to `{emplode.llm.model}`")
    if len(emplode.messages) == 1:
        pass

    if emplode.llm.model == "e":
        emplode.display_message(
            "***Note:*** *Conversations with this model is not encrypted.*\n"
        )
    if "ollama" in emplode.llm.model:
        emplode.llm.load()
    return


def display_welcome_message_once(emplode):
    if not hasattr(display_welcome_message_once, "_displayed"):
        emplode.display_message(
            """
        Welcome to **Emplode**.
        """
        )
        time.sleep(1)

        display_welcome_message_once._displayed = True
