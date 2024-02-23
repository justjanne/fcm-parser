from enum import IntEnum
from typing import NamedTuple

from fcm.util import read_bytes, read_utf16_str, read_uint, DEBUG_assert_expected
from fcm.util_debug import debug_value


class FileType(IntEnum):
    CUT = 0x10
    PRINT_TO_CUT = 0x38


def read_file_type(buffer: bytes, offset: int = 0) -> tuple[int, FileType]:
    offset, data = read_bytes(buffer, 4, offset)
    return offset, FileType.from_bytes(data, byteorder='little', signed=False)


class FileHeader(NamedTuple):
    format_identifier: str
    file_version: str
    content_id: int
    serial: bytes
    short_name: str
    long_name: str
    author_name: str
    copyright: str
    thumbnail_block_size_width: int
    thumbnail_block_size_height: int
    thumbnail_bytes: bytes
    storage_machine_model_id: str
    save_machine_ver: int
    file_type: FileType


def read_file_header(buffer: bytes, offset: int = 0) -> tuple[int, FileHeader]:
    offset, format_identifier = read_bytes(buffer, 4, offset)
    offset, file_version = read_bytes(buffer, 4, offset)
    debug_value("file_version", file_version)
    offset, content_id = read_uint(buffer, 4, offset)
    offset, serial = read_bytes(buffer, 4, offset)

    offset, short_name = read_bytes(buffer, 8, offset)
    offset, long_name = read_utf16_str(buffer, offset)
    offset, author_name = read_utf16_str(buffer, offset)
    offset, copyright = read_utf16_str(buffer, offset)

    # varies with mat size
    offset, thumbnail_block_size_width = read_uint(buffer, 1, offset)
    offset, thumbnail_block_size_height = read_uint(buffer, 1, offset)
    DEBUG_assert_expected("header thumbnail_block_size_width", thumbnail_block_size_width, [3])
    DEBUG_assert_expected("header thumbnail_block_size_height", thumbnail_block_size_height, [3, 4])

    offset, thumbnail_byte_length = read_uint(buffer, 4, offset)
    offset, _ = read_bytes(buffer, thumbnail_byte_length, offset)
    offset, storage_machine_model_id = read_bytes(buffer, 4, offset)
    offset, save_machine_ver = read_uint(buffer, 4, offset)
    debug_value("storage_machine_model_id,save_machine_ver", (storage_machine_model_id, save_machine_ver))
    offset, file_type = read_file_type(buffer, offset)
    debug_value("file_type", file_type.name)

    return offset, FileHeader(
        format_identifier,
        file_version,
        content_id,
        serial,
        short_name.decode("ascii").split("\x00", maxsplit=1)[0],
        long_name.decode("utf-16-le"),
        author_name.decode("utf-16-le"),
        copyright.decode("utf-16-le"),
        thumbnail_block_size_width,
        thumbnail_block_size_height,
        bytes(),
        storage_machine_model_id,
        save_machine_ver,
        file_type
    )
