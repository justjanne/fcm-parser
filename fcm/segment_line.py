from typing import NamedTuple

from fcm.util import read_int


class SegmentLine(NamedTuple):
    end: tuple[int, int]


def read_segment_line(buffer: bytes, offset: int = 0) -> tuple[int, SegmentLine]:
    offset, endx = read_int(buffer, 4, offset)
    offset, endy = read_int(buffer, 4, offset)
    return offset, SegmentLine(
        (endx, endy)
    )
