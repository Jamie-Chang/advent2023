from collections import defaultdict
from pathlib import Path

from common import collect_sum


def hash_algorithm(string: str) -> int:
    """
    >>> hash_algorithm("HASH")
    52
    """
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value


def part1(path: Path):
    return sum(map(hash_algorithm, path.read_text().split(",")))


@collect_sum
def part2(path: Path):
    hashmap = {}
    for value in path.read_text().split(","):
        if value.endswith("-"):
            hashmap.pop(value[:-1], None)
            continue

        label, lens = value.split("=")
        hashmap[label] = int(lens)

    boxes = defaultdict(list)
    for k, v in hashmap.items():
        boxes[hash_algorithm(k)].append(v)

    for box, lenses in boxes.items():
        for slot, lens in enumerate(lenses, 1):
            yield (box + 1) * slot * lens


def run(path: Path) -> tuple[int, int]:
    return part1(path), part2(path)
