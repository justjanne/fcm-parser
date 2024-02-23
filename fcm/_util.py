import struct
import sys


def read_bytes(buffer: bytes, length: int, offset: int = 0) -> [int, bytes]:
    return offset + length, buffer[offset:offset + length]


def read_bool(buffer: bytes, length: int, offset: int = 0) -> [int, bytes]:
    offset, data = read_bytes(buffer, length, offset)
    return offset, int.from_bytes(data, byteorder='little', signed=False) != 0


def read_int(buffer: bytes, length: int, offset: int = 0) -> [int, bytes]:
    offset, data = read_bytes(buffer, length, offset)
    return offset, int.from_bytes(data, byteorder='little', signed=True)


def read_uint(buffer: bytes, length: int, offset: int = 0) -> [int, bytes]:
    offset, data = read_bytes(buffer, length, offset)
    return offset, int.from_bytes(data, byteorder='little', signed=False)


def read_f32(buffer: bytes, length: int, offset: int = 0) -> [float, bytes]:
    offset, data = read_bytes(buffer, length, offset)
    return offset, struct.unpack('<f', data)[0]


def read_utf16_str(buffer: bytes, offset: int = 0) -> [int, bytes]:
    offset, length = read_uint(buffer, 1, offset)
    return read_bytes(buffer, length * 2, offset)
