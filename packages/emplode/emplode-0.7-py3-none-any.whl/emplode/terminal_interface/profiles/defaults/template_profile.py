from emplode import emplode

# You can import other libraries too
from datetime import date

# You can set variables
today = date.today()

# LLM Settings
emplode.llm.model = "groq/llama-3.1-70b-versatile"
emplode.llm.context_window = 110000
emplode.llm.max_tokens = 4096
emplode.llm.api_base = "https://api.example.com"
emplode.llm.api_key = "your_api_key_here"
emplode.llm.supports_functions = False
emplode.llm.supports_vision = False

emplode.offline = False
emplode.loop = True
emplode.auto_run = False

emplode.os = False

emplode.computer.import_computer_api = True

emplode.custom_instructions = f"""
    Today's date is {today}.
    """
