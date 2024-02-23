from enum import IntFlag
from typing import NamedTuple

from fcm.line_segment_section import read_line_segment_section, LineSegmentSection
from fcm.segment_line import read_segment_line, SegmentLine
from fcm.util import read_uint, DEBUG_assert_expected, read_bytes


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
    unknown1: int
    unknown2: int
    unknown3: int
    unknown4: int
    is_open: bool
    path_to_cut: bool
    path_to_draw: bool
    target_seam_allowance: bool
    rhinestone: bool
    paint_the_face_when_drawing: bool
    correction_by_scanner_correction_value: bool
    add_additional_line_at_draw: bool
    is_perforating: bool
    is_emboss: bool
    is_foil: bool
    is_only_for_draw: bool
    line_segment: LineSegmentSection | None
    rhinestone_segments: list[SegmentLine]


def read_path_header_section(buffer: bytes, offset: int = 0) -> tuple[int, PathHeaderSection]:
    offset, unknown1 = read_uint(buffer, 4, offset)
    offset, unknown2 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("path unknown2", unknown2, [0x00000004])

    offset, tool = read_path_tool(buffer, offset)
    offset, outline_count = read_uint(buffer, 4, offset)
    offset, rhinestone_count = read_uint(buffer, 4, offset)

    offset, unknown3 = read_uint(buffer, 2, offset)
    DEBUG_assert_expected("path unknown3", unknown3, [
        0x0000, 0x008b, 0x008c, 0x00b3, 0x00b4, 0x0113, 0x0112, 0x00eb,
    ])
    # 0x0000 means closed, 0x3f00 means it's an open path. But why?
    offset, unknown4 = read_uint(buffer, 2, offset)
    DEBUG_assert_expected("path unknown4", unknown4, [
        0x0000, 0x3f00
    ])

    line_segment = None
    if outline_count > 0:
        offset, line_segment = read_line_segment_section(buffer, outline_count, offset)

    rhinestones = []
    for i in range(0, rhinestone_count):
        offset, rhinestone = read_segment_line(buffer, offset)
        rhinestones.append(rhinestone)

    is_open = PathTool.PATH_OPEN in tool
    path_to_cut = PathTool.TOOL_CUT in tool
    path_to_draw = PathTool.TOOL_DRAW in tool
    target_seam_allowance = PathTool.SEAM_ALLOWANCE in tool
    rhinestone = PathTool.TOOL_RHINESTONE in tool
    paint_the_face_when_drawing = PathTool.FILL in tool
    correction_by_scanner_correction_value = PathTool.AUTO_ALIGN in tool
    add_additional_line_at_draw = False  # ToolFlag.ADDITIONAL_OUTLINE in tool
    is_perforating = PathTool.TOOL_PERFORATING in tool
    is_emboss = PathTool.TOOL_EMBOSS in tool
    is_foil = PathTool.TOOL_FOIL in tool
    is_only_for_draw = PathTool.TOOL_DRAW_ONLY in tool
    return offset, PathHeaderSection(
        unknown1,
        unknown2,
        unknown3,
        unknown4,
        is_open,
        path_to_cut,
        path_to_draw,
        target_seam_allowance,
        rhinestone,
        paint_the_face_when_drawing,
        correction_by_scanner_correction_value,
        add_additional_line_at_draw,
        is_perforating,
        is_emboss,
        is_foil,
        is_only_for_draw,
        line_segment,
        rhinestones,
    )
