from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Iterable, Iterator, Protocol, Self

from common import collect, read_lines


class SupportsArithmetic(Protocol):
    def __add__(self, other: Self, /) -> Self:
        ...

    def __sub__(self, other: Self, /) -> Self:
        ...

    def __mul__(self, other: Self, /) -> Self:
        ...


type Pair[T] = tuple[T, T]


def add_pair[T: SupportsArithmetic](a: Pair[T], b: Pair[T]) -> Pair[T]:
    return (a[0] + b[0], a[1] + b[1])


class Tile(StrEnum):
    empty = "."
    forward_mirror = "/"
    backward_mirror = "\\"
    vertical_splitter = "|"
    horizontal_splitter = "-"


type Vector = Pair[int]
type Location = Pair[int]


class Direction(Enum):
    east = (0, 1)
    south = (1, 0)
    north = (-1, 0)
    west = (0, -1)


@dataclass(frozen=True)
class Beam:
    location: Location
    direction: Direction

    def redirect(self, direction: Direction) -> Self:
        return type(self)(
            add_pair(self.location, direction.value),
            direction,
        )

    def follow(self) -> Iterator[Self]:
        location = self.location
        yield self
        while True:
            location = add_pair(location, self.direction.value)
            yield type(self)(location, self.direction)


def beam(location: Location, direction: Direction) -> Iterator[Location]:
    while True:
        yield location
        location = add_pair(location, direction.value)


def skip[T](it: Iterable[T], n: int = 1) -> Iterator[T]:
    iterator = iter(it)
    for _ in zip(iterator, range(n)):
        ...

    return iterator


@dataclass
class Grid:
    data: list[list[Tile]]

    @property
    def dimensions(self) -> tuple[range, range]:
        return range(len(self.data)), range(len(self.data[0]))

    def __getitem__(self, key: Location) -> Tile:
        return self.data[key[0]][key[1]]

    def __contains__(self, key: Location) -> bool:
        rows, cols = self.dimensions
        return key[0] in rows and key[1] in cols

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        return cls([[Tile(c) for c in line] for line in lines])

    def trace(self, start: Location, direction: Direction) -> Iterator[Location]:
        queue = [Beam(start, direction)]
        seen = set()

        while queue:
            beam = queue.pop(0)
            if beam in seen:
                continue

            seen.add(beam)

            for beam in beam.follow():
                if beam.location not in self:
                    break

                yield beam.location

                match self[beam.location], beam.direction:
                    case Tile.empty, _:
                        continue

                    case Tile.forward_mirror, Direction.east:
                        queue.append(beam.redirect(Direction.north))

                    case Tile.forward_mirror, Direction.west:
                        queue.append(beam.redirect(Direction.south))

                    case Tile.forward_mirror, Direction.north:
                        queue.append(beam.redirect(Direction.east))

                    case Tile.forward_mirror, Direction.south:
                        queue.append(beam.redirect(Direction.west))

                    case Tile.backward_mirror, Direction.east:
                        queue.append(beam.redirect(Direction.south))

                    case Tile.backward_mirror, Direction.west:
                        queue.append(beam.redirect(Direction.north))

                    case Tile.backward_mirror, Direction.north:
                        queue.append(beam.redirect(Direction.west))

                    case Tile.backward_mirror, Direction.south:
                        queue.append(beam.redirect(Direction.east))

                    case Tile.vertical_splitter, Direction.east | Direction.west:
                        queue.append(beam.redirect(Direction.north))
                        queue.append(beam.redirect(Direction.south))

                    case Tile.horizontal_splitter, Direction.north | Direction.south:
                        queue.append(beam.redirect(Direction.east))
                        queue.append(beam.redirect(Direction.west))

                    case Tile.vertical_splitter | Tile.horizontal_splitter, _:
                        # other possibilities
                        continue

                break  # Unless we decide to continue


def run(path) -> tuple[int, int]:
    grid = Grid.from_lines(read_lines(path))
    locations = grid.trace((0, 0), Direction.east)
    return len(set(locations)), part2(grid)


@collect(max)
def part2(grid: Grid) -> Iterator[int]:
    rows, cols = grid.dimensions

    for row in rows:
        yield len(set(grid.trace((row, 0), Direction.east)))
        yield len(set(grid.trace((row, cols[-1]), Direction.west)))

    for col in cols:
        yield len(set(grid.trace((0, col), Direction.south)))
        yield len(set(grid.trace((rows[-1], col), Direction.north)))
