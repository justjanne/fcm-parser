from typing import NamedTuple, Tuple, List, Optional

from fcm.path import Path, read_path
from fcm.util import read_uint, DEBUG_assert_expected, read_f32, read_bytes


class Piece(NamedTuple):
    # FIXME
    unknown1: int
    unknown2: int
    unknown3: Tuple[int, int]
    unknown4: int
    transform: Tuple[float, float, float, float, float, float]
    unknown6: int
    unknown7: int
    unknown8: int
    unknown9: int
    label: Optional[str]
    paths: List[Path]


def read_piece(buffer: bytes, offset: int = 0) -> Tuple[int, Piece]:
    offset, unknown1 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown1", unknown1, [0x00000000])

    offset, unknown2 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown2", unknown2, [0x00000000])

    offset, unknown3a = read_uint(buffer, 4, offset)
    offset, unknown3b = read_uint(buffer, 4, offset)

    offset, unknown4 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown4", unknown4, [0x00000001])

    # These are probably the align matrix values? seem to be a few correlated floats
    offset, transform1 = read_f32(buffer, 4, offset)
    offset, transform2 = read_f32(buffer, 4, offset)
    offset, transform3 = read_f32(buffer, 4, offset)
    offset, transform4 = read_f32(buffer, 4, offset)
    offset, transform5 = read_f32(buffer, 4, offset)
    offset, transform6 = read_f32(buffer, 4, offset)

    offset, unknown6 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown6", unknown6, [0x00000000])

    offset, unknown7 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown7", unknown7, [0x00000000])

    # FIXME
    # 0x00000000 means closed, #0x00000004 means it's an open path. But why?
    offset, unknown8 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown8", unknown8, [0x00000004, 0x00000000])

    offset, unknown9 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown9", unknown9, [0x00000004])

    offset, has_label = read_uint(buffer, 1, offset)
    offset, label = read_bytes(buffer, 3, offset)
    if has_label == 0x00:
        label = None
    elif has_label == 0x01:
        label = label.decode("ascii")
    else:
        raise Exception("unknown label type: " + has_label)

    offset, path_count = read_uint(buffer, 4, offset)
    paths = []
    for i in range(0, path_count):
        offset, path = read_path(buffer, offset)
        paths.append(path)

    return offset, Piece(
        unknown1,
        unknown2,
        (unknown3a, unknown3b),
        unknown4,
        (transform1, transform2, transform3, transform4, transform5, transform6),
        unknown6,
        unknown7,
        unknown8,
        unknown9,
        label,
        paths
    )
