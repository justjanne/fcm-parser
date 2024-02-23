from enum import IntFlag
from typing import NamedTuple

from ._util import read_uint, read_bytes
from .segment_bezier import SegmentBezier, read_segment_bezier
from .segment_line import SegmentLine, read_segment_line


class OutlineType(IntFlag):
    LINE = 0
    BEZIER = 1


def read_outline_type(buffer: bytes, offset: int = 0) -> tuple[int, OutlineType]:
    offset, data = read_bytes(buffer, 4, offset)
    return offset, OutlineType.from_bytes(data, byteorder='little', signed=False)


class Outline(NamedTuple):
    type: int
    segments: list[SegmentLine | SegmentBezier]


def read_outline(buffer: bytes, offset: int = 0) -> tuple[int, Outline]:
    offset, outline_type = read_outline_type(buffer, offset)
    offset, segment_count = read_uint(buffer, 4, offset)

    segments = []
    for i in range(0, segment_count):
        if outline_type == OutlineType.LINE:
            offset, point = read_segment_line(buffer, offset)
            segments.append(point)
        elif outline_type == OutlineType.BEZIER:
            offset, point = read_segment_bezier(buffer, offset)
            segments.append(point)

    return offset, Outline(
        outline_type,
        segments
    )
