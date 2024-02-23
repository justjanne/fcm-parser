from typing import NamedTuple

from fcm.cut_data_header import CutDataHeader, read_cut_data_header
from fcm.file_header import FileHeader, read_file_header
from fcm.piece_table_header import PieceTableHeader, read_piece_table_header


class FcmFile(NamedTuple):
    file_header: FileHeader
    cut_data_header: CutDataHeader
    piece_table_header: PieceTableHeader


def read_fcm_file(buffer: bytes, offset: int = 0) -> FcmFile:
    offset, file_header = read_file_header(buffer, offset)
    offset, cut_data = read_cut_data_header(file_header.file_type, buffer, offset)
    offset, piece_table = read_piece_table_header(buffer, offset)
    return FcmFile(
        file_header,
        cut_data,
        piece_table
    )
