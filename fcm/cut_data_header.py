from typing import NamedTuple

from fcm.file_header import FileType
from fcm.util import read_uint
from fcm.util_debug import debug_value


class CutDataHeader(NamedTuple):
    mat_id: int
    cut_width: int
    cut_height: int
    seam_allowance_width: int
    align_flag: int
    align_marks: list[tuple[int, int]]


def read_cut_data_header(file_type: FileType, buffer: bytes, offset: int = 0) -> tuple[int, CutDataHeader]:
    offset, mat_id = read_uint(buffer, 4, offset)
    offset, cut_width = read_uint(buffer, 4, offset)
    offset, cut_height = read_uint(buffer, 4, offset)
    debug_value("mat_id,cut_width,cut_height", (mat_id, cut_width, cut_height))
    offset, seam_allowance_width = read_uint(buffer, 4, offset)

    align_flag = 0
    align_marks: list[tuple[int, int]] = []
    if file_type == FileType.PRINT_TO_CUT:
        offset, align_flag = read_uint(buffer, 4, offset)
        offset, align_mark_count = read_uint(buffer, 4, offset)
        for i in range(0, 4):
            offset, align_mark_x = read_uint(buffer, 4, offset)
            offset, align_mark_y = read_uint(buffer, 4, offset)
            if i < align_mark_count:
                align_marks.append((align_mark_x, align_mark_y))

    return offset, CutDataHeader(
        mat_id,
        cut_width,
        cut_height,
        seam_allowance_width,
        align_flag,
        align_marks
    )
