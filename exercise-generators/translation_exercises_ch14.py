#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda activate cherokee-lessons
exec python "$0" "$@"
exit $?
''"""
import os
import pathlib
import random
import re
import textwrap

raw_text: str = """Set 1

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᎬᎿᎨᎢ?

2. ᎦᏙ ᎤᏍᏗ ᎩᎨᎢ?

3. ᎦᏙ ᎤᏍᏗ ᎤᏁᎦ?

4. ᎦᏙ ᎤᏍᏗ ᎤᏬᏗᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᏌᎪᏂᎨᎢ?

\end{multicols}

Set 2

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᎬᏂᎨᎢ?

2. ᎦᏙ ᎤᏍᏗ ᎤᏬᏗᎨᎢ?

3. ᎦᏙ ᎤᏍᏗ ᎩᎦᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᏌᎪᏂᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᎤᏁᎦ?

\end{multicols}

Set 3

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᏓᎭᎵᎨᎢ?

2. ᎦᏙ ᎤᏍᏗ ᎤᏬᏗᎨᎢ?

3. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᏌᎪᏂᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨᎢ?

\end{multicols}

Set 4

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᎢᏤᎢᏳᏍᏗ?

2. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨ ᎤᏍᎪᎸᎢ?

3. ᎦᏙ ᎤᏍᏗ ᏓᎭᎵᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᎢᏤᎢᏳᏍᏗ?

5. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨ ᎤᏍᎪᎸᎢ?

\end{multicols}

Set 5

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨᎢ?

2. ᎦᏙ ᎤᏍᏗ ᎢᏤᎢᏳᏍᏗ?

3. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨ ᎤᏍᎪᎸᎢ?

4. ᎦᏙ ᎤᏍᏗ ᎬᏂᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᎩᎦᎨᎢ?

\end{multicols}

Set 6

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᎤᏁᎦ?

2. ᎦᏙ ᎤᏍᏗ ᎤᏬᏗᎨᎢ?

3. ᎦᏙ ᎤᏍᏗ ᏌᎪᏂᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᏓᎭᎵᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨᎢ?

\end{multicols}

Set 7

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᎢᏤᎢᏳᏍᏗ?

2. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨ ᎤᏍᎪᎸᎢ?

3. ᎦᏙ ᎤᏍᏗ ᎬᎿᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᎩᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᎤᏁᎦ?

\end{multicols}

Set 8

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᎤᏬᏗᎨᎢ?

2. ᎦᏙ ᎤᏍᏗ ᏌᎪᏂᎨᎢ?

3. ᎦᏙ ᎤᏍᏗ ᏓᎭᎵᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨᎢ?

5. ᎦᏙ ᎤᏍᏗ ᎢᏤᎢᏳᏍᏗ?

\end{multicols}

Set 9

\begin{multicols}{2}

1. ᎦᏙ ᎤᏍᏗ ᏓᎶᏂᎨ ᎤᏍᎪᎸᎢ?

2. ᎦᏙ ᎤᏍᏗ ᎬᏂᎨᎢ?

3. ᎦᏙ ᎤᏍᏗ ᎩᎨᎢ?

4. ᎦᏙ ᎤᏍᏗ ᎤᏁᎦ?

5. ᎦᏙ ᎤᏍᏗ ᏓᎭᎵᎨᎢ?

\end{multicols}"""


def main() -> None:
    random.seed(0)
    wanted: int = 10
    already: list[str] = list()
    os.chdir(pathlib.Path(__file__).parent)
    entries: list[str] = list()
    for entry in textwrap.dedent(raw_text).split("\n"):
        entry = entry.strip()
        if not entry:
            continue
        if re.search("^\\d.*", entry):
            entry = re.sub("^\\d+.\\s+", "", entry)
            entries.append(entry)

    print(f"Have {len(entries):,} source entries.")

    block_gilisi: str = textwrap.dedent("""
    \begin_layout Standard
    gilisi 
    \end_layout
    """).strip()

    jalagi_content: str = ""
    gilisi_content: str = ""

    while wanted > 0:
        entry = random.choice(entries)
        if entry in already:
            continue
        color_objects: list[str] = list()
        here_there: list[str] = ["ᎠᎭᏂ", "ᎠᏂ", "ᎤᎿ", "ᎤᎿ"]
        random.shuffle(here_there)
        while len(color_objects) < 4:
            color_object = random.choice(
                    ["square-white", "gihli-white", "wesa-white", "gihli-dead-white", "wesa-dead-white", "nvya-white"])
            if color_object in color_objects:
                continue
            color_objects.append(color_object)

        already.append(entry)
        jalagi_content += "\\begin_layout Enumerate\n"
        jalagi_content += f"{entry}\n"

        jalagi_content += "\\begin_deeper\n"
        jalagi_content += "\\begin_layout Standard\n"
        for color_object in color_objects:
            jalagi_content += f"{here_there.pop()} \n"
            jalagi_content += "\\begin_inset Graphics\n"
            jalagi_content += f" filename ../artwork/with-colors/pngs/{color_object}.png\n"
            jalagi_content += " lyxscale 15"
            jalagi_content += " height 20baselineskip%"
            jalagi_content += "\n\\end_inset\n"
            jalagi_content += f" \n"
        jalagi_content += "\\end_layout\n"
        jalagi_content += "\\end_deeper\n\n"

        jalagi_content += "\end_layout\n"
        wanted -= 1

    jalagi_content += "\n"

    with open("written-jalagi-gilisi-template.lyx") as r:
        lyx_content = r.read()
        lyx_content = re.sub("(?s)\\\\begin_layout Standard\\s+jalagi\\s+\\\\end_layout\\s+",
                             jalagi_content.replace("\\", "\\\\"), lyx_content)

    with open("ch14.lyx", "w") as w:
        w.write(lyx_content)


if __name__ == '__main__':
    main()
