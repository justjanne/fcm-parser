from enum import IntEnum
from typing import NamedTuple

from ._util import read_uint, read_bytes, read_bool
from .point import read_point, Point


class FileType(IntEnum):
    CUT = 0x10
    PRINT_TO_CUT = 0x38


def read_file_type(buffer: bytes, offset: int = 0) -> tuple[int, FileType]:
    offset, data = read_bytes(buffer, 4, offset)
    return offset, FileType.from_bytes(data, byteorder='little', signed=False)


class CutDataHeader(NamedTuple):
    file_type: FileType
    mat_id: int
    cut_width: int
    cut_height: int
    seam_allowance_width: int
    align_needed: bool
    align_marks: list[Point]


def read_cut_data_header(buffer: bytes, offset: int = 0) -> tuple[int, CutDataHeader]:
    offset, file_type = read_file_type(buffer, offset)
    offset, mat_id = read_uint(buffer, 4, offset)
    offset, cut_width = read_uint(buffer, 4, offset)
    offset, cut_height = read_uint(buffer, 4, offset)
    offset, seam_allowance_width = read_uint(buffer, 4, offset)

    align_needed = False
    align_marks = []
    if file_type == FileType.PRINT_TO_CUT:
        offset, align_needed = read_bool(buffer, 4, offset)
        offset, align_mark_count = read_uint(buffer, 4, offset)
        for i in range(0, 4):
            offset, align_mark = read_point(buffer, offset)
            if i < align_mark_count:
                align_marks.append(align_mark)

    return offset, CutDataHeader(
        file_type,
        mat_id,
        cut_width,
        cut_height,
        seam_allowance_width,
        align_needed,
        align_marks
    )
