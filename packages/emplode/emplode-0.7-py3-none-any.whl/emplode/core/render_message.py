import re


def render_message(emplode, message):

    previous_save_skills_setting = emplode.computer.save_skills
    emplode.computer.save_skills = False

    # Split the message into parts by {{ and }}, including multi-line strings
    parts = re.split(r"({{.*?}})", message, flags=re.DOTALL)

    for i, part in enumerate(parts):
        # If the part is enclosed in {{ and }}
        if part.startswith("{{") and part.endswith("}}"):
            # Run the code inside the brackets
            output = emplode.computer.run(
                "python", part[2:-2].strip(), display=emplode.verbose
            )

            # Extract the output content
            outputs = (
                line["content"]
                for line in output
                if line.get("format") == "output"
                and "IGNORE_ALL_ABOVE_THIS_LINE" not in line["content"]
            )

            # Replace the part with the output
            parts[i] = "\n".join(outputs)

    # Join the parts back into the message
    rendered_message = "".join(parts).strip()

    if (
        emplode.debug == True and False  # DISABLED
    ):  # debug will equal "server" if we're debugging the server specifically
        print("\n\n\nSYSTEM MESSAGE\n\n\n")
        print(rendered_message)
        print("\n\n\n")

    emplode.computer.save_skills = previous_save_skills_setting

    return rendered_message
