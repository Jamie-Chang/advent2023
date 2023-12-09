import math
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Iterable, Iterator, Self

import parse

from common import read_lines

type Instruction = str
type Node = str

line_parser = parse.compile("{node} = ({left}, {right})")


@dataclass
class Graph:
    paths: dict[Node, tuple[Node, Node]]

    def follow(self, from_node: Node, instruction: Instruction) -> Node:
        return self.paths[from_node][0 if instruction == "L" else 1]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        paths = {}
        for line in lines:
            result = line_parser.parse(line)
            assert isinstance(result, parse.Result)

            paths[result["node"]] = (result["left"], result["right"])

        return cls(paths)

    def path(self, start: Node, instructions: Iterable[Instruction]) -> Iterator[Node]:
        yield start
        for instruction in instructions:
            start = self.follow(start, instruction)
            yield start

    def nodes(self) -> Iterator[Node]:
        for node in self.paths:
            yield node


def parse_input(lines: Iterable[str]) -> tuple[str, Graph]:
    lines = iter(lines)
    instructions = next(lines)
    next(lines)  # skip a line

    graph = Graph.from_lines(lines)
    return instructions, graph


def get_cycle(start: Node, graph: Graph, instructions: str) -> int:
    for i, node in enumerate(iterable=graph.path(start, cycle(instructions))):
        if node[-1] == "Z":
            return i
    assert False


def part1(instructions: Iterable[Instruction], graph: Graph) -> int:
    start = "AAA"
    for i, node in enumerate(graph.path(start, instructions)):
        if node == "ZZZ":
            return i

    assert False


def product(values: Iterable[int]) -> int:
    value = 1
    for v in values:
        value *= v

    return value


def part2(instructions: str, graph: Graph) -> int:
    start_nodes = [node for node in graph.nodes() if node[-1] == "A"]

    # From observation these are whole cycles
    cycles = [get_cycle(start_node, graph, instructions) for start_node in start_nodes]
    gcd = math.gcd(*cycles)
    return product(cycles) // gcd ** (len(cycles) - 1)


def run(path: Path) -> tuple[int, int]:
    instructions, graph = parse_input(lines=read_lines(path))
    return part1(cycle(instructions), graph), part2(instructions, graph)
