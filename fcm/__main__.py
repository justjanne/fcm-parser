import os

from fcm.debug import debug_print
from fcm.file import read_fcm_file, FcmFile
from fcm.generate_svg import generate_svg


def read_fcm(name: str) -> FcmFile:
    with open(name, "rb") as f:
        buf = f.read()
    return read_fcm_file(buf)


def convert_fcm(input_file: str, output_file: str):
    with open(input_file, "rb") as file_in:
        fcm = read_fcm_file(file_in.read())
    with open(output_file, "w") as file_out:
        generate_svg(file_out, fcm)


if __name__ == "__main__":
    for directory in sorted(os.listdir("samples/")):
        for filename in sorted(os.listdir("samples/"+directory)):
            if filename.endswith(".fcm"):
                convert_fcm(
                    "samples/{0}/{1}".format(directory, filename),
                    "generated/{0}_{1}.svg".format(directory, filename.removesuffix(".fcm"))
                )
    debug_print()
