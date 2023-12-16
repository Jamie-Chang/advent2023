from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from itertools import count
from pathlib import Path
from typing import Iterable, Iterator, Self, assert_never

from common import collect_sum, read_lines


class Tile(StrEnum):
    empty = "."
    rounded = "O"
    cubed = "#"


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

    def __iter__(self) -> Iterator[list[T]]:
        return self[:]

    def __getitem__(self, columns: slice) -> Iterator[list[T]]:
        for column in range(len(self))[columns]:
            yield list(map(lambda d: d[column], self.data))

    def __setitem__(self, key: int, sliced: list[T]) -> None:
        for row, value in zip(self.data, sliced):
            row[key] = value


@dataclass
class RowView[T]:
    data: list[list[T]]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[list[T]]:
        return self[:]

    def __getitem__(self, rows: slice) -> Iterator[list[T]]:
        for row in range(len(self))[rows]:
            yield self.data[row]

    def __setitem__(self, key: int, sliced: list[T]) -> None:
        self.data[key] = sliced


def get_rounded_indexes(column: list[Tile]) -> Iterator[int]:
    """
    >>> list(get_rounded_indexes(list(".O#.O")))
    [0, 3]
    """
    border = 0
    for i, value in enumerate(column):
        match value:
            case Tile.empty:
                ...
            case Tile.rounded:
                yield border
                border += 1

            case Tile.cubed:
                border = i + 1

            case _ as other:
                assert_never(other)


def _tilt(column: list[Tile]) -> Iterator[tuple[int, Tile]]:
    border = 0
    for i, value in enumerate(column):
        match value:
            case Tile.empty:
                ...
            case Tile.rounded:
                yield border, Tile.rounded
                border += 1

            case Tile.cubed:
                yield i, Tile.cubed
                border = i + 1

            case _ as other:
                assert_never(other)


def tilt(sliced: list[Tile]) -> list[Tile]:
    new_slice = [Tile.empty] * len(sliced)
    for i, tile in _tilt(sliced):
        new_slice[i] = tile

    return new_slice


@collect_sum
def score(grid: Grid) -> Iterator[int]:
    for column in grid.columns():
        yield sum(len(column) - i for i, v in enumerate(column) if v == Tile.rounded)


def part1(path: Path):
    grid = Grid.from_lines(read_lines(path))
    columns = grid.columns()

    for i, column in enumerate(columns):
        new_slice = tilt(column)
        columns[i] = new_slice

    return score(grid)


def run_cycle(grid: Grid):
    columns = grid.columns()
    rows = grid.rows()

    # North
    for i, column in enumerate(columns):
        new_slice = tilt(column)
        columns[i] = new_slice

    # West
    for i, row in enumerate(rows):
        new_slice = tilt(row)
        rows[i] = new_slice

    # South
    for i, column in enumerate(columns):
        new_slice = tilt(column[::-1])[::-1]
        columns[i] = new_slice

    # East
    for i, row in enumerate(rows):
        new_slice = tilt(row[::-1])[::-1]
        rows[i] = new_slice


def cycler(grid: Grid) -> range:
    past = {}
    for i in count():
        run_cycle(grid)
        state = grid.display()
        if index := past.get(state):
            return range(index, i)

        past[state] = i

    assert False


def part2(path: Path) -> int:
    grid = Grid.from_lines(read_lines(path))
    single_cycle = cycler(grid)
    offset = single_cycle[(999_999_999 - single_cycle.start) % len(single_cycle)]
    for _ in range(offset):
        run_cycle(grid)

    return score(grid)


def run(path: Path) -> tuple[int, int]:
    return part1(path), part2(path)
