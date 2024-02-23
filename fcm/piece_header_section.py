import struct
from enum import IntFlag
from typing import NamedTuple

from ._util import read_uint, read_f32, read_bytes
from ._util_debug import debug_value
from .path_header_section import PathHeaderSection, read_path_header_section


class PieceRestrictions(IntFlag):
    LICENSE_DESIGN = 0x0001
    SEAM_ALLOWANCE = 0x0002
    PROHIBITION_OF_SEAM_ALLOWANCE_SETTING = 0x0004
    NO_ASPECT_RATIO_CHANGE_PROHIBITED = 0x0020
    JUDGE_BY_USING_PERFECT_MASK_AT_AUTO_LAYOUT = 0x0020
    TEST_PATTERN = 0x0040
    PROHIBITION_OF_EDIT = 0x0080
    PROHIBITION_OF_TOOL = 0x0100


def read_piece_restrictions(buffer: bytes, offset: int = 0) -> tuple[int, PieceRestrictions]:
    offset, data = read_bytes(buffer, 4, offset)
    return offset, PieceRestrictions.from_bytes(data, byteorder='little', signed=False)


class PieceHeaderSection(NamedTuple):
    # FIXME
    unknown1: any
    unknown2: any
    width: int
    height: int
    unknown3: any
    transform: tuple[float, float, float, float, float, float]
    expansion_limit_value: int
    reduction_limit_value: int
    restrictions: PieceRestrictions
    label: str | None
    paths: list[PathHeaderSection]


def read_piece_header_section(buffer: bytes, offset: int = 0) -> tuple[int, PieceHeaderSection]:
    offset, unknown1 = read_bytes(buffer, 4, offset)
    debug_value("piece unknown1", unknown1.hex())

    offset, unknown2 = read_bytes(buffer, 4, offset)
    debug_value("piece unknown2", unknown2.hex())

    offset, width = read_uint(buffer, 4, offset)
    offset, height = read_uint(buffer, 4, offset)

    offset, unknown3 = read_bytes(buffer, 4, offset)
    debug_value("piece unknown3", unknown3.hex())

    offset, transformA11 = read_f32(buffer, 4, offset)
    offset, transformA21 = read_f32(buffer, 4, offset)
    offset, transformA22 = read_f32(buffer, 4, offset)
    offset, transformA13 = read_f32(buffer, 4, offset)
    offset, transformA12 = read_f32(buffer, 4, offset)
    offset, transformA23 = read_f32(buffer, 4, offset)

    offset, expansion_limit_value = read_uint(buffer, 4, offset)
    offset, reduction_limit_value = read_uint(buffer, 4, offset)
    offset, restrictions = read_uint(buffer, 4, offset)

    offset, label_length = read_uint(buffer, 4, offset)
    offset, label_data = read_bytes(buffer, label_length, offset)
    has_label, label_text = struct.unpack('?3s', label_data)
    label = label_text.decode("ascii") if has_label else None

    offset, path_count = read_uint(buffer, 4, offset)
    paths = []
    for i in range(0, path_count):
        offset, path_length = read_uint(buffer, 4, offset)
        _, path = read_path_header_section(buffer, offset)
        offset += path_length
        paths.append(path)

    return offset, PieceHeaderSection(
        unknown1,
        unknown2,
        width,
        height,
        unknown3,
        (transformA11, transformA21, transformA22, transformA13, transformA12, transformA23),
        expansion_limit_value,
        reduction_limit_value,
        restrictions,
        label,
        paths
    )
