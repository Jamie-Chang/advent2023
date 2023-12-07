import math
from pathlib import Path
from typing import Iterable, Iterator

from common import read_lines


type Time = int
type Distance = int


def parse(lines: Iterable[str]) -> Iterator[tuple[Time, Distance]]:
    time, distance = lines
    return zip(
        map(int, time.split(":")[1].split()),
        map(int, distance.split(":")[1].split()),
    )


def parse_single(lines: Iterable[str]) -> tuple[Time, Distance]:
    time, distance = lines
    return (
        int("".join(time.split(":")[1].split())),
        int("".join(distance.split(":")[1].split())),
    )


def solve(time: Time, distance: Distance) -> range:
    """
    >>> solve(7, 9)
    range(2, 6)

    >>> solve(15, 40)
    range(4, 12)

    >>> solve(30, 200)
    range(11, 20)
    """
    inner = math.sqrt(time**2 - 4 * distance)
    return range(int((time - inner) / 2) + 1, math.ceil((time + inner) / 2))


def product(it: Iterable[int], start: int = 1) -> int:
    for i in it:
        start *= i
    return start


def run(path: Path):
    return (
        product(len(solve(t, d)) for t, d in parse(read_lines(path))),
        len(solve(*parse_single(read_lines(path)))),
    )
