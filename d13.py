from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Iterable, Iterator, Self
from itertools import chain, groupby

from common import collect_sum, read_lines


class Tile(StrEnum):
    ash = "."
    rock = "#"

    def other(self) -> Self:
        if self == self.ash:
            return self.rock
        return self.ash


@dataclass
class Grid:
    data: list[list[Tile]]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        return cls([[Tile(c) for c in line] for line in lines])

    def columns(self) -> ColumnView[Tile]:
        return ColumnView(self.data)

    def rows(self) -> RowView[Tile]:
        return RowView(self.data)

    def display(self) -> str:
        return "\n".join("".join(line) for line in self.data)


@dataclass
class ColumnView[T]:
    """
    >>> view = ColumnView([[1, 2, 3], [4, 5, 6]])
    >>> list(view[1:])
    [[2, 5], [3, 6]]
    >>> list(view[1::-1])
    [[2, 5], [1, 4]]
    """

    data: list[list[T]]

    def __len__(self) -> int:
        return len(self.data[0])

    def __getitem__(self, columns: slice) -> Iterator[list[T]]:
        for column in range(len(self))[columns]:
            yield list(map(lambda d: d[column], self.data))


@dataclass
class RowView[T]:
    data: list[list[T]]

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, rows: slice) -> Iterator[list[T]]:
        for row in range(len(self))[rows]:
            yield self.data[row]


def reflections(slices: RowView | ColumnView) -> Iterator[int]:
    for i in range(1, len(slices)):
        if all(f == b for f, b in zip(slices[i - 1 :: -1], slices[i:])):
            yield i


def first[T](it: Iterable[T]) -> T:
    return next(iter(it))


def difference[T](a: list[T], b: list[T]) -> int:
    return sum(1 for element_a, element_b in zip(a, b) if element_a != element_b)


def smudges(slices: RowView | ColumnView) -> Iterator[int]:
    for i in range(1, len(slices)):
        if sum(difference(f, b) for f, b in zip(slices[i - 1 :: -1], slices[i:])) == 1:
            yield i


def split_inputs(lines: Iterator[str]) -> Iterator[list[str]]:
    """
    >>> list(split_inputs(["A", "", "B", "C"]))
    [['A'], ['B', 'C']]
    """
    for has_content, group in groupby(lines, key=bool):
        if has_content:
            yield list(group)


def score(columns: Iterable[int], rows: Iterable[int]) -> int:
    return first(chain(columns, map(lambda v: 100 * v, rows)))


@collect_sum
def part1(grids: Iterable[Grid]) -> Iterator[int]:
    for grid in grids:
        yield score(reflections(grid.columns()), reflections(grid.rows()))


@collect_sum
def part2(grids: Iterable[Grid]) -> Iterator[int]:
    for grid in grids:
        yield score(smudges(grid.columns()), smudges(grid.rows()))


def get_grids(path: Path) -> Iterator[Grid]:
    for group in split_inputs(read_lines(path)):
        yield Grid.from_lines(group)


def run(path: Path) -> tuple[int, int]:
    return part1(get_grids(path)), part2(get_grids(path))
