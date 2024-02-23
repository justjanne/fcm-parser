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


def DEBUG_assert_expected(context: str, value, expected: list):
    if type(value) is int:
        value = 0xFFFFFFFF & value
    if value not in expected:
        friendly_value = str(value)
        if type(value) is int:
            friendly_value = "0x" + int.to_bytes(value, 4, byteorder='big', signed=False).hex()
        print("Unexpected value for {0}: {1}".format(
            context,
            friendly_value
        ), file=sys.stderr)
