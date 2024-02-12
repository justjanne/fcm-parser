from typing import NamedTuple, Tuple

from fcm.util import read_uint


class LinePoint(NamedTuple):
    end: Tuple[int, int]


def read_point_line(buffer: bytes, offset: int = 0) -> Tuple[int, LinePoint]:
    offset, endx = read_uint(buffer, 4, offset)
    offset, endy = read_uint(buffer, 4, offset)
    return offset, LinePoint(
        (endx, endy)
    )
