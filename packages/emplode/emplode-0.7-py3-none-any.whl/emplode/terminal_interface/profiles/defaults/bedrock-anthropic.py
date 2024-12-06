from emplode import emplode

emplode.llm.model = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"

emplode.computer.import_computer_api = True

emplode.llm.supports_functions = False
emplode.llm.supports_vision = False
emplode.llm.context_window = 10000
emplode.llm.max_tokens = 4096
