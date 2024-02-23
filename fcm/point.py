from typing import NamedTuple

from ._util import read_int


class Point(NamedTuple):
    x: int
    y: int


def read_point(buffer: bytes, offset: int = 0) -> tuple[int, Point]:
    offset, x = read_int(buffer, 4, offset)
    offset, y = read_int(buffer, 4, offset)
    return offset, Point(
        x, y
    )
