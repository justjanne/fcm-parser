from typing import NamedTuple

from .point import read_point, Point


class SegmentLine(NamedTuple):
    end: Point


def read_segment_line(buffer: bytes, offset: int = 0) -> tuple[int, SegmentLine]:
    offset, end = read_point(buffer, offset)
    return offset, SegmentLine(
        end
    )
