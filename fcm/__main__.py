import os

from fcm import convert_fcm, read_fcm_file
from fcm.util_debug import debug_print, debug_value

if __name__ == "__main__":
    os.makedirs("generated/", exist_ok=True)
    for directory in sorted(os.listdir("samples/")):
        if "." not in directory:
            for filename in sorted(os.listdir("samples/"+directory)):
                if filename.endswith(".fcm"):
                    convert_fcm(
                        "samples/{0}/{1}".format(directory, filename),
                        "generated/{0}_{1}.svg".format(directory, filename.removesuffix(".fcm"))
                    )
    debug_print()
