#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda activate cherokee-lessons
exec python "$0" "$@"
exit $?
''"""
import random


def main() -> None:
    random.seed(0)

    already_left: set[int] = set()
    already_right: set[int] = set()

    def next_left() -> int:
        left: int = random.randint(1, 13)
        if left in already_left:
            return next_left()
        return left

    def next_right() -> int:
        right: int = random.randint(1, 13)
        if right in already_right:
            return next_right()
        return right

    for ix in range(15):
        left: int = next_left()
        right: int = next_right()
        print(f"{left} ᎠᎴ {right}?")
        print(f"{left} ᎠᎴ {right} {left+right} ᎢᎩ.")



if __name__ == '__main__':
    main()

