from dataclasses import InitVar, dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Iterable, Iterator, Self, assert_never

from common import read_lines

type Coord = tuple[int, int]
type Between = tuple[Coord, Coord]


def ilen(it: Iterable) -> int:
    return sum(1 for _ in it)


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

    @property
    def opposite(self) -> Self:
        match self:
            case self.NORTH:
                return self.SOUTH
            case self.SOUTH:
                return self.NORTH
            case self.WEST:
                return self.EAST
            case self.EAST:
                return self.WEST
            case _ as other:
                assert_never(other)

    def move_from(self, coord: Coord) -> Coord:
        """
        >>> Direction.NORTH.move_from((1, 1))
        (0, 1)
        >>> Direction.SOUTH.move_from((1, 1))
        (2, 1)
        >>> Direction.WEST.move_from((1, 1))
        (1, 0)
        >>> Direction.EAST.move_from((1, 1))
        (1, 2)
        """
        row, col = coord
        match self:
            case self.NORTH:
                return row - 1, col
            case self.SOUTH:
                return row + 1, col
            case self.WEST:
                return row, col - 1
            case self.EAST:
                return row, col + 1
            case _ as other:
                assert_never(other)


class Tile(str, Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_WEST = "7"
    SOUTH_EAST = "F"
    GROUND = "."
    START = "S"

    def movements(self) -> set[Direction]:
        match self:
            case self.VERTICAL:
                return {Direction.NORTH, Direction.SOUTH}
            case self.HORIZONTAL:
                return {Direction.WEST, Direction.EAST}
            case self.NORTH_WEST:
                return {Direction.NORTH, Direction.WEST}
            case self.NORTH_EAST:
                return {Direction.EAST, Direction.NORTH}
            case self.SOUTH_EAST:
                return {Direction.SOUTH, Direction.EAST}
            case self.SOUTH_WEST:
                return {Direction.SOUTH, Direction.WEST}
            case self.START:
                return {Direction.SOUTH, Direction.EAST}
            case self.GROUND:
                return set()
            case _ as other:
                assert_never(other)


def start_tile(grid: "Grid", start: Coord) -> Tile:
    directions = {
        d
        for d in Direction
        if d.move_from(start) in grid
        and d.opposite in grid[d.move_from(start)].movements()
    }
    if directions == {Direction.NORTH, Direction.SOUTH}:
        return Tile.VERTICAL
    if directions == {Direction.WEST, Direction.EAST}:
        return Tile.HORIZONTAL
    if directions == {Direction.NORTH, Direction.WEST}:
        return Tile.NORTH_WEST
    if directions == {Direction.EAST, Direction.NORTH}:
        return Tile.NORTH_EAST
    if directions == {Direction.SOUTH, Direction.EAST}:
        return Tile.SOUTH_EAST
    if directions == {Direction.SOUTH, Direction.WEST}:
        return Tile.SOUTH_WEST
    if directions == {Direction.SOUTH, Direction.EAST}:
        return Tile.START
    assert False


@dataclass
class Grid:
    values: list[list[Tile]]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        return cls([[Tile(t) for t in line] for line in lines])

    def __contains__(self, coord: Coord) -> bool:
        try:
            self[coord]
            return True
        except KeyError:
            return False

    def __setitem__(self, coord: Coord, tile: Tile) -> None:
        self.values[coord[0]][coord[1]] = tile

    def __getitem__(self, coord: Coord) -> Tile:
        if any(v < 0 for v in coord):
            raise KeyError(coord)
        try:
            return self.values[coord[0]][coord[1]]
        except IndexError as e:
            raise KeyError(coord) from e

    def coords(self) -> Iterator[Coord]:
        for row, cols in enumerate(self.values):
            for col in range(len(cols)):
                yield row, col

    def find(self, tile: Tile) -> Coord:
        for row, cols in enumerate(self.values):
            for col, value in enumerate(cols):
                if value is tile:
                    return row, col

        raise ValueError(f"Cannot find {tile}")

    def follow(
        self,
        start: Coord,
        direction: Direction,
    ) -> Iterator[Coord]:
        coord = start

        yield coord

        while (coord := direction.move_from(coord)) != start:
            yield coord
            available_movements = self[coord].movements() - {direction.opposite}
            direction, *others = available_movements
            assert not others


def super_sample(border: list[Coord]) -> Iterator[Coord]:
    for c, n in zip(border, border[1:] + [border[0]]):
        yield c[0] * 2, c[1] * 2
        yield (c[0] + n[0]), (c[1] + n[1])


@dataclass
class SuperSample:
    grid: Grid
    border: InitVar[list[Coord]]
    border_coords: set[Coord] = field(init=False)

    def __post_init__(self, border: list[Coord]):
        self.border_coords = set(super_sample(border))

    def __getitem__(self, coord: Coord) -> bool:
        if (coord[0] // 2, coord[1] // 2) not in self.grid:
            raise KeyError(coord)
        return coord not in self.border_coords

    def explore(self, start: Coord):
        queue = [start]
        seen = set()
        while queue:
            coord = queue.pop(0)

            if coord in seen:
                continue

            seen.add(coord)

            if not self[coord]:
                continue

            yield coord
            queue.extend(d.move_from(coord) for d in Direction)


def part2(grid: Grid, start: Coord, border: list[Coord]) -> int:
    row, col = start
    starts = [
        (row * 2 + 1, col * 2 + 1),
        (row * 2 - 1, col * 2 + 1),
        (row * 2 + 1, col * 2 - 1),
        (row * 2 - 1, col * 2 - 1),
    ]

    ground = SuperSample(grid, border)

    for start in starts:
        try:
            return ilen(
                (r, c) for r, c in ground.explore(start) if r % 2 == 0 and c % 2 == 0
            )
        except KeyError:
            ...

    assert False


def run(path: Path) -> tuple[int, int]:
    grid = Grid.from_lines(read_lines(path))
    start = grid.find(Tile.START)
    grid[start] = start_tile(grid, start)
    direction, *_ = grid[start].movements()

    border = list(grid.follow(direction=direction, start=start))

    return len(border) // 2, part2(grid, start, border)
