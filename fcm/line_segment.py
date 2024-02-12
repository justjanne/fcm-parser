from typing import NamedTuple, Tuple, List

from fcm.outline import read_outline, Outline
from fcm.util import read_uint


class LineSegment(NamedTuple):
    start: Tuple[int, int]
    outlines: List[Outline]


def read_line_segment(buffer: bytes, count: int, offset: int = 0) -> Tuple[int, LineSegment]:
    offset, startx = read_uint(buffer, 4, offset)
    offset, starty = read_uint(buffer, 4, offset)

    outlines = []
    for i in range(0, count):
        offset, outline = read_outline(buffer, offset)
        outlines.append(outline)

    return offset, LineSegment(
        (startx, starty),
        outlines
    )
