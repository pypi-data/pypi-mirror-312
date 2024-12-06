from emplode import emplode
import os

# LLM settings
emplode.llm.api_base = "https://api.cerebras.ai/v1"
emplode.llm.model = "openai/llama3.1-70b"  
emplode.llm.api_key = os.environ.get("CEREBRAS_API_KEY")
emplode.llm.supports_functions = False
emplode.llm.supports_vision = False
emplode.llm.max_tokens = 4096
emplode.llm.context_window = 8192


# Computer settings
emplode.computer.import_computer_api = False

# Misc settings
emplode.offline = False
emplode.auto_run = False

# Custom Instructions
emplode.custom_instructions = f"""

    """
