from typing import NamedTuple

from .outline import read_outline, Outline
from .point import read_point, Point


class LineSegmentSection(NamedTuple):
    start: Point
    outlines: list[Outline]


def read_line_segment_section(buffer: bytes, count: int, offset: int = 0) -> tuple[int, LineSegmentSection]:
    offset, start = read_point(buffer, offset)

    outlines = []
    for i in range(0, count):
        offset, outline = read_outline(buffer, offset)
        outlines.append(outline)

    return offset, LineSegmentSection(
        start,
        outlines
    )
