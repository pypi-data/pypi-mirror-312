import os


DIR_README = "readme_examples"


def _get_lines(path_to_file, filename, filetype=".py"):
    with open(f"{path_to_file}{filename}{filetype}", encoding="utf-8") as file:
        lines = []
        for line in file:
            rstrip_line = line.rstrip()
            if len(rstrip_line) > 4:
                if rstrip_line[0:3] != "pip":
                    lines.append(rstrip_line)
            else:
                lines.append(rstrip_line)
    return lines


def _get_example_readme(lines):
    example = []
    in_example = False
    for line in lines:
        line = line.lstrip()
        if len(line) > 2:
            if line[0:3] == "```":
                if in_example is False:
                    if "not run" in line:
                        in_example = False
                    else:
                        in_example = True
                else:
                    in_example = False
            elif in_example is True:
                example.append(line)
    example.pop()  # The last line is pip install pyPLNmodels which is not python code.
    return [example]


def _write_file(examples, filename, string_definer, dirname):
    for i, example in enumerate(examples):
        nb_example = str(i + 1)
        example_filename = f"{dirname}/test_{filename}_{string_definer}_{nb_example}.py"
        try:
            os.remove(example_filename)
        except FileNotFoundError:
            pass
        with open(example_filename, "a", encoding="utf-8") as the_file:
            for line in example:
                the_file.write(line + "\n")


def _create_readm_example_file():
    lines = _get_lines("../", "README", filetype=".md")
    examples = _get_example_readme(lines)
    _write_file(examples, "readme", "example", dirname=DIR_README)


print("Building readme examples...")

os.makedirs(DIR_README, exist_ok=True)

_create_readm_example_file()
print("Done!")
