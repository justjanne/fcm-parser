import os
import sys

from fcm.debug import debug_print
from fcm.file import read_fcm_file


def try_read(name: str):
    try:
        with open(name, "rb") as f:
            buf = f.read()
        read_fcm_file(buf)
    except Exception as e:
        print("Error processing {0}: ".format(name), file=sys.stderr)
        print(e, file=sys.stderr)


if __name__ == "__main__":
    for dirname in os.listdir("samples/"):
        for filename in os.listdir("samples/"+dirname):
            try_read("samples/"+dirname+"/"+filename)
    debug_print()
