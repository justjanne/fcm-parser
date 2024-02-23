from enum import IntFlag
from typing import NamedTuple

from ._util import read_uint, read_bytes
from ._util_debug import debug_value
from .line_segment_section import read_line_segment_section, LineSegmentSection
from .segment_line import read_segment_line, SegmentLine


class PathTool(IntFlag):
    PATH_OPEN = 0x0001
    TOOL_CUT = 0x0002
    TOOL_DRAW = 0x0004
    SEAM_ALLOWANCE = 0x0008
    TOOL_RHINESTONE = 0x0010
    FILL = 0x0020
    AUTO_ALIGN = 0x0040
    TOOL_DRAW_ONLY = 0x1000
    TOOL_EMBOSS = 0x2000
    TOOL_FOIL = 0x4000
    TOOL_PERFORATING = 0x8000


def read_path_tool(buffer: bytes, offset: int = 0) -> tuple[int, PathTool]:
    offset, data = read_bytes(buffer, 4, offset)
    return offset, PathTool.from_bytes(data, byteorder='little', signed=False)


class PathHeaderSection(NamedTuple):
    # FIXME
    unknown1: any
    unknown2: any
    tool: PathTool
    line_segment: LineSegmentSection | None
    rhinestone_segments: list[SegmentLine]


def read_path_header_section(buffer: bytes, offset: int = 0) -> tuple[int, PathHeaderSection]:
    offset, unknown1 = read_bytes(buffer, 4, offset)
    debug_value("path unknown1", unknown1.hex())

    offset, tool = read_path_tool(buffer, offset)
    offset, outline_count = read_uint(buffer, 4, offset)
    offset, rhinestone_count = read_uint(buffer, 4, offset)

    offset, unknown2 = read_bytes(buffer, 4, offset)
    debug_value("path unknown2", unknown2.hex())

    line_segment = None
    if outline_count > 0:
        offset, line_segment = read_line_segment_section(buffer, outline_count, offset)

    rhinestones = []
    for i in range(0, rhinestone_count):
        offset, rhinestone = read_segment_line(buffer, offset)
        rhinestones.append(rhinestone)

    return offset, PathHeaderSection(
        unknown1,
        unknown2,
        tool,
        line_segment,
        rhinestones,
    )
