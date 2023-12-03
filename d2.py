from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, Literal

from common import collect, collect_sum, read_lines


type Colour = Literal["red", "green", "blue"]
type CubeSet = Counter[Colour]


def parse_subset(raw: str) -> Counter:
    counter = Counter()
    for square in raw.split(", "):
        n, colour = square.split(" ")
        counter[colour] += int(n)

    return counter


def parse_line(raw: str) -> Iterator[Counter]:
    _, subsets = raw.split(sep=": ")
    return (parse_subset(subset) for subset in subsets.split("; "))


def power(cube_set: CubeSet) -> int:
    return cube_set["red"] * cube_set["green"] * cube_set["blue"]


def reduce_max(subsets: Iterable[CubeSet]) -> CubeSet:
    subsets = iter(subsets)
    result = Counter(next(subsets))
    for subset in subsets:
        for k, v in subset.items():
            result[k] = max(result[k], v)

    return result


@collect_sum
def part1(path: Path) -> Iterator[int]:
    target = Counter(red=12, green=13, blue=14)
    for number, line in enumerate(read_lines(path), 1):
        subsets = parse_line(line)
        if all(subset <= target for subset in subsets):
            yield number


@collect_sum
def part2(path: Path) -> Iterator[int]:
    for line in read_lines(path):
        yield power(reduce_max(parse_line(line)))


@collect(tuple)
def run(path: Path) -> Iterator[int]:
    yield part1(path)
    yield part2(path)
