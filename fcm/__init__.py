from ._util_debug import debug_value
from .fcm_file import FcmFile, read_fcm_file
from .generate_svg import generate_svg


def read_fcm(name: str) -> FcmFile:
    with open(name, "rb") as f:
        buf = f.read()
    return read_fcm_file(buf)


def convert_fcm(input_file: str, output_file: str, thumbnail_file: str):
    with open(input_file, "rb") as file_in:
        fcm = read_fcm_file(file_in.read())
    with open(output_file, "w") as file_out:
        generate_svg(file_out, fcm)
    with open(thumbnail_file, "wb") as file_thumbnail:
        file_thumbnail.write(fcm.file_header.thumbnail_bytes)
