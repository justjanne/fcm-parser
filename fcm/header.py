import math
from typing import Tuple, NamedTuple

from fcm.debug import debug_value
from fcm.util import read_bytes, read_utf16_str, read_uint, DEBUG_assert_expected, read_int


class FcmHeader(NamedTuple):
    format_identifier: str
    file_version: str
    content_id: bytes
    short_name: str
    long_name: str
    author_name: str
    copyright: str
    # FIXME
    unknown1: int
    unknown2: Tuple[int, int]
    unknown3: str
    unknown4: int
    unknown5: int
    unknown6: int
    thumbnail_block_size_width: int
    thumbnail_block_size_height: int
    # FIXME
    unknown7: int
    unknown8: int
    unknown9: int
    unknown10: Tuple[int, int]
    unknown11: int
    unknown12: int
    unknown13: Tuple[int, int]
    storage_machine_model_id: str
    save_machine_ver: int
    file_type: int


def read_fcm_header(buffer: bytes, offset: int = 0) -> Tuple[int, FcmHeader]:
    offset, format_identifier = read_bytes(buffer, 4, offset)
    offset, file_version = read_bytes(buffer, 4, offset)
    debug_value("file_version", file_version)
    offset, content_id = read_bytes(buffer, 8, offset)

    offset, short_name = read_bytes(buffer, 8, offset)
    offset, long_name = read_utf16_str(buffer, offset)
    offset, author_name = read_utf16_str(buffer, offset)
    offset, copyright = read_utf16_str(buffer, offset)

    offset, unknown1 = read_uint(buffer, 2, offset)
    DEBUG_assert_expected("header unknown1", unknown1, [0x0303, 0x0403])
    offset, unknown2a = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown2a", unknown2a, [0x000004ee, 0x0000045e, 0x0000063e])
    offset, unknown3 = read_bytes(buffer, 2, offset)
    unknown3 = unknown3.decode("ascii")
    DEBUG_assert_expected("header unknown3", unknown3, ["BM"])
    offset, unknown2b = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown2b", unknown2b, [0x00000000, 0x000004ee, 0x0000045e, 0x0000063e])

    offset, unknown4 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown4", unknown4, [0x00000000])

    offset, unknown5 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown5", unknown5, [0x0000003e])

    offset, unknown6 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown6", unknown6, [0x00000028])

    offset, thumbnail_block_size_width = read_uint(buffer, 4, offset)
    offset, thumbnail_block_size_height = read_uint(buffer, 4, offset)
    # align line length to 32-bit integers
    thumbnail_line_length = math.ceil(thumbnail_block_size_width / 32.0) * 32
    thumbnail_byte_length = thumbnail_line_length // 8 * thumbnail_block_size_height
    debug_value("thumbnail_size", (thumbnail_block_size_width, thumbnail_block_size_height))

    offset, unknown7 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown7", unknown7, [0x00010001])

    offset, unknown8 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown8", unknown8, [0x00000000])

    offset, unknown9 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown9", unknown9, [0x00000000, 0x00000420])

    offset, unknown10a = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown10a", unknown10a, [0x00000000, 0x00001625, 0x00000ec4])
    offset, unknown10b = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown10b", unknown10b, [0x00000000, 0x00001625, 0x00000ec4])

    offset, unknown11 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown11", unknown11, [0x00000000, 0x00000002])

    offset, unknown12 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("header unknown12", unknown12, [0x00000000, 0x00000002])

    offset, unknown13a = read_int(buffer, 4, offset)
    DEBUG_assert_expected("header unknown13a", unknown13a, [0x00000000, 0xff000000])
    offset, unknown13b = read_int(buffer, 4, offset)
    DEBUG_assert_expected("header unknown13b", unknown13b, [0x00ffffff, 0xffffffff])

    offset, _ = read_bytes(buffer, thumbnail_byte_length, offset)
    offset, storage_machine_model_id = read_bytes(buffer, 4, offset)
    offset, save_machine_ver = read_uint(buffer, 4, offset)
    debug_value("storage_machine_model_id,save_machine_ver", (storage_machine_model_id, save_machine_ver))
    offset, file_type = read_uint(buffer, 4, offset)
    debug_value("file_type", file_type)

    return offset, FcmHeader(
        format_identifier,
        file_version,
        content_id,
        short_name.decode("ascii").split("\x00", maxsplit=1)[0],
        long_name.decode("utf-16-le"),
        author_name.decode("utf-16-le"),
        copyright.decode("utf-16-le"),
        unknown1,
        (unknown2a, unknown2b),
        unknown3,
        unknown4,
        unknown5,
        unknown6,
        thumbnail_block_size_width,
        thumbnail_block_size_height,
        unknown7,
        unknown8,
        unknown9,
        (unknown10a, unknown10b),
        unknown11,
        unknown12,
        (unknown13a, unknown13b),
        storage_machine_model_id,
        save_machine_ver,
        file_type
    )
