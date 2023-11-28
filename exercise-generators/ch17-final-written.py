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

output_lyx: str = "ch17-final-written.lyx"

objects_neutral: list[str] = list()
objects_neutral.extend(["ᎩᎦᎨ ᎫᎴ", "ᎩᎦᎨ ᏅᏯ", "ᎩᎦᎨ ᏄᎾ", "ᎩᎦᎨ ᏌᏛᏗ", "ᎩᎦᎨ ᏚᏯ"])
objects_neutral.extend(["ᎤᏁᎦ ᎫᎴ", "ᎤᏁᎦ ᏅᏯ", "ᎤᏁᎦ ᏄᎾ", "ᎤᏁᎦ ᏌᏛᏗ", "ᎤᏁᎦ ᏚᏯ"])
objects_neutral.extend(["ᎤᏬᏗᎨ ᎫᎴ", "ᎤᏬᏗᎨ ᏅᏯ", "ᎤᏬᏗᎨ ᏄᎾ", "ᎤᏬᏗᎨ ᏌᏛᏗ", "ᎤᏬᏗᎨ ᏚᏯ"])

objects_alive: list[str] = list()
objects_alive.extend(["ᎠᎩᎦᎨ ᎠᏫ", "ᎠᎩᎦᎨ ᏥᏍᏚ", "ᎠᎩᎦᎨ ᏌᎶᎵ", "ᎠᎩᎦᎨ ᏩᎭᏯ", "ᎠᎩᎦᎨ ᏲᎾ"])
objects_alive.extend(["ᎤᏁᎦ ᎠᏫ", "ᎤᏁᎦ ᏥᏍᏚ", "ᎤᏁᎦ ᏌᎶᎵ", "ᎤᏁᎦ ᏩᎭᏯ", "ᎤᏁᎦ ᏲᎾ"])
objects_alive.extend(["ᎤᏬᏗᎨ ᎠᏫ", "ᎤᏬᏗᎨ ᏥᏍᏚ", "ᎤᏬᏗᎨ ᏌᎶᎵ", "ᎤᏬᏗᎨ ᏩᎭᏯ", "ᎤᏬᏗᎨ ᏲᎾ"])

subjects: list[str] = list()
subjects.extend(["ᎠᏴᏫᏯᎢ", "ᎠᏣᎳᎩ", "ᎠᎩᎵᏏ", "ᎠᏴᏫ", "ᎠᏴ", "ᏂᎯ"])
subjects.extend(["ᎠᏂᏴᏫᏯᎢ", "ᎠᏂᏣᎳᎩ", "ᎠᏂᎩᎵᏏ", "ᎠᏂᏴᏫ"])

subject_lookup: dict[str, str] = {
        "ᎠᏴᏫᏯᎢ" : "The Native American",
        "ᎠᏣᎳᎩ"  : "The Cherokee person",
        "ᎠᎩᎵᏏ"  : "The English person",
        "ᎠᏲᏁᎦ"  : "The white person",
        "ᎠᏴᏫ"   : "The person",
        "ᎠᏴ"    : "I",
        "ᏂᎯ"    : "You",
        "ᎠᏂᏴᏫᏯᎢ": "The Native Americans",
        "ᎠᏂᏣᎳᎩ" : "The Cherokee people",
        "ᎠᏂᎩᎵᏏ" : "The English people",
        "ᎠᏂᏲᏁᎦ" : "The white people",
        "ᎠᏂᏴᏫ"  : "The people"
}

color_lookup: dict[str, str] = {
        "ᎩᎦᎨ" : "a red",
        "ᎠᎩᎦᎨ": "a red",
        "ᎤᏁᎦ" : "a white",
        "ᎤᏬᏗᎨ": "a brown"
}

object_lookup: dict[str, str] = {
        "ᎠᏫ" : "deer",
        "ᏥᏍᏚ": "rabbit",
        "ᏌᎶᎵ": "squirrel",
        "ᏩᎭᏯ": "wolf",
        "ᏲᎾ" : "bear",
        "ᎫᎴ" : "acorn",
        "ᏅᏯ" : "rock",
        "ᏄᎾ" : "potato",
        "ᏌᏛᏗ": "trap",
        "ᏚᏯ" : "bean"
}

# 1st, 2nd, 3rd-s, 3rd-p
neutral: tuple = ("ᎠᎩᎭ", "ᏣᎭ", "ᎤᎭ", "ᎤᏂᎭ")
living: tuple = ("ᎠᎩᎧᎭ", "ᏣᎧᎭ", "ᎤᏩᎧᎭ", "ᎤᏂᎧᎭ")

verb_lookup: dict[str, str] = {
        "ᎠᎩᎭ" : "have",
        "ᏣᎭ"  : "have",
        "ᎤᎭ"  : "has",
        "ᎤᏂᎭ" : "have",
        "ᎠᎩᎧᎭ": "have",
        "ᏣᎧᎭ" : "have",
        "ᎤᏩᎧᎭ": "has",
        "ᎤᏂᎧᎭ": "have"
}

multicolumn_begin: str = """
\\begin_layout Standard
\\begin_inset ERT
status collapsed

\\begin_layout Plain Layout


\\backslash
begin{multicols}{2}
\\end_layout

\\begin_layout Plain Layout


\\backslash
raggedcolumns
\\end_layout

\\end_inset


\\end_layout
"""

multicolumn_end: str = """
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


def main() -> None:
    wanted_sets: int = 8
    wanted_per_set: int = 5
    random.seed(wanted_sets * wanted_per_set)
    os.chdir(pathlib.Path(__file__).parent)

    jalagi_content: str = ""

    wanted: int = wanted_sets * wanted_per_set
    already: set[tuple[str, str, str]] = set()
    print(f"Wanted: {wanted:,}")
    set_counter: int = 0
    item_counter: int = wanted_per_set
    prev_subject: str = ""
    prev_color: str = ""
    prev_object: str = ""
    while wanted > 0:
        verb_object: str
        subject: str
        verb: str
        verb_set: tuple[str, str, str]
        object_set: list[str] = list()
        if random.choice([True, False]):
            verb_set = living
            object_set = objects_alive
        else:
            verb_set = neutral
            object_set = objects_neutral

        subject = random.choice(subjects)

        if subject == prev_subject:
            continue
        prev_subject = subject

        if subject == "ᎠᏴ":
            verb = verb_set[0]
        elif subject == "ᏂᎯ":
            verb = verb_set[1]
        elif subject.startswith("ᎠᏂ"):
            verb = verb_set[3]
        else:
            verb = verb_set[2]

        verb_object = random.choice(object_set)
        for object_part in prev_object.split():
            if object_part.strip() in verb_object:
                verb_object = ""
                break
        if not verb_object:
            continue
        prev_object = verb_object

        entry: tuple[str, str, str] = (subject, verb_object, verb)
        if entry in already:
            continue
        already.add(entry)

        # SOV vs OVS
        _ = subject
        if _ == "ᎠᏴ" or _ == "ᏂᎯ":
            _ = ""
        else:
            _ = f"Ꮎ {_}"
        sov: str = f"{_} {verb_object} {verb}".strip()
        ovs: str = f"{verb_object} {verb} {_}".strip()
        correct_answer = random.choice([sov, sov, sov, ovs, ovs])
        correct_answer = re.sub("\\s+", " ", correct_answer).strip()

        wanted -= 1
        item_counter += 1
        if item_counter >= wanted_per_set:
            item_counter = 0
            set_counter += 1
            if set_counter > 1:
                jalagi_content += "\n"
                jalagi_content += multicolumn_end
                jalagi_content += "\n"
            jalagi_content += "\\begin_layout Subsubsection*\n"
            jalagi_content += f"Set {set_counter:,}\n"
            jalagi_content += "\\end_layout\n"
            jalagi_content += "\n"
            jalagi_content += multicolumn_begin
            jalagi_content += "\n"

        jalagi_content += "\\begin_layout Enumerate\n"
        jalagi_content += f"{correct_answer}."

        jalagi_content += "\\begin_deeper\n"
        jalagi_content += "\\begin_layout Enumerate\n"

        # attempt auto generate translation answer
        answer_text: str = ""
        answer_text += subject_lookup[subject]
        answer_text += " "
        answer_text += verb_lookup[verb]
        answer_text += " "
        answer_text += color_lookup[verb_object[:verb_object.index(" ")]]
        answer_text += " "
        answer_text += object_lookup[verb_object[verb_object.index(" ") + 1:]]
        answer_text += "."
        jalagi_content += answer_text
        jalagi_content += "\n\n"

        jalagi_content += "\\end_layout\n"
        jalagi_content += "\\end_deeper\n\n"
        jalagi_content += "\end_layout\n"

    jalagi_content += "\n"
    jalagi_content += multicolumn_end
    jalagi_content += "\n"

    with open("written-jalagi-gilisi-template.lyx") as r:
        lyx_content = r.read()
        lyx_content = re.sub("(?s)\\\\begin_layout Standard\\s+jalagi\\s+\\\\end_layout\\s+",
                             jalagi_content.replace("\\", "\\\\"), lyx_content)

    with open(output_lyx, "w") as w:
        w.write(lyx_content)


if __name__ == '__main__':
    main()
