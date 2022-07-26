import sys
from dataclasses import asdict, dataclass
import os
import re
import shutil
import json
from dataclasses import field
from json import JSONDecodeError

TERM_REGEX: str = "[Ꭰ-Ᏼ]+"
ENTRY_REGEX: str = "-?[Ꭰ-Ᏼ]+-?"

@dataclass
class Config:
    already_used: list[str] = field(default_factory=list)
    entries_file: str = "vocabulary.txt"
    unmatched_file: str = "vocabulary-unmatched.txt"
    vocab_template: str = "vocabulary-template.lyx"
    vocab_lyx: str = "vocabulary.lyx"
    source_file: str = "Cherokee Language Lessons-Volume 1.lyx"

    def load(self):
        if not os.path.isfile("vocabulary.json"):
            with open("vocabulary.json", "w") as w:
                json.dump(asdict(self), w, indent=4)

        with open("vocabulary.json", "r") as r:
            try:
                jconfig: dict = json.load(r)
                for key in jconfig.keys():
                    if hasattr(self, key):
                        setattr(self, key, jconfig[key])
            except JSONDecodeError as e:
                with open("vocabulary.json", "w") as w:
                    json.dump(asdict(self), w, indent=4)


def main() -> None:
    config: Config = Config()
    config.load()

    already_used: list[str]
    if config.already_used:
        already_used = config.already_used
    else:
        already_used = []

    entries_file = config.entries_file
    unmatched_file = config.unmatched_file
    vocab_template = config.vocab_template
    vocab_lyx = config.vocab_lyx
    source_file = config.source_file
    terms: list[str] = extract_terms(source_file)
    entries: dict[str] = dict()
    entry_breakdowns: dict[str] = dict()
    active_entry_breakdowns: dict[str] = dict()
    if not os.path.isfile(entries_file):
        with open(entries_file, "w"):
            pass
    with open(entries_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            parts: list[str] = line.split("|")
            if len(parts) != 4:
                print("Bad vocabulary entry: " + line)
                continue
            entry_word: str = parts[0].strip().upper()
            entry_pronounce: str = parts[1].strip()
            entry_breakdown: str = parts[2].strip()
            entry_definition: str = parts[3].strip()
            if not entry_definition:
                continue  # Ignore entries without a definition
            entries[entry_word] = (entry_word, entry_pronounce, entry_breakdown, entry_definition)
            if entry_word.startswith("-"):
                entry_breakdowns[entry_word] = (entry_word, entry_pronounce, entry_breakdown, entry_definition)

    with open(entries_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            parts: list[str] = line.split("|")
            if len(parts) != 4:
                print("Bad vocabulary entry: " + line)
                continue
            entry_term: str = parts[0].strip()
            entry_breakdown: str = parts[2].strip()
            entry_definition: str = parts[3].strip()
            if not entry_definition:
                continue  # Ignore entries without a definition
            if entry_breakdown:
                for match in re.finditer(ENTRY_REGEX, entry_breakdown):
                    item: str = match.group()
                    if not item:
                        continue
                    if not item.startswith("-"):
                        continue
                    if item.endswith("-"):
                        continue
                    if item not in entries:
                        entries[item] = (item, "", "", "")
                    if item not in entry_breakdowns:
                        entry_breakdowns[item] = (item, "", "", "")
                    if item not in active_entry_breakdowns and entry_term in terms:
                        active_entry_breakdowns[item] = (item, "", "", "")

    previous_entries: list[str] = []
    for already_file in already_used:
        if not os.path.isfile(already_file):
            print(f"Previous entries file {already_file} not found.")
            continue
        with open(already_file, "r") as w:
            for line in w:
                if line.strip().startswith("#"):
                    continue
                parts: list[str] = line.strip().split("|")
                if len(parts) == 4:
                    already_entry: str = parts[0].strip()
                    if already_entry not in previous_entries:
                        previous_entries.append(already_entry)
        print(f"Loaded {len(previous_entries):,} entries from {already_file}")

    for term in terms:
        if term in entries:
            continue
        if term in previous_entries:
            continue
        entries[term] = (term, "", "", "")

    entries_text: list[str] = list()

    entries_text.append(f"# {source_file}")
    entries_text.append("# ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳ ㉑ ㉒ ㉓ ㉔ ㉕ ㉖ ㉗ ㉘ ㉙ ㉚ ㉛ ㉜ ㉝ ㉞ ㉟ ㊱ ㊲ ㊳ ㊴ ㊵ ㊶ ㊷ ㊸ ㊹ ㊺ ㊻ ㊼ ㊽ ㊾ ㊿")
    entries_text.append("Syllabary|Pronounce|Breakdown|Definition")

    # first add entries with no definitions - in insertion order
    for term in entries:
        if not re.match(ENTRY_REGEX, term):
            continue
        (term, pronounce, break_down, definition) = entries[term]
        if definition:
            continue
        entries_text.append(f"{term}|{pronounce}|{break_down}|{definition}")

    # second add entries in ascending order with definitions
    for term in sorted(list(entries)):
        if not re.match(ENTRY_REGEX, term):
            continue
        (term, pronounce, break_down, definition) = entries[term]
        if not definition:
            continue
        entries_text.append(f"{term}|{pronounce}|{break_down}|{definition}")

    skip_entries: list[str] = list()
    # Output unmatched entries listing. Useful for manually pruning the master list.
    with open(f"{unmatched_file}", "w") as w:
        for entry in entries_text:
            entry_term: str = entry.split("|")[0]
            if entry_term in active_entry_breakdowns:
                continue
            if entry_term in terms:
                continue
            if entry_term in previous_entries:
                continue
            if " " in entry_term:
                continue
            skip_entries.append(entry_term)
            w.write(entry.strip())
            w.write("\n")

    # Output updated master entries file.
    with open(f"{entries_file}.tmp", "w") as w:
        for entry in entries_text:
            w.write(entry.strip())
            w.write("\n")
    shutil.copy(entries_file, f"{entries_file}.bak")
    shutil.copy(f"{entries_file}.tmp", entries_file)

    # Output updated used entries file.
    used_count: int = 0
    with open(f"used-{entries_file}", "w") as w:
        for entry in entries_text:
            parts: list[str] = entry.strip().split("|")
            if len(parts) != 4:
                continue
            (entry_term, _, _, definition) = parts
            if definition.strip() == "*":
                continue
            if entry_term in skip_entries:
                continue
            if entry_term.startswith("-") and entry_term not in active_entry_breakdowns.keys():
                continue
            w.write(entry.strip())
            w.write("\n")
            used_count += 1
    print(f"Wrote {used_count:,} entries to used-{entries_file}.")

    counter: int = 0
    section: str = ""
    split_section: int = 10
    with open(vocab_lyx, "w") as w:
        with open(vocab_template, "r") as r:
            for line in r:
                w.write(line)
                if line.startswith("\\begin_body"):
                    break
        w.write("\n")
        w.write("\\begin_layout Chapter\n")
        w.write("Vocabulary\n")
        w.write("\\end_layout\n")
        w.write("\n")
        for key in sorted(list(entries)):
            if not re.match(ENTRY_REGEX, key):
                continue
            if key in skip_entries:
                continue
            term: str
            pronounce: str
            break_down: str
            definition: str
            (term, pronounce, break_down, definition) = entries[key]
            if not definition.strip():
                continue
            if definition.strip() == "*":
                continue
            if term in previous_entries:
                continue
            if section != term[0]:
                section = term[0]
                w.write(section_entry(section))
                counter = 0
            elif (counter % split_section) == 0:
                w.write(section_entry(term))
            counter += 1
            w.write(glossary_entry(term, pronounce, break_down, definition))
            w.write("\n")
        w.write("\n")
        w.write("\\end_body")
        w.write("\n")
        w.write("\\end_document")
        w.write("\n")


def section_entry(section: str) -> str:
    return ("\n"
            "\\begin_layout\n"
            "Section*\n"
            f"{section}\n"
            "\\end_layout\n"
            "\n")


def glossary_entry(term: str, pronounce: str, break_down: str, definition: str) -> str:
    term = term.replace(" ", "\\begin_inset space ~\n\\end_inset\n\n")
    entry: str = (f"\n"
                  f"\\begin_layout Description\n"
                  f"{term} ")
    if definition[-1] not in ".,?!":
        definition += "."
    if pronounce:
        entry += f"[{pronounce}] "
    entry += (f"\\begin_inset Quotes eld\n"
              f"\\end_inset\n"
              f"\n"
              f"{definition}\n"
              f"\\begin_inset Quotes erd\n"
              f"\\end_inset\n"
              f"\n")
    if break_down:
        entry += f" ({break_down})"
    entry += (f"\n"
              f"\\end_layout\n"
              f"\n")
    return entry


def extract_terms(file: str) -> list[str]:
    terms: list[str] = list()
    with open(file, "r") as f:
        for line in f:
            for item in re.finditer(TERM_REGEX, line.upper()):
                chr_text: str = item.group()
                if not chr_text in terms:
                    terms.append(chr_text)

    return terms


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
