from typing import NamedTuple, Tuple

from fcm.util import read_int


class BezierPoint(NamedTuple):
    control1: Tuple[int, int]
    control2: Tuple[int, int]
    end: Tuple[int, int]


def read_point_bezier(buffer: bytes, offset: int = 0) -> Tuple[int, BezierPoint]:
    offset, control1x = read_int(buffer, 4, offset)
    offset, control1y = read_int(buffer, 4, offset)
    offset, control2x = read_int(buffer, 4, offset)
    offset, control2y = read_int(buffer, 4, offset)
    offset, endx = read_int(buffer, 4, offset)
    offset, endy = read_int(buffer, 4, offset)
    return offset, BezierPoint(
        (control1x, control1y),
        (control2x, control2y),
        (endx, endy)
    )
