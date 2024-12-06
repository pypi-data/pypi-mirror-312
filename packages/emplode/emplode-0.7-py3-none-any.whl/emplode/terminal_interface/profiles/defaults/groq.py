from emplode import emplode

emplode.llm.model = "groq/llama-3.1-70b-versatile"

emplode.computer.import_computer_api = True

emplode.llm.supports_functions = False
emplode.llm.supports_vision = False
emplode.llm.context_window = 110000
emplode.llm.max_tokens = 4096
