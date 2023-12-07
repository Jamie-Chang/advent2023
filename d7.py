from collections import Counter
from enum import Enum, auto
from pathlib import Path
from typing import Iterable, Iterator, Self

from common import collect_sum, read_lines


class HandType(int, Enum):
    """
    >>> HandType.ONE_PAIR > HandType.HIGH_CARD
    True
    """

    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    @classmethod
    def from_hand(cls, hand: str, joker: bool = False) -> Self:
        """
        >>> HandType.from_hand("QJJQ2", joker=True) == HandType.FOUR_OF_A_KIND
        True
        >>> HandType.from_hand("KTJJT", joker=True) == HandType.FOUR_OF_A_KIND
        True
        >>> HandType.from_hand("JJJJJ", joker=True) == HandType.FIVE_OF_A_KIND
        True
        >>> HandType.from_hand("JJJJK", joker=True) == HandType.FIVE_OF_A_KIND
        True
        """
        counter = Counter(hand)
        if joker:
            jokers = counter.pop("J", 0)
            card = counter.most_common(1)[0][0] if counter else "J"
            counter[card] += jokers

        match counter.most_common(2):
            case (_, 1), (_, 1):
                return cls.HIGH_CARD
            case (_, 2), (_, 1):
                return cls.ONE_PAIR
            case (_, 2), (_, 2):
                return cls.TWO_PAIR
            case (_, 3), (_, 1):
                return cls.THREE_OF_A_KIND
            case (_, 3), (_, 2):
                return cls.FULL_HOUSE
            case (_, 4), _:
                return cls.FOUR_OF_A_KIND
            case [(_, 5)]:
                return cls.FIVE_OF_A_KIND
            case _ as other:
                assert False, other


STRENGTH_MAP = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def get_strength(hand: str, joker: bool = False) -> tuple[int, ...]:
    strength_map = {**STRENGTH_MAP, "J": 1} if joker else STRENGTH_MAP
    return tuple(strength_map[card] for card in hand)


def get_hand(line: str) -> str:
    return line.split()[0]


def get_sort_key(hand: str, joker: bool = False) -> tuple[HandType, tuple[int, ...]]:
    return HandType.from_hand(hand, joker), get_strength(hand, joker)


@collect_sum
def part1(lines: Iterable[str]) -> Iterator[int]:
    lines = sorted(lines, key=lambda line: get_sort_key(get_hand(line)))
    for rank, line in enumerate(lines, 1):
        yield rank * int(line.split()[1])


@collect_sum
def part2(lines: Iterable[str]) -> Iterator[int]:
    """
    >>> part2(
    ...     [
    ...         "32T3K 765",
    ...         "T55J5 684",
    ...         "KK677 28",
    ...         "KTJJT 220",
    ...         "QQQJA 483",
    ...     ]
    ... )
    5905
    """
    lines = sorted(lines, key=lambda line: get_sort_key(get_hand(line), joker=True))
    for rank, line in enumerate(lines, 1):
        yield rank * int(line.split()[1])


def run(path: Path) -> tuple[int, int]:
    return part1(read_lines(path)), part2(read_lines(path))
