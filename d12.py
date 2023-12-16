from functools import cache
from itertools import product
from pathlib import Path
from typing import Iterable, Iterator

from common import collect, collect_sum, read_lines


@collect(lambda s: "".join(s))
def substitute(value: str, with_values: Iterable[str]) -> Iterator[str]:
    """
    >>> substitute(".??..??...?##.", ".....")
    '...........##.'
    """
    with_values = iter(with_values)
    for v in value:
        if v == "?":
            yield next(with_values)
        else:
            yield v


def check(value: str, groups: list[int]) -> bool:
    """
    >>> check(".###.##..#..", [3, 2, 1])
    True
    """
    return [len(v) for v in value.split(".") if v] == groups


def count_broken(value: str) -> int:
    return sum(1 for v in value if v == "?")


def arrangements(value: str, groups: list[int]) -> Iterator[str]:
    """
    >>> list(arrangements(".??.????????.", [2, 2, 1, 2]))
    ['.##.##.#.##..', '.##.##.#..##.', '.##.##..#.##.', '.##..##.#.##.']
    """
    count_broken(value)
    for replacements in product(["#", "."], repeat=count_broken(value)):
        substituted = substitute(value, replacements)
        if check(substituted, groups):
            yield substituted


@cache
def possible(value: str, groups: tuple[int, ...]) -> int:
    """
    >>> possible(".??.????????.", (2, 2, 1, 2))
    4
    >>> possible("???.###", (1, 1, 3))
    1
    >>> possible(".??..??...?##.", (1,1,3))
    4
    >>> possible("??..??", ())
    1
    >>> possible("???????", (2, 1))
    10
    >>> possible("?###", (3))
    1
    >>> possible("?###????", (3,2))
    2
    >>> possible("???", (2))
    2
    >>> possible("?###????????", (3,2,1))
    10
    """
    if not groups:
        if any(c == "#" for c in value):
            return 0
        return 1

    size = groups[0]
    total: int = 0
    for i, v in enumerate(value):
        candidate = value[i : i + size]
        rest = value[i + size :]

        if len(candidate) < size:
            continue

        match v:
            case ".":
                continue

            case "#":
                # Commit to match
                if not any(c == "." for c in candidate) and not rest.startswith("#"):
                    total += possible(rest[1:], groups[1:])
                break

            case "?":
                # Tentatively match
                if any(c == "." for c in candidate):
                    continue

                if rest.startswith("#"):
                    continue

                total += possible(rest[1:], groups[1:])
    return total


@collect_sum
def part1(path: Path):
    for line in read_lines(path):
        springs, groups = line.split(" ")
        yield possible(springs, map(int, groups.split(",")))


@collect_sum
def part2(path: Path):
    for line in read_lines(path):
        springs, groups = line.split(" ")
        yield possible(
            "?".join(springs for _ in range(5)),
            tuple(map(int, groups.split(","))) * 5,
        )


def run(path: Path) -> tuple[int, int]:
    return part1(path), part2(path)
