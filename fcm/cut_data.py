from typing import NamedTuple, List, Tuple

from fcm.debug import debug_value
from fcm.piece import Piece, read_piece
from fcm.util import read_uint, DEBUG_assert_expected


class CutData(NamedTuple):
    mat_id: int
    cut_width: int
    cut_height: int
    # FIXME
    unknown1: int
    piece_offsets: List[int]
    piece_ids: List[int]
    pieces: List[Piece]


def read_cut_data(buffer: bytes, offset: int = 0) -> Tuple[int, CutData]:
    offset, mat_id = read_uint(buffer, 4, offset)
    offset, cut_width = read_uint(buffer, 4, offset)
    offset, cut_height = read_uint(buffer, 4, offset)
    debug_value("mat_id,cut_width,cut_height", (mat_id, cut_width, cut_height))

    offset, unknown1 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("cut_data unknown1", unknown1, [0x000007d0, 0x000002bc])

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
        _, piece = read_piece(buffer, el_offset + start_offset)
        pieces.append(piece)
    offset = start_offset + total_length
    return offset, CutData(
        mat_id,
        cut_width,
        cut_height,
        unknown1,
        piece_offsets,
        piece_ids,
        pieces
    )
