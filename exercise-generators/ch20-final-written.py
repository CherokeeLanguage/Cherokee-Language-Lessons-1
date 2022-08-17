#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda activate cherokee-lessons
exec python "$0" "$@"
exit $?
''"""
import dataclasses
import os
import pathlib
import random
import re

from dataclasses import field

output_lyx: pathlib.Path | None = None
prev_already: pathlib.Path = pathlib.Path("ch19-final-written-already.txt")

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


@dataclasses.dataclass
class VerbObject(object):
    form: str = ""
    subj: str = ""
    obj: str = ""
    classes: set[str] = field(default_factory=set)
    templates: list[str] = field(default_factory=list)


@dataclasses.dataclass
class SubjectObject:
    form: str = ""
    subj: str = ""
    classes: set[str] = field(default_factory=set)
    is_person: bool = False


@dataclasses.dataclass
class Adjective:
    form: str = ""
    subj: str = ""
    classes: set[str] = field(default_factory=set)
    is_person: bool = False


def verb_objects() -> list[VerbObject]:
    vo_list: list[VerbObject] = list()
    vo_list.append(VerbObject("ᎠᎪᏩᏘᎭ", "3s", "3s", set()))
    vo_list.append(VerbObject("ᎠᏂᎪᏩᏘᎭ", "3s", "3s", set()))
    vo_list.append(VerbObject("ᏓᎪᏩᏘᎭ", "3s", "3p", set()))
    vo_list.append(VerbObject("ᏓᏂᎪᏩᏘᎭ", "3p", "3p", set()))
    vo_list.append(VerbObject("ᏥᎪᏩᏘᎭ", "1s", "3s", {"a"}))
    vo_list.append(VerbObject("ᏥᎪᏩᏘᎭ", "1s", "3s", {"i"}))
    vo_list.append(VerbObject("ᎦᏥᎪᏩᏘᎭ", "1s", "3p", {"a"}))
    vo_list.append(VerbObject("ᏕᏥᎪᏩᏘᎭ", "1s", "3p", {"i"}))
    vo_list.append(VerbObject("ᎯᎪᏩᏘᎭ", "2s", "3s", {"a"}))
    vo_list.append(VerbObject("ᎯᎪᏩᏘᎭ", "2s", "3s", {"i"}))
    vo_list.append(VerbObject("ᎦᎯᎪᏩᏘᎭ", "2s", "3p", {"a"}))
    vo_list.append(VerbObject("ᏕᎯᎪᏩᏘᎭ", "2s", "3p", {"i"}))

    vo_list.append(VerbObject("ᎤᎭ", "3s", "3s", {"i", "neutral"}))
    vo_list.append(VerbObject("ᎤᏂᎭ", "3p", "3s", {"i", "neutral"}))
    vo_list.append(VerbObject("ᎠᎩᎭ", "1s", "3s", {"i", "neutral"}))
    vo_list.append(VerbObject("ᏣᎭ", "2s", "3s", {"i", "neutral"}))

    vo_list.append(VerbObject("ᎤᏩᎧᎭ", "3s", "3s", {"a"}))
    vo_list.append(VerbObject("ᎤᏂᎧᎭ", "3p", "3s", {"a"}))
    vo_list.append(VerbObject("ᎠᎩᎧᎭ", "1s", "3s", {"a"}))
    vo_list.append(VerbObject("ᏣᎧᎭ", "2s", "3s", {"a"}))

    vo_list.append(VerbObject("ᎠᎩᎪᏩᏘᎭ", "3s", "1s", {"a"}))
    vo_list.append(VerbObject("ᏣᎪᏩᏘᎭ", "3s", "2s", {"a"}))

    vo_list.append(VerbObject("ᎬᎩᎪᏩᏘᎭ", "3p", "1s", {"a"}))
    vo_list.append(VerbObject("ᎨᏣᎪᏩᏘᎭ", "3p", "2s", {"a"}))

    vo_list.append(VerbObject("ᏚᎭ", "3s", "3p", {"i", "neutral"}))
    vo_list.append(VerbObject("ᏚᏂᎭ", "3p", "3p", {"i", "neutral"}))
    vo_list.append(VerbObject("ᏓᎩᎭ", "1s", "3p", {"i", "neutral"}))
    vo_list.append(VerbObject("ᏕᏣᎭ", "2s", "3p", {"i", "neutral"}))

    vo_list.append(VerbObject("ᏚᏩᎧᎭ", "3s", "3p", {"a"}))
    vo_list.append(VerbObject("ᏚᏂᎧᎭ", "3p", "3p", {"a"}))
    vo_list.append(VerbObject("ᏓᎩᎧᎭ", "1s", "3p", {"a"}))
    vo_list.append(VerbObject("ᏕᏣᎧᎭ", "2s", "3p", {"a"}))

    return vo_list


def adjective_allowed(subject: str) -> bool:
    if subject.startswith("ᎠᎢ"):
        return True
    if subject.startswith("ᎥᏍᎩ"):
        return True
    if subject.startswith("Ꭰ"):
        return True
    return False


def subject_objects() -> list[SubjectObject]:
    so_list: list[SubjectObject] = list()
    so_list.append(SubjectObject("ᎠᎨᏯ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏂᎨᏯ", "3p", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏍᎦᏯ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏂᏍᎦᏯ", "3p", {"a"}, True))

    so_list.append(SubjectObject("ᎩᏟ", "3s", {"a"}))
    so_list.append(SubjectObject("ᎩᏟ", "3p", {"a"}))
    so_list.append(SubjectObject("ᏅᏯ", "3s", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏅᏯ", "3p", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏪᏌ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏪᏌ", "3p", {"a"}))

    so_list.append(SubjectObject("ᎥᏍᎩᎾ", "3s", {"a"}))
    so_list.append(SubjectObject("ᎥᏍᎩᎾ", "3s", {"i", "neutral"}))
    so_list.append(SubjectObject("ᎥᏍᎩᎾ", "3p", {"a", "neutral"}))
    so_list.append(SubjectObject("ᎥᏍᎩᎾ", "3p", {"i"}))

    # so_list.append(SubjectObject("ᎯᎠ", "3s", {"a"}))
    # so_list.append(SubjectObject("ᎯᎠ", "3s", {"i", "neutral"}))
    # so_list.append(SubjectObject("ᎯᎠ", "3p", {"a"}))
    # so_list.append(SubjectObject("ᎯᎠ", "3p", {"i", "neutral"}))

    so_list.append(SubjectObject("ᎠᎭᏫ", "3s", {"a"}))
    so_list.append(SubjectObject("ᎠᎭᏫ", "3p", {"a"}))
    so_list.append(SubjectObject("ᎪᏪᎵ", "3s", {"i"}))
    so_list.append(SubjectObject("ᏗᎪᏪᎵ", "3p", {"i"}))
    so_list.append(SubjectObject("ᎫᎴ", "3s", {"i", "neutral"}))
    so_list.append(SubjectObject("ᎫᎴ", "3p", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏙᏯ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏙᏯ", "3p", {"a"}))
    so_list.append(SubjectObject("ᏚᏯ", "3s", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏚᏯ", "3p", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏥᏍᏚ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏥᏍᏚ", "3p", {"a"}))
    so_list.append(SubjectObject("ᏩᎭᏯ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏩᎭᏯ", "3p", {"a"}))

    so_list.append(SubjectObject("ᎠᎨᏳᏣ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏂᎨᏳᏣ", "3p", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏧᏣ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏂᏧᏣ", "3p", {"a"}, True))

    so_list.append(SubjectObject("ᏌᎶᎵ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏌᎶᎵ", "3p", {"a"}))
    so_list.append(SubjectObject("ᏌᏛᏗ", "3s", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏗᏌᏛᏗ", "3p", {"i", "neutral"}))
    so_list.append(SubjectObject("ᏐᏈᎵ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏐᏈᎵ", "3p", {"a"}))
    so_list.append(SubjectObject("ᏡᎬᎢ", "3s", {"i", "rod"}))
    so_list.append(SubjectObject("ᏕᏡᎬᎢ", "3p", {"i", "rod"}))
    so_list.append(SubjectObject("ᏲᎾ", "3s", {"a"}))
    so_list.append(SubjectObject("ᏲᎾ", "3p", {"a"}))

    so_list.append(SubjectObject("ᏴᏫ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏴᏫ", "3p", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏴᏫ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎠᏂᏴᏫ", "3p", {"a"}, True))
    so_list.append(SubjectObject("ᎠᎵᏌᏇᏘ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎡᏂᏙᏂ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎵᏂᏓ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎹᎦᎵ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎹᎦᏰᏘ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᎺᎵ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏆᏆᎠ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏑᏌᏃ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏙᎹᏏ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏕᏫᏗ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏣᎵ", "3s", {"a"}, True))
    so_list.append(SubjectObject("ᏣᏂ", "3s", {"a"}, True))

    so_list.append(SubjectObject("ᎪᎱᏍᏗ", "3s", {"i", "neutral"}))
    so_list.append(SubjectObject("ᎪᎱᏍᏗ", "3p", {"i", "neutral"}))

    return so_list


def adjectives_list() -> list[Adjective]:
    a_list: list[Adjective] = list()

    a_list.append(Adjective("ᎤᏁᎦ", "3s", {"i"}))
    a_list.append(Adjective("ᎤᏁᎦ", "3s", {"a"}))
    a_list.append(Adjective("ᎤᏬᏗᎨ", "3s", {"i"}))
    a_list.append(Adjective("ᎤᏬᏗᎨ", "3s", {"a"}))

    a_list.append(Adjective("ᎩᎦᎨ", "3s", {"i"}))
    a_list.append(Adjective("ᎬᎿᎨ", "3s", {"i"}))
    a_list.append(Adjective("ᏌᎪᏂᎨ", "3s", {"i"}))
    a_list.append(Adjective("ᏓᎭᎵᎨ", "3s", {"i"}))
    a_list.append(Adjective("ᏓᎶᏂᎨ", "3s", {"i"}))

    a_list.append(Adjective("ᎠᎩᎦᎨ", "3s", {"a"}))
    a_list.append(Adjective("ᎠᎬᎿᎨ", "3s", {"a"}))
    a_list.append(Adjective("ᎠᏌᎪᏂᎨ", "3s", {"a"}))
    a_list.append(Adjective("ᎠᏓᎭᎵᎨ", "3s", {"a"}))
    a_list.append(Adjective("ᎠᏓᎶᏂᎨ", "3s", {"a"}))

    a_list.append(Adjective("ᎩᎦᎨ ᎤᏍᎪᎸ", "3s", {"i"}))
    a_list.append(Adjective("ᎠᎩᎦᎨ ᎤᏍᎪᎸ", "3s", {"a"}))
    a_list.append(Adjective("ᎬᎿᎨ ᎤᏍᎪᎸ", "3s", {"i"}))
    a_list.append(Adjective("ᎠᎬᎿᎨ ᎤᏍᎪᎸ", "3s", {"a"}))
    a_list.append(Adjective("ᏌᎪᏂᎨ ᎤᏍᎪᎸ", "3s", {"i"}))
    a_list.append(Adjective("ᎠᏌᎪᏂᎨ ᎤᏍᎪᎸ", "3s", {"a"}))
    a_list.append(Adjective("ᏓᎶᏂᎨ ᎤᏍᎪᎸ", "3s", {"i"}))
    a_list.append(Adjective("ᎠᏓᎶᏂᎨ ᎤᏍᎪᎸ", "3s", {"a"}))

    a_list.append(Adjective("ᏗᎩᎦᎨ ᎤᏂᏍᎪᎸ", "3p", {"i"}))
    a_list.append(Adjective("ᎠᏂᎩᎦᎨ ᎤᏂᏍᎪᎸ", "3p", {"a"}))
    a_list.append(Adjective("ᏗᎬᎿᎨ ᎤᏂᏍᎪᎸ", "3p", {"i"}))
    a_list.append(Adjective("ᎠᏂᎬᎿᎨ ᎤᏂᏍᎪᎸ", "3p", {"a"}))
    a_list.append(Adjective("ᏗᏌᎪᏂᎨ ᎤᏂᏍᎪᎸ", "3p", {"i"}))
    a_list.append(Adjective("ᎠᏂᏌᎪᏂᎨ ᎤᏂᏍᎪᎸ", "3p", {"a"}))
    a_list.append(Adjective("ᏗᏓᎶᏂᎨ ᎤᏂᏍᎪᎸ", "3p", {"i"}))
    a_list.append(Adjective("ᎠᏂᏓᎶᏂᎨ ᎤᏂᏍᎪᎸ", "3p", {"a"}))

    a_list.append(Adjective("ᏧᏁᎦ", "3p", {"i"}))
    a_list.append(Adjective("ᎤᏂᏁᎦ", "3p", {"a"}))
    a_list.append(Adjective("ᏧᏬᏗᎨ", "3p", {"i"}))
    a_list.append(Adjective("ᏧᏃᏗᎨ", "3p", {"a"}))

    return a_list


def sentence_templates() -> list[str]:
    st: list[str] = list()
    st.append("{subject} {adjective} {object} {verb}")
    st.append("{adjective} {object} {verb} {subject}")
    st.append("{verb}-ᏍᎪ {adjective} {object} {subject}")
    st.append("{verb}-Ꮷ {adjective} {object} {subject}")

    # st.append("{subject} {adjective} {object} ᎠᎭᏂ ᎾᎥ {verb}")
    # st.append("{adjective} {object} ᎠᎭᏂ ᎾᎥ {verb} {subject}")

    # st.append("{subject} {adjective} {object} ᎤᎿ ᎾᎥ {verb}")
    # st.append("{adjective} {object} ᎤᎿ ᎾᎥ {verb} {subject}")

    st.append("ᎥᏝ {subject} {object} Ᏹ-{verb}")
    st.append("ᎥᏝ {object} Ᏹ-{verb} {subject}")

    st.append("{object} {adjective}")
    st.append("ᎥᏝ {object} {adjective} ᏱᎩ")
    st.append("ᎥᏝ {adjective} {object} ᏱᎩ")
    st.append("{object} ᎥᏝ {adjective} ᏱᎩ")

    st.append("{object} {adjective} ᎨᏒᎩ")
    st.append("{adjective} {object} ᎨᏒᎩ")
    st.append("{object} {adjective} ᎨᏎᏍᏗ")
    st.append("{adjective} {object} ᎨᏎᏍᏗ")
    st.append("{object} {adjective} ᎨᎲᎩ")
    st.append("{adjective} {object} ᎨᎲᎩ")

    st.append("ᎥᏝ {object} {adjective} ᏱᎨᏒᎩ")
    st.append("ᎥᏝ {adjective} {object} ᏱᎨᏒᎩ")
    st.append("ᎥᏝ {object} {adjective} ᏱᎨᏎᏍᏗ")
    st.append("ᎥᏝ {adjective} {object} ᏱᎨᏎᏍᏗ")
    st.append("ᎥᏝ {object} {adjective} ᏱᎨᎲᎩ")
    st.append("ᎥᏝ {adjective} {object} ᏱᎨᎲᎩ")

    st.append("{object} ᎥᏝ {adjective} ᏱᎨᏒᎩ")
    st.append("{object} ᎥᏝ {adjective} ᏱᎨᏎᏍᏗ")
    st.append("{object} ᎥᏝ {adjective} ᏱᎨᎲᎩ")

    # st.append("ᎦᏙ {adjective} {object} {verb}")
    st.append("ᎦᎪ {adjective} {object} {verb}")
    st.append("ᎦᎩ {adjective} {object} {verb}")

    st.append("ᎦᎪ ᎥᏝ {adjective} {object} Ᏹ-{verb}")

    return st


def alt_verb(verb: str) -> str:
    if random.choice([True, False, False, False]):
        verb = re.sub("ᏘᎭ$", "Ꮨ", verb)
        verb = re.sub("ᎧᎭ$", "Ꭷ", verb)
    return verb


def alt_words(sentence: str) -> str:
    sentence = re.sub("ᎪᏩᏘᎭ\\b", random.choice(["ᎪᏩᏘᎭ", "ᎪᏩᏘ"]), sentence)
    sentence = re.sub("ᎧᎭ\\b", random.choice(["ᎧᎭ", "Ꭷ"]), sentence)
    sentence = re.sub("\\bᎥᏍᎩᎾ\\b", random.choice(["ᎥᏍᎩᎾ", "ᏍᎩᎾ", "ᎥᏍᎩ", "ᎾᏍᎩ"]), sentence)
    sentence = re.sub("\\bᎥᏝ\\b", random.choice(["ᎥᏝ", "Ꮭ"]), sentence)
    sentence = re.sub("\\bᏩᎭᏯ\\b", random.choice(["ᏩᎭᏯ", "ᏩᏯ"]), sentence)
    sentence = re.sub("\\bᎠᎭᏫ\\b", random.choice(["ᎠᎭᏫ", "ᎠᏫ"]), sentence)
    sentence = re.sub("\\bᎠᎭᏂ\\b", random.choice(["ᎠᎭᏂ", "ᎠᏂ"]), sentence)
    sentence = re.sub("\\bᎦᏙ\\b", random.choice(["ᎦᏙ", "Ꮩ"]), sentence)

    sentence = re.sub("\\b(Ᏹ?)ᎨᏐᎢ\\b", random.choice(["\\1ᎨᏐᎢ", "\\1ᎨᏐ"]), sentence)
    sentence = re.sub("\\b(Ᏹ?)ᎨᏒᎩ\\b", random.choice(["\\1ᎨᏒᎩ", "\\1ᎨᏒᎢ", "\\1ᎨᏎᎢ"]), sentence)
    sentence = re.sub("\\b(Ᏹ?)ᎨᎲᎩ\\b", random.choice(["\\1ᎨᎲᎩ", "\\1ᎨᎲᎢ", "\\1ᎨᎮᎢ"]), sentence)

    sentence = re.sub("\\b(Ᏹ?ᎨᏐ)Ꭲ\\b", random.choice(["\\1Ꭲ", "\\1"]), sentence)
    sentence = re.sub("\\b(Ᏹ?ᎨᏒ)Ꭲ\\b", random.choice(["\\1Ꭲ", "\\1"]), sentence)
    sentence = re.sub("\\b(Ᏹ?ᎨᏎ)Ꭲ\\b", random.choice(["\\1Ꭲ", "\\1"]), sentence)
    sentence = re.sub("\\b(Ᏹ?ᎨᎲ)Ꭲ\\b", random.choice(["\\1Ꭲ", "\\1"]), sentence)
    sentence = re.sub("\\b(Ᏹ?ᎨᎮ)Ꭲ\\b", random.choice(["\\1Ꭲ", "\\1"]), sentence)
    return sentence


def load_previous_already():
    already: set[str] = set()
    with prev_already.open() as r:
        for line in r:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            line = re.sub("\\s+", " ", line).strip()
            already.add(line)
    return already


def main() -> None:
    global output_lyx
    wanted_sets: int = 5
    wanted_per_set: int = 10
    random.seed(wanted_sets * wanted_per_set)
    os.chdir(pathlib.Path(__file__).parent)

    subjects: list[SubjectObject] = subject_objects()
    verbs: list[VerbObject] = verb_objects()
    adjectives = adjectives_list()

    random.shuffle(subjects)
    random.shuffle(verbs)
    random.shuffle(adjectives)

    jalagi_content: str = ""

    wanted: int = wanted_sets * wanted_per_set
    print(f"Wanted: {wanted:,}")
    set_counter: int = 0
    item_counter: int = wanted_per_set
    prev_verb: str = ""
    prev_subj: str = ""
    prev_adj: str = ""
    prev_obj: str = ""
    prev_template: str = ""
    already: set[str] = load_previous_already()
    templates: list[str] = sentence_templates()
    sentences: list[str] = list()
    while len(sentences) < wanted:
        have_parts: int = 1
        verb: VerbObject = random.choice(verbs)
        verb_subject: SubjectObject = SubjectObject()
        if verb.subj.startswith("3"):
            for _ in range(9):
                verb_subject = random.choice(subjects)
                if verb_subject.subj != verb.subj:
                    verb_subject = SubjectObject()
                    continue
                if not verb_subject.classes.issubset(verb.classes):
                    verb_subject = SubjectObject()
                    continue
                if not verb_subject.is_person:
                    verb_subject = SubjectObject()
                    continue
                have_parts += 1
                break

        verb_object: SubjectObject = SubjectObject()
        if verb.obj.startswith("3"):
            for _ in range(9):
                verb_object = random.choice(subjects)
                if verb_object.subj != verb.obj:
                    verb_object = SubjectObject()
                    continue
                if not verb_object.classes.issubset(verb.classes):
                    verb_object = SubjectObject()
                    continue
                if verb_object.is_person:
                    verb_object = SubjectObject()
                    continue
                have_parts += 1
                break

        object_adjective: Adjective = Adjective()
        for _ in range(9):
            object_adjective = random.choice(adjectives)
            if not adjective_allowed(object_adjective.form):
                object_adjective = Adjective()
                break
            if verb_object.subj != object_adjective.subj:
                object_adjective = Adjective()
                continue
            if not object_adjective.classes.issubset(verb_object.classes):
                object_adjective = Adjective()
                continue
            have_parts += 1
            break

        if have_parts < 2:
            continue
        if verb.form == prev_verb:
            continue
        if verb_subject.form == prev_subj and prev_subj:
            continue
        if verb_object.form == prev_obj and prev_obj:
            continue
        if object_adjective.form == prev_adj and prev_adj:
            continue

        already_text = f"{verb_subject.form} {object_adjective.form} {verb_object.form} {verb.form}"
        already_text = re.sub("\\s+", " ", already_text).strip()
        if already_text in already:
            continue
        already.add(already_text)

        prev_verb = verb.form
        prev_subj = verb_subject.form
        prev_obj = verb_object.form
        prev_adj = object_adjective.form

        template: str = random.choice(templates)

        sentence: str = template
        sentence = sentence.replace("{subject}", verb_subject.form)
        sentence = sentence.replace("{object}", verb_object.form)
        sentence = sentence.replace("{adjective}", object_adjective.form)
        sentence = sentence.replace("{verb}", alt_verb(verb.form))

        sentence = alt_words(sentence)
        sentence = re.sub("\\s+", " ", sentence).strip()

        if not sentence:
            continue
        if not re.search("^Ꭵ?Ꮭ\\b", sentence) and sentence.count(" ") < 2:
            continue
        if re.search("^Ꭵ?Ꮭ\\b", sentence) and sentence.count(" ") < 3:
            continue

        if sentence.startswith("ᎦᎪ ") or sentence.startswith("ᎦᎩ "):
            sentence += "?"
            if not verb.subj.startswith("3"):
                continue
        elif sentence.startswith("Ꮩ ") or sentence.startswith("ᎦᏙ "):
            sentence += "?"
        elif "-ᏍᎪ" in sentence or "-Ꮷ" in sentence:
            sentence += "?"
        else:
            sentence += "."

        if "-ᏍᎪ" in sentence:
            sentence = sentence.replace("-ᏍᎪ", random.choice(["Ꮝ", "Ꮝ", "ᏍᎪ"]))
        if "-Ꮷ" in sentence:
            sentence = sentence.replace("-Ꮷ", "Ꮷ")
        if "Ᏹ-" in sentence:
            sentence = sentence.replace("Ᏹ-Ꭰ", "Ꮿ")
            sentence = sentence.replace("Ᏹ-Ꭱ", "Ᏸ")
            sentence = sentence.replace("Ᏹ-Ꭲ", "Ᏹ")
            sentence = sentence.replace("Ᏹ-Ꭳ", "Ᏺ")
            sentence = sentence.replace("Ᏹ-Ꭴ", "Ᏻ")
            sentence = sentence.replace("Ᏹ-Ꭵ", "Ᏼ")
            sentence = sentence.replace("Ᏹ-Ꭽ", "Ꮿ")
            sentence = sentence.replace("Ᏹ-Ꭾ", "Ᏸ")
            sentence = sentence.replace("Ᏹ-Ꭿ", "Ᏹ")
            sentence = sentence.replace("Ᏹ-Ꮀ", "Ᏺ")
            sentence = sentence.replace("Ᏹ-Ꮁ", "Ᏻ")
            sentence = sentence.replace("Ᏹ-Ꮂ", "Ᏼ")
            sentence = sentence.replace("Ᏹ-", "Ᏹ")

        if "Ꮻ-" in sentence:
            sentence = sentence.replace("Ꮻ-Ꭰ", "Ꮹ")
            sentence = sentence.replace("Ꮻ-Ꭱ", "Ꮺ")
            sentence = sentence.replace("Ꮻ-Ꭲ", "Ꮻ")
            sentence = sentence.replace("Ꮻ-Ꭳ", "Ꮼ")
            sentence = sentence.replace("Ꮻ-Ꭴ", "Ꮽ")
            sentence = sentence.replace("Ꮻ-Ꭵ", "Ꮢ")
            sentence = sentence.replace("Ꮻ-Ꭽ", "Ꮹ")
            sentence = sentence.replace("Ꮻ-Ꭾ", "Ꮺ")
            sentence = sentence.replace("Ꮻ-Ꭿ", "Ꮻ")
            sentence = sentence.replace("Ꮻ-Ꮀ", "Ꮼ")
            sentence = sentence.replace("Ꮻ-Ꮁ", "Ꮽ")
            sentence = sentence.replace("Ꮻ-Ꮂ", "Ꮾ")
            sentence = sentence.replace("Ꮻ-", "Ꮻ")

        if re.search("\\bᎥ?Ꮭ [Ꭰ-Ᏼ]+ ᏱᎩ\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎩ\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᏐᎢ?\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᏒᎢ?\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᏒᎩ\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᏎᎢ?\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᎲᎢ?\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᎲᎩ\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᎮᎢ?\\b", sentence):
            continue
        if re.search("\\bᎥ?Ꮭ ᏱᎨᏎᏍᏗ\\b", sentence):
            continue

        if sentence in sentences:
            continue

        if template == prev_template:
            continue
        prev_template = template

        sentences.append(sentence)

    for sentence in sentences:
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
        jalagi_content += f"{sentence}"
        jalagi_content += "\end_layout\n"

    jalagi_content += "\n"
    jalagi_content += multicolumn_end
    jalagi_content += "\n"

    with open("written-jalagi-gilisi-template.lyx") as r:
        lyx_content = r.read()
        lyx_content = re.sub("(?s)\\\\begin_layout Standard\\s+jalagi\\s+\\\\end_layout\\s+",
                             jalagi_content.replace("\\", "\\\\"), lyx_content)

    if output_lyx is None:
        output_lyx =  pathlib.Path(__file__).with_suffix(".lyx")

    with output_lyx.open("w") as w:
        w.write(lyx_content)

    with output_lyx.with_suffix(".txt").open("w") as w:
        for sentence in sentences:
            w.write(sentence)
            w.write("\n")
    already_file = pathlib.Path(output_lyx)
    already_file = already_file.with_name(already_file.stem + "-already").with_suffix(".txt")
    with already_file.open("w") as w:
        for already_item in already:
            w.write(already_item)
            w.write("\n")


if __name__ == '__main__':
    main()
