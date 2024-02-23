import struct
import sys


def read_bytes(buffer: bytes, length: int, offset: int = 0, limit: int = -1) -> [int, bytes]:
    if 0 <= limit <= offset + length:
        return limit, None
    return offset + length, buffer[offset:offset + length]


def read_bool(buffer: bytes, length: int, offset: int = 0, limit: int = -1) -> [int, bytes]:
    offset, data = read_bytes(buffer, length, offset, limit)
    if data is None:
        return offset, None
    return offset, int.from_bytes(data, byteorder='little', signed=False) != 0


def read_int(buffer: bytes, length: int, offset: int = 0, limit: int = -1) -> [int, bytes]:
    offset, data = read_bytes(buffer, length, offset, limit)
    if data is None:
        return offset, None
    return offset, int.from_bytes(data, byteorder='little', signed=True) if data is not None else None


def read_uint(buffer: bytes, length: int, offset: int = 0, limit: int = -1) -> [int, bytes]:
    offset, data = read_bytes(buffer, length, offset, limit)
    if data is None:
        return offset, None
    return offset, int.from_bytes(data, byteorder='little', signed=False)


def read_f32(buffer: bytes, length: int, offset: int = 0, limit: int = -1) -> [float, bytes]:
    offset, data = read_bytes(buffer, length, offset, limit)
    if data is None:
        return offset, None
    return offset, struct.unpack('<f', data)[0]


def read_utf16_str(buffer: bytes, offset: int = 0, limit: int = -1) -> [int, bytes]:
    offset, length = read_uint(buffer, 1, offset, limit)
    if length is None:
        return offset, None
    return read_bytes(buffer, length * 2, offset)
