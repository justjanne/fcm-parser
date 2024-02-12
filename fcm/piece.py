from typing import NamedTuple, Tuple, List, Optional

from fcm.debug import debug_value
from fcm.path import Path, read_path
from fcm.util import read_uint, DEBUG_assert_expected, read_f32, read_bytes


class Piece(NamedTuple):
    # FIXME
    unknown1: int
    unknown2: int
    unknown3: Tuple[int, int]
    unknown4: int
    unknown5: Tuple[float, float, float, float, float, float]
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
    offset, unknown5a = read_f32(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown5", unknown5a, [1.0, 0.9996899366378784])
    offset, unknown5b = read_f32(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown5b", unknown5b, [0.0, 0.0011049534659832716])
    offset, unknown5c = read_f32(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown5c", unknown5c, [0.0])
    offset, unknown5d = read_f32(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown5d", unknown5d, [1.0, 1.007078766822815, ])
    offset, unknown5e = read_f32(buffer, 4, offset)
    offset, unknown5f = read_f32(buffer, 4, offset)
    debug_value("piece unknown5", (unknown5a, unknown5b, unknown5c, unknown5d))

    offset, unknown6 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown7", unknown6, [0x00000000])

    offset, unknown7 = read_uint(buffer, 4, offset)
    DEBUG_assert_expected("piece unknown7", unknown7, [0x00000000])

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
        (unknown5a, unknown5b, unknown5c, unknown5d, unknown5e, unknown5f),
        unknown6,
        unknown7,
        unknown8,
        unknown9,
        label,
        paths
    )
