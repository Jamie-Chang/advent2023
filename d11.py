from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Self

from common import collect_sum, read_lines

type Pair[T] = tuple[T, T]


@dataclass
class Slice:
    galaxies: set[int] = field(default_factory=set)

    def __bool__(self) -> bool:
        return bool(self.galaxies)

    def __iter__(self) -> Iterator[int]:
        return iter(self.galaxies)


@dataclass
class Image:
    galaxies: set[Pair[int]]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        row, col = -1, -1
        galaxies = set()
        for row, line in enumerate(lines):
            for col, value in enumerate(line):
                if value == "#":
                    galaxies.add((row, col))

        return cls(galaxies)

    @property
    def bound(self) -> Pair[int]:
        max_row = max(g[0] for g in self.galaxies) + 1
        max_col = max(g[1] for g in self.galaxies) + 1
        return max_row, max_col

    def __iter__(self) -> Iterator[Pair[int]]:
        return iter(self.galaxies)

    def columns(self) -> Iterator[Slice]:
        """
        >>> image = Image({(1, 2), (5, 7)})
        >>> empty = [Slice()]
        >>> list(image.columns()) == [*(empty * 2), Slice({1}), *(empty * 4), Slice({5})]
        True
        """
        index = defaultdict(set)
        for r, c in self.galaxies:
            index[c].add(r)

        for c in range(self.bound[1]):
            yield Slice(index[c])

    def rows(self) -> Iterator[Slice]:
        """
        >>> image = Image({(2, 1), (7, 5)})
        >>> empty = [Slice()]
        >>> list(image.rows()) == [*(empty * 2), Slice({1}), *(empty * 4), Slice({5})]
        True
        """
        index = defaultdict(set)
        for r, c in self.galaxies:
            index[r].add(c)

        for r in range(self.bound[0]):
            yield Slice(index[r])

    def expand_columns(self, factor: int = 2):
        """
        >>> image = Image({(1, 2), (5, 7)})
        >>> image.expand_columns() == Image({(1, 4), (5, 13)})
        True
        """
        return Image(
            {(r, c) for c, sliced in expand(self.columns(), factor) for r in sliced}
        )

    def expand_rows(self, factor: int = 2):
        """
        >>> image = Image({(2, 1), (7, 5)})
        >>> image.expand_rows() == Image({(4, 1), (13, 5)})
        True
        """
        return Image(
            {(r, c) for r, sliced in expand(self.rows(), factor) for c in sliced}
        )


def expand(slices: Iterable[Slice], factor: int = 2) -> Iterator[tuple[int, Slice]]:
    """
    >>> result = list(expand([Slice(), Slice(), Slice({1})]))
    >>> result == [(4, Slice({1}))]
    True
    """
    i = 0
    for sliced in slices:
        if not sliced:
            i += factor
            continue

        yield i, sliced
        i += 1


def distance(a: Pair[int], b: Pair[int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@collect_sum
def part1(path: Path):
    image = Image.from_lines(read_lines(path))
    image = image.expand_columns()
    image = image.expand_rows()
    for coord1, coord2 in combinations(image, 2):
        yield distance(coord1, coord2)


@collect_sum
def part2(path: Path):
    image = Image.from_lines(read_lines(path))
    image = image.expand_columns(1000000)
    image = image.expand_rows(1000000)
    for coord1, coord2 in combinations(image, 2):
        yield distance(coord1, coord2)


def run(path: Path) -> tuple[int, int]:
    return part1(path), part2(path)
