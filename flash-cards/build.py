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
import shutil
import subprocess


def main() -> None:

    output_folder: pathlib.Path = pathlib.Path("cll1-flashcards")
    os.chdir(pathlib.Path(__file__).resolve().parent)
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir()

    for tex_file in pathlib.Path(".").glob("*.tex"):
        subprocess.run(["xelatex", tex_file], check=True)
        pdf_file: pathlib.Path = tex_file.with_suffix(".pdf")
        shutil.move(pdf_file, output_folder)
        pdf_file.with_suffix(".aux").unlink()
        pdf_file.with_suffix(".log").unlink()

    zip_file = output_folder.with_suffix(".zip")
    docs_folder = pathlib.Path("..", "docs", "Flash Cards")
    subprocess.run(["zip", zip_file, "-r", output_folder])
    shutil.copy(zip_file, docs_folder)
    for pdf_file in docs_folder.glob("*.pdf"):
        pdf_file.unlink()

    index_md: str = """
    # Flash Cards
    
    ## ZIP Archive
    
    * Zip of all flashcards: [${FLD}.zip](${FLD}.zip).
    
    ## Individual PDFs
    
    """

    for pdf_file in output_folder.resolve().glob("*.pdf"):
        shutil.copy(pdf_file, docs_folder)
        pdf_name = pdf_file.name
        index_md += f"* [{pdf_name}]({pdf_name})\n"

    index_md += "\n"

    with open(docs_folder.resolve("index.md"), "w") as w:
        w.write(index_md)


if __name__ == '__main__':
    main()
