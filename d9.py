from pathlib import Path
from typing import Iterator

from common import collect_sum, read_lines


def differentiate(sequence: list[int]) -> list[int]:
    """
    >>> differentiate([3, 3, 5, 9, 15])
    [0, 2, 4, 6]
    """
    return [n - c for c, n in zip(sequence, sequence[1:])]


def get_next_value(sequence: list[int]) -> int:
    """
    >>> get_next_value([10, 13, 16, 21, 30, 45])
    68
    >>> get_next_value([1, 3, 6, 10, 15, 21])
    28
    """
    if all(value == 0 for value in sequence):
        return 0
    return sequence[-1] + get_next_value(differentiate(sequence))


def get_prev_value(sequence: list[int]) -> int:
    """
    >>> get_prev_value([10, 13, 16, 21, 30, 45])
    5
    """
    if all(value == 0 for value in sequence):
        return 0
    return sequence[0] - get_prev_value(differentiate(sequence))


def run(path: Path) -> tuple[int, int]:
    return part1(path), part2(path)


@collect_sum
def part1(path: Path) -> Iterator[int]:
    for line in read_lines(path):
        sequence = list(map(int, line.split()))
        yield get_next_value(sequence)


@collect_sum
def part2(path: Path) -> Iterator[int]:
    for line in read_lines(path):
        sequence = list(map(int, line.split()))
        yield get_prev_value(sequence)
