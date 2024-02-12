from typing import NamedTuple, Tuple

from fcm.cut_data import CutData, read_cut_data
from fcm.header import read_fcm_header, FcmHeader


class FcmFile(NamedTuple):
    file_header: FcmHeader
    cut_data: CutData


def read_fcm_file(buffer: bytes, offset: int = 0) -> FcmFile:
    offset, file_header = read_fcm_header(buffer, offset)
    offset, cut_data = read_cut_data(buffer, offset)
    return FcmFile(
        file_header,
        cut_data,
    )
