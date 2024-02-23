from typing import NamedTuple

from fcm.outline import read_outline, Outline
from fcm.util import read_int


class LineSegmentSection(NamedTuple):
    start: tuple[int, int]
    outlines: list[Outline]


def read_line_segment_section(buffer: bytes, count: int, offset: int = 0) -> tuple[int, LineSegmentSection]:
    offset, startx = read_int(buffer, 4, offset)
    offset, starty = read_int(buffer, 4, offset)

    outlines = []
    for i in range(0, count):
        offset, outline = read_outline(buffer, offset)
        outlines.append(outline)

    return offset, LineSegmentSection(
        (startx, starty),
        outlines
    )
