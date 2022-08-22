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
    appendix_start: str = """
\\begin_layout Chapter
\\start_of_appendix
ᏗᏕᏠᏆᏍᏗ
\\begin_inset Argument 1
status collapsed
\\begin_layout Plain Layout
Dictionary
\\end_layout
\\end_inset
\\end_layout
"""
    header_text: str = ""
    box_start: str = """
\\begin_layout Standard
\\begin_inset Box Frameless
position "t"
hor_pos "c"
has_inner_box 1
inner_pos "t"
use_parbox 0
use_makebox 0
width "100col%"
special "none"
height "1in"
height_special "totalheight"
thickness "0.4pt"
separation "3pt"
shadowsize "4pt"
framecolor "black"
backgroundcolor "none"
status open
"""
    box_end: str = """
\\end_inset
\\end_layout
"""
    footer_text: str = """
\\end_body
\\end_document
"""
    begin_multicols: str = """
\\begin_layout Standard
\\begin_inset ERT
status collapsed
\\begin_layout Plain Layout
\\backslash
begin{multicols}{2}
\\backslash
raggedcolumns
\\end_layout
\\end_inset
\\end_layout
"""
    between_box_skip: str = """
\\begin_layout Standard
\\begin_inset VSpace bigskip
\\end_inset
\\end_layout
"""
    end_multicols: str = """
\\begin_layout Standard
\\begin_inset ERT
status collapsed

\\begin_layout Plain Layout


\\backslash
end{multicols}
\\end_layout

\\end_inset


\\end_layout
"""
    entries: dict[str, str] = dict()
    input: TextIO
    with input_file.open("r") as input:
        for line in input:
            header_text += line
            if line.strip() == "\\begin_body":
                break
        lyx_text = input.read()
    lyx_text = lyx_text[:lyx_text.index("\\start_of_appendix")]

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
    max_lines: int = 40
    with output_file.open("w") as output:
        output.write(header_text)
        output.write(appendix_start)
        keys: list[str] = [*entries]
        keys.sort()
        section_name: str = ""
        counter: int = 0
        for key in keys:
            entry = entries[key]
            if not section_name or key[0] != section_name[0] or counter > max_lines:
                if section_name:
                    output.write(end_multicols)
                    output.write(box_end)
                    output.write(between_box_skip)
                if counter > max_lines and section_name == key[0]:
                    section_name = key[0:2]
                else:
                    section_name = key[0]
                output.write(box_start)
                output.write(f"\n\\begin_layout Section\n{section_name}\n\\end_layout\n\n")
                output.write(begin_multicols)
                counter = 0
            output.write(entry)
            counter += entry.count("\\begin_layout Description")
        output.write(end_multicols)
        output.write(box_end)
        output.write(footer_text)


if __name__ == '__main__':
    main()
