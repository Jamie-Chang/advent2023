from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Self
from itertools import batched

from common import collect_sum, read_lines


@dataclass
class Card:
    winning_numbers: set[int]
    numbers: set[int]
    matches: int = field(init=False)

    def __post_init__(self):
        self.matches = len(self.winning_numbers & self.numbers)

    @classmethod
    def from_line(cls, line: str) -> Self:
        _, numbers = line.split(": ")
        winners, card = numbers.split(" | ")
        return cls(set(parse_numbers(winners)), set(parse_numbers(card)))

    @property
    def points(self) -> int:
        if self.matches == 0:
            return 0

        return 2 ** (self.matches - 1)


def parse_numbers(raw: str) -> Iterator[int]:
    return (int("".join(s).strip()) for s in batched(raw, 3))


def get_cards(cards: list[Card]) -> int:
    return sum(_cards(n + 1, cards) for n in range(len(cards)))


def _cards(card_number: int, cards: list[Card]) -> int:
    matches = cards[card_number - 1].matches
    return 1 + sum(_cards(card_number + 1 + i, cards) for i in range(matches))


@collect_sum
def part1(path: Path):
    for line in read_lines(path):
        yield Card.from_line(line).points


def part2(path: Path):
    return get_cards([Card.from_line(line) for line in read_lines(path)])


def run(path: Path):
    return part1(path), part2(path)
