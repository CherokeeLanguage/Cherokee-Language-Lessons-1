#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda activate cherokee-lessons
exec python "$0" "$@"
exit $?
''"""
from __future__ import annotations

import os.path
import re
import shutil
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from PyPDF2.generic import Destination


def main() -> None:
    src_pdf = os.path.join("..", "Cherokee Language Lessons-Volume 1.pdf")
    out_dir = "pdf-splits"
    if not os.path.exists(src_pdf):
        raise RuntimeError(f"{src_pdf} not found!")
    shutil.rmtree(out_dir, ignore_errors=True)
    os.mkdir(out_dir)
    with open(src_pdf, "rb") as f:
        pdf = PdfFileReader(f)
        splits = get_split_page_starts(pdf)
        splits[0] = "Front Matter"
        section_name = re.sub("(?i)[^a-z0-9ᎠᏴ]", "_", splits[0])
        writer: PdfFileWriter|None = PdfFileWriter()
        chunk_counter: int = 1
        for page_no in range(pdf.numPages):
            if page_no and page_no in splits:
                filename = os.path.join(out_dir, f"{chunk_counter:03}-{section_name}.pdf")
                with open(filename, "wb") as w:
                    writer.write(w)
                chunk_counter += 1
                writer: PdfFileWriter = PdfFileWriter()
                section_name = re.sub("(?i)[^a-z0-9ᎠᏴ]", "_", splits[page_no])
            writer.add_page(pdf.getPage(page_no))
        filename = os.path.join(out_dir, f"{chunk_counter:03}-{section_name}.pdf")
        with open(filename, "wb") as w:
            writer.write(w)


def get_split_page_starts(pdf: PdfFileReader):
    chapter_lookup: dict[int, str] = dict()
    bookmarks: list[Destination | list[Destination | list[Destination]]] = pdf.getOutlines()
    b: Destination
    for b in bookmarks:
        # Only interested in Top Level splits - maps to Chapter for this book
        if isinstance(b, list):
            continue
        chapter_lookup[pdf.getDestinationPageNumber(b)] = str(b["/Title"])
    return chapter_lookup


if __name__ == '__main__':
    main()
