import os
import re

def make_poem(match):
    return f"""\\begin{{poetry}}{{{match.group("title").strip()}}}{{{match.group("author").strip()}}}
{format_poem_body(match.group("body"))}
\\end{{poetry}}"""


def format_poem_body(body):
    lines = body.rstrip().split("\n")
    # excludes the last line
    formatted_lines = [
        line.rstrip() + R"\\" + "\n" if line != "" else "\u0026" for line in lines[:-1]
    ]

    return "".join(formatted_lines).replace("\n\u0026", ">\n\n") + lines[-1].rstrip()


def make_prose(match):
    return f"""\\begin{{prose}}{{{match.group("details")}}}{{{match.group("title").strip()}}}{{{match.group("author").strip()}}}
{format_prose_body(match.group("body"))}
\\end{{prose}}"""


def format_prose_body(body):
    return body.strip().replace("\n", R"\\" + "\n")


def to_latex(match):
    if match.group("directive") in ["", "poetry"]:
        return make_poem(match)
    elif match.group("directive") == "prose":
        return make_prose(match)
    elif match.group("directive") == "art":
        return f"""\\clearpage
\\textbf{{\\LARGE Insert art here:  {match.group("details")}}}
\\clearpage"""
    else:
        raise Exception("Invalid directive: " + match.group("directive"))


local_directory = os.path.abspath(os.path.dirname(__file__))

with open(local_directory + "/willow.txt", encoding="utf8") as infile:
    entries = infile.read().split("#")

generated_text = ""
for index, entry in enumerate(entries[1:]):
    match = re.search(
        r"(?P<directive>\S*)[ ]?(?P<details>[^\n#]*)\n(?:(?P<title>[^\n#]*)\n(?P<author>[^\n#]*)\n\n(?P<body>(?:.|\n)*))?",
        entry,
    )
    if not match:
        print(f"Failed on entry {index}: `{entry}`")
        continue

    print(f"Converting item {index}: {match}")
    generated_text += to_latex(match) + "\n\n"

outfile_path = local_directory + "/willow.tex"
if os.path.exists(outfile_path):
    raise Exception("File already exists: aborting")

with open(outfile_path, "w", encoding="utf8") as outfile:
    outfile.write(generated_text)
