from typing import NamedTuple

from .point import read_point, Point


class SegmentBezier(NamedTuple):
    control1: Point
    control2: Point
    end: Point


def read_segment_bezier(buffer: bytes, offset: int = 0) -> tuple[int, SegmentBezier]:
    offset, control1 = read_point(buffer, offset)
    offset, control2 = read_point(buffer, offset)
    offset, end = read_point(buffer, offset)
    return offset, SegmentBezier(
        control1,
        control2,
        end
    )
