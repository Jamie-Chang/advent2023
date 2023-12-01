from pathlib import Path
from typing import Final, Iterable, Iterator

from common import collect_sum, read_lines, first


NUMBER_MAP: Final[dict[str, int]] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

LENGTHS: set[int] = {len(k) for k in NUMBER_MAP}


def window(chars: str, size: int) -> Iterator[str]:
    return (chars[i : i + size] for i in range(len(chars)))


def parse_numbers(chars: str) -> Iterator[int]:
    """
    >>> list(parse_numbers('two1nine'))
    [2, 1, 9]
    >>> list(parse_numbers('eightwothree'))
    [8, 2, 3]
    >>> list(parse_numbers('9q'))
    [9]
    """

    windowed = zip(*(window(chars, length) for length in LENGTHS))

    for char, windows in zip(chars, windowed):
        if char.isdigit():
            yield int(char)
            continue

        try:
            yield first(
                NUMBER_MAP[window] for window in windows if window in NUMBER_MAP
            )
        except ValueError:
            pass


def part1(lines: Iterable[str]) -> int:
    return sum(
        int(
            first(c for c in line if c.isdigit())
            + first(c for c in reversed(line) if c.isdigit())
        )
        for line in lines
    )


@collect_sum
def part2(lines: Iterable[str]) -> Iterator[int]:
    for line in lines:
        numbers = list(parse_numbers(line))
        yield numbers[0] * 10 + numbers[-1]


def run(path: Path) -> tuple[int, int]:
    return (
        part1(read_lines(path)),
        part2(read_lines(path)),
    )
