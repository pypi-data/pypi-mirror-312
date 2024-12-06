from yaspin import yaspin

spinner = yaspin()
spinner.start()

import os
import platform
import re
import subprocess
import sys
import time

import platformdirs
import pyperclip
import yaml

try:
    from pynput.keyboard import Controller, Key
except ImportError:
    spinner.stop()
    print("Please run `pip install pynput` to use the `wtf` command.")
    exit()

os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
import litellm

SYSTEM_MESSAGE = f"""
You are a fast, efficient terminal assistant. Your task is to:

1. Scan the provided terminal history.
2. Identify the most recent error or issue.
3. Take a deep breath, and thoughtfully, carefully determine the most likely solution or debugging step.
4. Respond with a VERY brief explanation followed by a markdown code block containing a shell command to address the issue.

Rules:
- Provide a single shell command in your code block, using line continuation characters (\\ for Unix-like systems, ^ for Windows) for multiline commands.
- Ensure the entire command is on one logical line, requiring the user to press enter only once to execute.
- If multiple steps are needed, explain the process briefly, then provide only the first command or a combined command using && or ;.
- Keep any explanatory text extremely brief and concise.
- Place explanatory text before the code block.
- NEVER USE COMMENTS IN YOUR CODE.
- Construct the command with proper escaping: e.g. use sed with correctly escaped quotes to ensure the shell interprets the command correctly. This involves:
	•	Using double quotes around the sed expression to handle single quotes within the command.
	•	Combining single and double quotes to properly escape characters within the shell command.
- If previous commands attempted to fix the issue and failed, learn from them by proposing a DIFFERENT command.
- Focus on the most recent error, ignoring earlier unrelated commands. If the user included a message at the end, focus on helping them.
- If you need more information to confidently fix the problem, ask the user to run wtf again in a moment, then write a command like grep to learn more about the problem.
- The error may be as simple as a spelling error, or as complex as requiring tests to be run, or code to be find-and-replaced.
- Prioritize speed and conciseness in your response. Don't use markdown headings. Don't say more than a sentence or two. Be incredibly concise.

User's System: {platform.system()}
CWD: {os.getcwd()}
{"Shell: " + os.environ.get('SHELL') if os.environ.get('SHELL') else ''}

"""

CUSTOM_MESSAGE_SYSTEM_MESSAGE = f"""

You are a fast, efficient AI assistant for terminal and coding tasks. When summoned, you will:

1. Review the provided terminal history (which may or may not be relevant) and final user query.
2. Determine the most appropriate solution or debugging step to resolve the user's final query.
3. Respond with a brief explanation and a single shell command in a markdown code block.

Rules:
- Provide one logical command (use \ or ^ for multiline).
- Keep explanations concise and place them before the code block.
- Use proper command escaping (e.g., sed with correct quotes).
- Avoid comments in the code block.
- If more info is needed, provide a command to gather it (e.g., grep).
- Focus on the user's FINAL query and ADDRESS NOTHING ELSE, using terminal history for context if relevant.
- For multi-step solutions, explain briefly and provide the first or combined command.
- Prioritize addressing the user's specific request (at the END, after "wtf") efficiently.

User's System: {platform.system()}
CWD: {os.getcwd()}
{"Shell: " + os.environ.get('SHELL') if os.environ.get('SHELL') else ''}

"""

LOCAL_SYSTEM_MESSAGE = f"""
You're a fast AI assistant for terminal issues. You must:

1. Scan terminal history
2. Identify latest error
3. Determine best solution
4. Reply with brief explanation + single shell command in markdown

Rules:
- One logical command (use \ or ^ for multiline)
- Explain briefly, then provide command
- No comments in code
- Proper escaping (e.g., sed with correct quotes)
- If unsure, get more info with a command like grep
- Prioritize speed and conciseness

Example response:

We need to fix the file permissions on config.yml.
```bash
chmod 644 config.yml
```

User's System: {platform.system()}
CWD: {os.getcwd()}
{"Shell: " + os.environ.get('SHELL') if os.environ.get('SHELL') else ''}

Now, it's your turn:
"""


def main():

    custom_message = None
    if len(sys.argv) > 1:
        custom_message = "wtf " + " ".join(sys.argv[1:])

    keyboard = Controller()
    history = None

    if True:
        clipboard = pyperclip.paste()

        shortcut_key = Key.cmd if platform.system() == "Darwin" else Key.ctrl
        with keyboard.pressed(shortcut_key):
            keyboard.press("a")
            keyboard.release("a")

        with keyboard.pressed(shortcut_key):
            keyboard.press("c")
            keyboard.release("c")

        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)

        time.sleep(0.1)

        history = pyperclip.paste()

        pyperclip.copy(clipboard)

    if not history:
        try:
            import pytesseract
            from PIL import ImageGrab

            platform_name = platform.system()
            if platform_name == "Windows":
                import win32gui

                window = win32gui.GetForegroundWindow()
                left, top, right, bottom = win32gui.GetWindowRect(window)
            elif platform_name == "Darwin":
                from Quartz import (
                    CGWindowListCopyWindowInfo,
                    kCGNullWindowID,
                    kCGWindowListOptionOnScreenOnly,
                )

                window_info = CGWindowListCopyWindowInfo(
                    kCGWindowListOptionOnScreenOnly, kCGNullWindowID
                )
                for window in window_info:
                    if window["kCGWindowLayer"] == 0:
                        window_geometry = window["kCGWindowBounds"]
                        left = window_geometry["X"]
                        top = window_geometry["Y"]
                        right = int(left + window_geometry["Width"])
                        bottom = int(top + window_geometry["Height"])
                        break
            else: 
                root = subprocess.Popen(
                    ["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE
                )
                stdout, stderr = root.communicate()
                m = re.search(b"^_NET_ACTIVE_WINDOW.* ([\\w]+)$", stdout)
                if m is not None:
                    window_id = m.group(1)
                    window = subprocess.Popen(
                        ["xwininfo", "-id", window_id], stdout=subprocess.PIPE
                    )
                    stdout, stderr = window.communicate()
                    match = re.search(
                        rb"Absolute upper-left X:\s*(\d+).*Absolute upper-left Y:\s*(\d+).*Width:\s*(\d+).*Height:\s*(\d+)",
                        stdout,
                        re.DOTALL,
                    )
                    if match is not None:
                        left, top, width, height = map(int, match.groups())
                        right = left + width
                        bottom = top + height

            screenshot = ImageGrab.grab(
                bbox=(int(left), int(top), int(right), int(bottom))
            )

            text = pytesseract.image_to_string(screenshot)

            history = text

            if "wtf" in history:
                last_wtf_index = history.rindex("wtf")
                history = history[:last_wtf_index]
        except ImportError:
            spinner.stop()
            print(
                "To use OCR to capture terminal output (recommended) run `pip install pytesseract` or `pip3 install pytesseract`."
            )
            spinner.start()

    if not history:
        try:
            shell = os.environ.get("SHELL", "/bin/bash")
            command = [shell, "-ic", "fc -ln -10"]  

            output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode(
                "utf-8"
            )

            lines = output.strip().split("\n")

            history = [
                line
                for line in lines
                if not line.startswith("...")
                and "saving" not in line
                and "Saving session..." not in line
            ]
            history = [l.strip() for l in history if l.strip()][-10:]

            last_command = history[-1]
            spinner.start()
            print(
                f"\nRunning the last command again to collect its output: {last_command}\n"
            )
            spinner.stop()
            try:
                last_command_output = subprocess.check_output(
                    last_command, shell=True, stderr=subprocess.STDOUT
                ).decode("utf-8")
            except subprocess.CalledProcessError as e:
                last_command_output = e.output.decode("utf-8")
            except Exception as e:
                last_command_output = str(e)

            history = "The user tried to run the following commands:\n" + "\n".join(
                history
            )
            history += f"\nThe last command, {last_command}, resulted in this output:\n{last_command_output}"

        except Exception as e:
            raise
            print(
                "Failed to retrieve and run the last command from terminal history. Exiting."
            )
            return

    history = history[-9000:].strip()
    spinner_commands = [
        "⠴",
        "⠦",
        "⠇",
        "⠉",
        "⠙",
        "⠸",
        "⠼",
        "⠤",
        "⠴",
        "⠂",
        "⠄",
        "⠈",
        "⠐",
        "⠠",
    ]
    for command in spinner_commands:
        if history.endswith(command):
            history = history[: -len(command)].strip()
            break

    if "wtf" in history:
        last_wtf_index = history.rindex("wtf")
        history = history[:last_wtf_index]

    pattern = r'File "([^"]+)", line (\d+)'
    matches = re.findall(pattern, history)

    matches = matches[-1:] 

    def get_lines_from_file(filename, line_number):
        lines = []
        try:
            with open(filename, "r") as file:
                all_lines = file.readlines()
                start_line = max(0, line_number - 3)  
                end_line = min(len(all_lines), line_number + 2) 
                for i in range(start_line, end_line + 1):
                    lines.append(f"Line {i+1}: " + all_lines[i].rstrip())
        except Exception as e:
            lines.append(f"Error reading file: {e}")
        return lines

    result = []
    for match in matches:
        filename, line_number = match
        line_number = int(line_number)
        lines = get_lines_from_file(filename, line_number)
        result.append({"filename": filename, "text": "\n".join(lines)})

    if result != []:
        history = "Terminal: " + history

    for entry in result:
        history = f"""File: {entry["filename"]}\n{entry["text"]}\n\n""" + history

    default_profile_path = os.path.join(
        platformdirs.user_config_dir("emplode"), "profiles", "default.yaml"
    )

    try:
        with open(default_profile_path, "r") as file:
            profile = yaml.safe_load(file)
            wtf_model = profile.get("wtf", {}).get("model")
            if wtf_model:
                model = wtf_model
            else:
                model = profile.get("llm", {}).get("model", "gpt-4o-mini")
    except:
        model = "gpt-4o-mini"

    if "ollama" in model or "llama" in model:
        system_message = LOCAL_SYSTEM_MESSAGE
    else:
        system_message = SYSTEM_MESSAGE

    if custom_message:
        system_message = CUSTOM_MESSAGE_SYSTEM_MESSAGE
        user_message = (
            "Answer THIS question by telling me what code to run:"
            + custom_message
            + "\nMy terminal history, which may or may not be relevant, is this:\n---\n"
            + history
            + "\n---\nPlease now answer THIS question by telling me what code to run: "
            + custom_message
        )
    else:
        user_message = (
            history.strip()
            + "\n\nPlease help me resolve the final error above by telling me what code to run in a markdown code block."
        )

    messages = [
        {"role": "system", "content": system_message.strip()},
        {"role": "user", "content": user_message.strip()},
    ]

    in_code = False
    backtick_count = 0
    language_buffer = ""
    started = False

    for chunk in litellm.completion(
        model=model, messages=messages, temperature=0, stream=True
    ):
        if not started:
            started = True
            spinner.stop()
            print("")

        content = chunk.choices[0].delta.content
        if content:
            for char in content:
                if char == "`":
                    backtick_count += 1
                    if backtick_count == 3:
                        in_code = not in_code
                        backtick_count = 0
                        language_buffer = ""
                        if not in_code:  
                            time.sleep(0.1)
                            print("\n")
                            return  
                        else: 
                            print("Press `enter` to run: ", end="", flush=True)
                elif in_code:
                    if language_buffer is not None:
                        if char.isalnum():
                            language_buffer += char
                        elif char.isspace():
                            language_buffer = None
                    elif char not in ["\n", "\\"]:
                        keyboard.type(char)
                else:
                    if backtick_count:
                        print("`" * backtick_count, end="", flush=True)
                        backtick_count = 0

                    print(char, end="", flush=True)

                    backtick_count = 0

if __name__ == "__main__":
    main()
