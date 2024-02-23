from typing import NamedTuple

from ._util import read_bytes, read_utf16_str, read_uint, read_bool


class FileHeader(NamedTuple):
    format_identifier: str
    file_version: str
    content_id: int
    short_name: str
    long_name: str
    author_name: str
    copyright: str
    thumbnail_block_size_width: int
    thumbnail_block_size_height: int
    thumbnail_bytes: bytes
    storage_machine_model_id: str
    save_machine_ver: int
    print_to_cut: bool


def read_file_header(buffer: bytes, offset: int = 0) -> tuple[int, FileHeader]:
    # static file header
    offset, format_identifier = read_bytes(buffer, 4, offset)
    offset, file_version = read_bytes(buffer, 4, offset)
    offset, content_id = read_uint(buffer, 4, offset)

    # dynamic file header
    offset, header_length = read_uint(buffer, 4, offset)
    limit = offset + header_length

    offset, short_name = read_bytes(buffer, 8, offset, limit)
    short_name = short_name.decode("ascii").split("\x00", maxsplit=1)[0]
    offset, long_name = read_utf16_str(buffer, offset, limit)
    long_name = long_name.decode("utf-16-le")
    offset, author_name = read_utf16_str(buffer, offset, limit)
    author_name = author_name.decode("utf-16-le")
    offset, copyright = read_utf16_str(buffer, offset, limit)
    copyright = copyright.decode("utf-16-le")

    offset, thumbnail_block_size_width = read_uint(buffer, 1, offset, limit)
    offset, thumbnail_block_size_height = read_uint(buffer, 1, offset, limit)
    offset, thumbnail_byte_length = read_uint(buffer, 4, offset, limit)
    offset, thumbnail_bytes = read_bytes(buffer, thumbnail_byte_length, offset, limit)

    offset, storage_machine_model_id = read_bytes(buffer, 4, offset, limit)
    offset, save_machine_ver = read_uint(buffer, 4, offset, limit)
    offset, print_to_cut = read_bool(buffer, 4, offset, limit)

    return limit, FileHeader(
        format_identifier,
        file_version,
        content_id,
        short_name,
        long_name,
        author_name,
        copyright,
        thumbnail_block_size_width,
        thumbnail_block_size_height,
        thumbnail_bytes,
        storage_machine_model_id,
        save_machine_ver,
        print_to_cut
    )
