import os
import sys
from typing import TextIO

from fcm.file import read_fcm_file, FcmFile


def read_fcm(name: str) -> FcmFile:
    with open(name, "rb") as f:
        buf = f.read()
    return read_fcm_file(buf)


def try_read(name: str):
    try:
        read_fcm(name)
    except Exception as e:
        print("Error processing {0}: ".format(name), file=sys.stderr)
        print(e, file=sys.stderr)


def generate_svg(out: TextIO, data: FcmFile):
    out.write('<svg viewBox="0 0 {0} {1}" width="{2}mm" height="{3}mm" xmlns="http://www.w3.org/2000/svg">\n'.format(
        data.cut_data.cut_width,
        data.cut_data.cut_height,
        data.cut_data.cut_width / 100.0,
        data.cut_data.cut_height / 100.0
    ))
    out.write('  <rect x="0" y="0" width="100%" height="100%" fill="#eeeeee" />\n')
    for piece in data.cut_data.pieces:
        out.write('  <g transform="matrix({0} {1} {2} {3} {4} {5})">\n'.format(
            piece.transform[0], piece.transform[1], piece.transform[2],
            piece.transform[3], piece.transform[4], piece.transform[5],
        ))
        for path in piece.paths:
            if path.line_segment:
                path_data = "M {0},{1}".format(
                    path.line_segment.start[0], path.line_segment.start[1]
                )
                for outline in path.line_segment.outlines:
                    if outline.type == 0x00:
                        for point in outline.points:
                            path_data += "L {0},{1}".format(
                                point.end[0], point.end[1]
                            )
                    elif outline.type == 0x01:
                        for point in outline.points:
                            path_data += "C {0} {1}, {2} {3}, {4} {5}".format(
                                point.control1[0], point.control1[1],
                                point.control2[0], point.control2[1],
                                point.end[0], point.end[1]
                            )
                out.write('    <path fill="none" stroke="#000000" stroke-width="100" d="{0}" />\n'.format(path_data))
        out.write("  </g>\n")
    out.write("</svg>\n")


if __name__ == "__main__":
    for dirname in os.listdir("samples/"):
        for filename in os.listdir("samples/"+dirname):
            try_read("samples/"+dirname+"/"+filename)
    debug_print()
