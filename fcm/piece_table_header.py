from typing import NamedTuple

from fcm.piece_header_section import PieceHeaderSection, read_piece_header_section
from fcm.util import read_uint


class PieceTableHeader(NamedTuple):
    piece_ids: list[int]
    pieces: list[PieceHeaderSection]


def read_piece_table_header(buffer: bytes, offset: int = 0) -> tuple[int, PieceTableHeader]:
    offset, piece_offset_count = read_uint(buffer, 4, offset)
    piece_offsets = []
    for i in range(0, piece_offset_count):
        offset, piece_offset = read_uint(buffer, 4, offset)
        piece_offsets.append(piece_offset)

    offset, total_length = read_uint(buffer, 4, offset)
    offset, piece_id_count = read_uint(buffer, 4, offset)
    piece_ids = []
    for i in range(0, piece_id_count):
        offset, piece_id = read_uint(buffer, 2, offset)
        piece_ids.append(piece_id)

    pieces = []
    start_offset = offset
    for el_offset in piece_offsets:
        _, piece = read_piece_header_section(buffer, el_offset + start_offset)
        pieces.append(piece)
    offset = start_offset + total_length

    return offset, PieceTableHeader(
        piece_ids,
        pieces
    )
