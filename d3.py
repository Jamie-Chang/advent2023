from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Self
from common import collect_sum, product, read_lines


type Location = tuple[int, int]
type Object = PartNumber | Symbol


@dataclass
class PartNumber:
    value: int

    def __hash__(self) -> int:
        return id(self)


@dataclass(frozen=True)
class Symbol:
    value: str


def split_line(line: str):
    buffer = ""
    for c in line:
        match c:
            case digit if digit.isdigit():
                buffer += digit
            case other:
                if buffer:
                    yield buffer
                    buffer = ""

                yield other

    if buffer:
        yield buffer


def parse_line(line: str) -> Iterator[tuple[int, Object]]:
    """
    >>> list(parse_line('....'))
    []

    >>> list(parse_line('.*..'))
    [(1, Symbol(value='*'))]

    >>> list(parse_line('*...'))
    [(0, Symbol(value='*'))]

    >>> list(parse_line('*..*.'))
    [(0, Symbol(value='*')), (3, Symbol(value='*'))]

    >>> list(parse_line('...*'))
    [(3, Symbol(value='*'))]

    >>> list(parse_line('123..*'))
    [(0, PartNumber(value=123)), (1, PartNumber(value=123)), (2, PartNumber(value=123)), (5, Symbol(value='*'))]

    >>> list(parse_line('..123.'))
    [(2, PartNumber(value=123)), (3, PartNumber(value=123)), (4, PartNumber(value=123))]
    """
    index = 0
    for group in split_line(line):
        match group:
            case ".":
                ...
            case group if group.isdigit():
                part = PartNumber(int(group))
                for i in range(len(group)):
                    yield index + i, part

            case group if len(group) == 1:
                yield index, Symbol(group)

            case other:
                assert False, f"Symbol should only be a single character: {other}"

        index += len(group)


def adjacent(location: Location) -> Iterator[Location]:
    row, col = location
    yield row - 1, col - 1
    yield row - 1, col
    yield row - 1, col + 1
    yield row, col - 1
    yield row, col + 1
    yield row + 1, col - 1
    yield row + 1, col
    yield row + 1, col + 1


@dataclass
class SparseGrid:
    parts: dict[Location, PartNumber]
    symbols: dict[Location, Symbol]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        parts = {}
        symbols = {}
        for row, line in enumerate(lines):
            for col, obj in parse_line(line):
                match obj:
                    case PartNumber():
                        parts[row, col] = obj

                    case Symbol():
                        symbols[row, col] = obj

        return cls(parts, symbols)

    def get_adjacent_parts(self, location: Location) -> Iterable[PartNumber]:
        for new_location in adjacent(location):
            if obj := self.parts.get(new_location):
                yield obj

    def get_all_parts(self) -> Iterable[PartNumber]:
        for location in self.symbols:
            yield from self.get_adjacent_parts(location)


def part1(path: Path) -> int:
    grid = SparseGrid.from_lines(read_lines(path))
    return sum(p.value for p in set(grid.get_all_parts()))


@collect_sum
def part2(path: Path) -> Iterator[int]:
    grid = SparseGrid.from_lines(read_lines(path))
    for location, symbol in grid.symbols.items():
        if symbol.value != "*":
            continue

        parts = set(grid.get_adjacent_parts(location))
        if len(parts) == 2:
            yield product(part.value for part in parts)


def run(path: Path) -> tuple[int, int]:
    return (part1(path), part2(path))
