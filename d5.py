from itertools import batched, count

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Self
from common import read_lines, collect


@dataclass
class RangeMapping:
    source: range
    destination: range

    def __post_init__(self):
        assert len(self.source) == len(
            self.destination
        ), f"{self.source = } {self.destination = }"

    @classmethod
    def from_line(cls, line: str) -> Self:
        destination, source, range_ = map(int, line.split(" "))
        return cls(
            range(source, source + range_), range(destination, destination + range_)
        )

    def __bool__(self) -> bool:
        return bool(self.source)

    def __contains__(self, value: int) -> bool:
        return value in self.source

    def __getitem__(self, value: int) -> int:
        return self.destination[self.source.index(value)]

    def reverse(self) -> Self:
        return RangeMapping(self.destination, self.source)


@dataclass
class Map:
    range_mappings: list[RangeMapping]

    def __getitem__(self, key: int) -> int:
        for mapping in self.range_mappings:
            if key in mapping:
                return mapping[key]

        return key

    def reverse(self) -> Self:
        return Map([rm.reverse() for rm in self.range_mappings])


class compose:
    def __init__(self, maps: Iterable[Map]) -> None:
        self.maps = list(maps)

    def __getitem__(self, key: int) -> int:
        for m in self.maps:
            key = m[key]

        return key

    def reverse(self) -> Self:
        return compose(map.reverse() for map in reversed(self.maps))


@dataclass
class SeedSet:
    seed_ranges: list[range]

    @classmethod
    def from_line(cls, line: str) -> Self:
        ranges = []
        for start, c in  batched(parse_seeds(line), 2):
            ranges.append(range(start, start + c))
        return cls(ranges)

    def __contains__(self, value: int):
        return any(value in s for s in self.seed_ranges)


def split_by[T](it: Iterable[T], value: T) -> Iterator[list[T]]:
    buffer = []
    for v in it:
        if v == value:
            yield buffer
            buffer = []
        else:
            buffer.append(v)

    yield buffer


def parse_seeds(raw: str) -> Iterator[int]:
    _, seeds = raw.split(": ")
    return (int(s) for s in seeds.split(" "))


@collect(min)
def part1(path: Path) -> Iterator[int]:
    groups = split_by(read_lines(path), "")
    seeds = list(parse_seeds(next(groups)[0]))
    composed = compose(
        Map([RangeMapping.from_line(line) for line in lines[1:]]) for lines in groups
    )

    # print(mapping)
    for seed in seeds:
        yield composed[seed]


def part2(path: Path) -> int:
    groups = split_by(read_lines(path), "")
    seeds = SeedSet.from_line(next(groups)[0])
    composed = compose(
        Map([RangeMapping.from_line(line) for line in lines[1:]]) for lines in groups
    )

    composed_reversed = composed.reverse()

    for i in count(0):
        seed = composed_reversed[i]
        if seed in seeds:
            return i

    assert False



# @collect(min)
# def part2(path: Path) -> Iterator[int]:
#     groups = split_by(read_lines(path), "")
#     seeds = list(batched(parse_seeds(next(groups)[0]), 2))
#     maps: list[Map] = []
#     for lines in groups:
#         result = mapping_parser.parse(lines[0])
#         assert isinstance(result, parse.Result)
#         maps.append(
#             Map([RangeMapping(*map(int, line.split(" "))) for line in lines[1:]])
#         )

#     mapping = compose(maps)
#     for start, n in seeds:
#         for seed in range(start, start + n):
#             yield mapping[seed]


def run(path):
    return part1(path), part2(path)
    # return (part1(path), part2(path))
