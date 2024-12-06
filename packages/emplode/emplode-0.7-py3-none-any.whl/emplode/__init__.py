import sys

if "--os" in sys.argv:
    from rich import print as rich_print
    from rich.markdown import Markdown
    from rich.rule import Rule

    def print_markdown(message):

        for line in message.split("\n"):
            line = line.strip()
            if line == "":
                print("")
            elif line == "---":
                rich_print(Rule(style="white"))
            else:
                try:
                    rich_print(Markdown(line))
                except UnicodeEncodeError as e:
                    print("Error displaying line:", line)

        if "\n" not in message and message.startswith(">"):
            print("")

    import pkg_resources
    import requests
    from packaging import version

    def check_for_update():
        response = requests.get(f"https://pypi.org/pypi/emplode/json")
        latest_version = response.json()["info"]["version"]

        current_version = pkg_resources.get_distribution("emplode").version

        return version.parse(latest_version) > version.parse(current_version)

    if check_for_update():
        print_markdown(
            "> **A new version of Emplode is available.**\n>Please run: `pip install --upgrade emplode`\n\n---"
        )

    if "--voice" in sys.argv:
        print("Coming soon...")
    from .computer_use.loop import run_async_main

    run_async_main()
    exit()

from .core.async_core import AsyncEmplode
from .core.computer.terminal.base_language import BaseLanguage
from .core.core import Emplode

emplode = Emplode()
computer = emplode.computer