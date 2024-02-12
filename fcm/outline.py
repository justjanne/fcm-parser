from typing import NamedTuple, List, Union, Tuple

from fcm.point_bezier import BezierPoint, read_point_bezier
from fcm.point_line import LinePoint, read_point_line
from fcm.util import read_uint


class Outline(NamedTuple):
    type: int
    points: List[Union[LinePoint, BezierPoint]]


def read_outline(buffer: bytes, offset: int = 0) -> Tuple[int, Outline]:
    offset, outline_type = read_uint(buffer, 4, offset)
    offset, point_count = read_uint(buffer, 4, offset)

    points = []
    for i in range(0, point_count):
        if outline_type == 0:
            offset, point = read_point_line(buffer, offset)
        elif outline_type == 1:
            offset, point = read_point_bezier(buffer, offset)
        else:
            raise Exception("Unknowns outline type: " + str(outline_type))
        points.append(point)

    return offset, Outline(
        outline_type,
        points
    )
