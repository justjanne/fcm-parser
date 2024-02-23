from typing import NamedTuple

from ._util import read_int


class SegmentBezier(NamedTuple):
    control1: tuple[int, int]
    control2: tuple[int, int]
    end: tuple[int, int]


def read_segment_bezier(buffer: bytes, offset: int = 0) -> tuple[int, SegmentBezier]:
    offset, control1x = read_int(buffer, 4, offset)
    offset, control1y = read_int(buffer, 4, offset)
    offset, control2x = read_int(buffer, 4, offset)
    offset, control2y = read_int(buffer, 4, offset)
    offset, endx = read_int(buffer, 4, offset)
    offset, endy = read_int(buffer, 4, offset)
    return offset, SegmentBezier(
        (control1x, control1y),
        (control2x, control2y),
        (endx, endy)
    )
