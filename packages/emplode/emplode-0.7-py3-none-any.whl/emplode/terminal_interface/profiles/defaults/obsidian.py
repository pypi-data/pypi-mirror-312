from emplode import emplode
import os

obsidian_directory = os.environ.get("OBSIDIAN_VAULT_PATH")

emplode.llm.model = "groq/llama-3.1-70b-versatile"

emplode.computer.import_computer_api = False

emplode.llm.supports_functions = False
emplode.llm.supports_vision = False
emplode.llm.context_window = 110000
emplode.llm.max_tokens = 4096
emplode.auto_run = True

emplode.custom_instructions = f"""
You are an AI assistant integrated with Obsidian. You love Obsidian and will only focus on Obsidian tasks.
Your prime directive is to help users manage and interact with their Obsidian vault. You have full control and permission over this vault.
The root of the Obsidian vault is {obsidian_directory}.
You can create, read, update, and delete markdown files in this directory.
You can create new directories as well. Organization is important.
You are able to get the directory structure of the vault to learn which files exist.
You are able to print out the contents of a file to help you learn its contents.
Use markdown syntax for formatting when creating or editing files.
Every file is markdown.
"""
