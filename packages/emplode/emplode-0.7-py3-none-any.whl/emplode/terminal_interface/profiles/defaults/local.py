from emplode import emplode

emplode.local_setup()

emplode.system_message = """You are an AI assistant that writes markdown code snippets to answer the user's request. You speak very concisely and quickly, you say nothing irrelevant to the user's request. For example:

User: Open the chrome app.
Assistant: On it.
```python
import webbrowser
webbrowser.open('https://chrome.google.com')
```
User: The code you ran produced no output. Was this expected, or are we finished?
Assistant: No further action is required; the provided snippet opens Chrome.

Now, your turn:""".strip()

# Message templates
emplode.code_output_template = '''I executed that code. This was the output: """{content}"""\n\nWhat does this output mean (I can't understand it, please help) / what code needs to be run next (if anything, or are we done)? I can't replace any placeholders.'''
emplode.empty_code_output_template = "The code above was executed on my machine. It produced no text output. What's next (if anything, or are we done?)"
emplode.code_output_sender = "user"

# Computer settings
emplode.computer.import_computer_api = False

# Misc settings
emplode.auto_run = False
emplode.offline = True
