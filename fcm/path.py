from enum import IntFlag
from typing import NamedTuple, Tuple, List, Optional

from fcm.line_segment import LineSegment, read_line_segment
from fcm.point_line import read_point_line, LinePoint
from fcm.util import read_uint, DEBUG_assert_expected, read_bytes


class ToolFlag(IntFlag):
    PATH_OPEN = 0x0001
    CUT = 0x0002
    ADDITIONAL_OUTLINE = 0x0004
    EMBOSSING = 0x0008
    RHINESTONE = 0x0010
    FILL = 0x0020
    DRAW_ONLY = 0x1000
    # still missing: SEAM_ALLOWANCE, AUTO_ALIGN, PERFORATING, FOIL,


def read_tool_flags(buffer: bytes, offset: int = 0) -> Tuple[int, ToolFlag]:
    offset, data = read_bytes(buffer, 4, offset)
    return offset, ToolFlag.from_bytes(data, byteorder='little', signed=False)


class Path(NamedTuple):
    # FIXME
    unknown1: int
    unknown2: int
    tool: ToolFlag
    # FIXME
    unknown4: int
    line_segment: Optional[LineSegment]
    rhinestone_segments: List[LinePoint]


def read_path(buffer: bytes, offset: int = 0) -> Tuple[int, Path]:
    offset, unknown1 = read_uint(buffer, 4, offset)
    offset, unknown2 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("path unknown2", unknown2, [0x00000004])

    # More flags, too many to count
    offset, tool = read_tool_flags(buffer, offset)
    offset, outline_count = read_uint(buffer, 4, offset)
    offset, rhinestone_count = read_uint(buffer, 4, offset)

    offset, unknown4 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("path unknown4", unknown4, [
        0x00000000, 0x0000008b, 0x0000008c, 0x000000b3, 0x000000b4,
        0x00000113, 0x00000112, 0x000000eb, 0x3f000000
    ])

    line_segment = None
    if outline_count > 0:
        offset, line_segment = read_line_segment(buffer, outline_count, offset)

    rhinestones = []
    for i in range(0, rhinestone_count):
        offset, rhinestone = read_point_line(buffer, offset)
        rhinestones.append(rhinestone)

    return offset, Path(
        unknown1,
        unknown2,
        tool,
        unknown4,
        line_segment,
        rhinestones,
    )
