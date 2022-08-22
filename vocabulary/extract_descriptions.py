#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda activate cherokee-lessons
exec python "$0" "$@"
exit $?
''"""
import pathlib
import re
from re import Pattern
from typing.io import TextIO
import os


def main() -> None:
    os.chdir(pathlib.Path(__file__).parent)
    input_file = pathlib.Path("../Cherokee Language Lessons-Volume 1.lyx")
    output_file = pathlib.Path("extracted-vocabulary.lyx")
    header_text: str = ""
    body_text: str = ""
    footer_text: str = """
\end_body
\end_document
"""
    entries: dict[str, str] = dict()
    input: TextIO
    with input_file.open("r") as input:
        for line in input:
            header_text += line
            if line.strip() == "\\begin_body":
                break
        lyx_text = input.read()

    pattern: str = str("(?ms)(\\\\begin_layout Description\\s+.*?\\\\end_layout\\s+("
                               "\\\\begin_deeper.*?\\\\end_deeper\\s+)*)")
    for entry in re.findall(pattern, lyx_text):
        entry_text: str = entry[0]
        if not re.search("(?ms)\\\\begin_layout Description\\s+[Ꭰ-Ᏼ]+.*?[\\[]", entry_text):
            continue
        entry_key: str = entry_text[len("\begin_layout Description")+2:]
        entry_key = entry_key[:entry_key.index("[")].strip()
        entry_key = re.sub("\\s+\\\\begin_inset space ~\\s+\\\\end_inset\\s+", " ", entry_key)
        if "\\begin_deeper" in entry_key:
            continue
        entries[entry_key] = entry_text
    with output_file.open("w") as output:
        output.write(header_text)
        keys: list[str] = [*entries]
        keys.sort()
        for key in keys:
            output.write(entries[key])
        output.write(footer_text)


if __name__ == '__main__':
    main()
