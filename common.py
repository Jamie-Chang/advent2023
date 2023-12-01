from functools import wraps
from pathlib import Path
from typing import Callable, Iterable, Iterator


def get_input(*, day: int) -> Path:
    return Path(__file__).parent / "inputs" / f"d{day}.txt"


def read_lines(path: Path) -> Iterator[str]:
    with path.open() as f:
        for line in f:
            yield line.rstrip()


def first[T](it: Iterable[T], /) -> T:
    """
    >>> first([1, 2, 3])
    1

    >>> first([])
    Traceback (most recent call last):
        ...
    ValueError: Empty Iterator
    """

    try:
        return next(iter(it))
    except StopIteration:
        raise ValueError("Empty Iterator")


def collect[T: Iterable, V, **P](
    collector: Callable[[T], V], /
) -> Callable[[Callable[P, T]], Callable[P, V]]:
    """
    Flexible way to collect results for generator functions
    >>> @collect(sum)
    ... def iterator():
    ...     yield 1
    >>> iterator()
    1

    >>> @collect(list)
    ... def iterator():
    ...     yield 1
    >>> iterator()
    [1]

    """

    def wrapper(fn: Callable[P, T]) -> Callable[P, V]:
        @wraps(fn)
        def _new_func(*args: P.args, **kwargs: P.kwargs) -> V:
            return collector(fn(*args, **kwargs))

        return _new_func

    return wrapper


def collect_sum[**P](fn: Callable[P, Iterable[int]]) -> Callable[P, int]:
    """Common use case that confuses pylance"""
    return Callable[P, int], collect(sum)(fn)  # type: ignore
