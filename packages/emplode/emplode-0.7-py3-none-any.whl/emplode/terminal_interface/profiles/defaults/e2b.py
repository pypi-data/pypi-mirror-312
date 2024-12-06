import e2b

from emplode import emplode


class PythonE2B:
    name = "python"

    system_message = "# Follow this rule: Every Python code block MUST contain at least one print statement."

    def run(self, code):
        stdout, stderr = e2b.run_code("Python3", code)

        yield {
            "type": "console",
            "format": "output",
            "content": stdout
            + stderr, 
        }

    def stop(self):
        pass

    def terminate(self):
        pass

emplode.computer.terminate()

emplode.computer.languages = [PythonE2B]
