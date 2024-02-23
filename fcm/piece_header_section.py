from enum import IntFlag
from typing import NamedTuple

from fcm.path_header_section import PathHeaderSection, read_path_header_section
from fcm.util import read_uint, DEBUG_assert_expected, read_f32, read_bytes, read_bool


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
    unknown1: int
    unknown2: int
    width: int
    height: int
    unknown3: int
    transform: tuple[float, float, float, float, float, float]
    expansion_limit_value: int
    reduction_limit_value: int
    restrictions: PieceRestrictions
    unknown7: int
    label: str | None
    paths: list[PathHeaderSection]


def read_piece_header_section(buffer: bytes, offset: int = 0) -> tuple[int, PieceHeaderSection]:
    offset, unknown1 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown1", unknown1, [0x00000000])

    offset, unknown2 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown2", unknown2, [0x00000000])

    offset, width = read_uint(buffer, 4, offset)
    offset, height = read_uint(buffer, 4, offset)

    offset, unknown3 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown3", unknown3, [0x00000001])

    offset, transformA11 = read_f32(buffer, 4, offset)
    offset, transformA21 = read_f32(buffer, 4, offset)
    offset, transformA22 = read_f32(buffer, 4, offset)
    offset, transformA13 = read_f32(buffer, 4, offset)
    offset, transformA12 = read_f32(buffer, 4, offset)
    offset, transformA23 = read_f32(buffer, 4, offset)

    offset, expansion_limit_value = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece expansion_limit_value", expansion_limit_value, [0x00000000])

    offset, reduction_limit_value = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece expansion_limit_value", expansion_limit_value, [0x00000000])

    offset, restrictions = read_uint(buffer, 4, offset)

    # setting this to 0x00000011 fails parsing?
    offset, unknown7 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown7", unknown7, [0x00000004])

    offset, label_info = read_bool(buffer, 1, offset)
    offset, label = read_bytes(buffer, 3, offset)
    if label_info:
        label = label.decode("ascii")
    else:
        label = None

    offset, path_count = read_uint(buffer, 4, offset)
    paths = []
    for i in range(0, path_count):
        offset, path = read_path_header_section(buffer, offset)
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
        unknown7,
        label,
        paths
    )
