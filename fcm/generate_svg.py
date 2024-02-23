from typing import TextIO

from .fcm_file import FcmFile
from .outline import OutlineType


def generate_svg(out: TextIO, data: FcmFile):
    out.write('<svg viewBox="0 0 {0} {1}" width="{2}mm" height="{3}mm" xmlns="http://www.w3.org/2000/svg">\n'.format(
        data.cut_data_header.cut_width,
        data.cut_data_header.cut_height,
        data.cut_data_header.cut_width // 100,
        data.cut_data_header.cut_height // 100,
    ))
    for piece in data.piece_table_header.pieces:
        out.write('  <g {6} transform="matrix({0} {1} {2} {3} {4} {5})">\n'.format(
            piece.transform[0], piece.transform[1], piece.transform[2],
            piece.transform[3], piece.transform[4], piece.transform[5],
            'id=\"{0}\"'.format(piece.label) if piece.label is not None else ''
        ))
        for path in piece.paths:
            if path.line_segment:
                path_data = "M {0},{1}".format(
                    path.line_segment.start[0], path.line_segment.start[1]
                )
                for outline in path.line_segment.outlines:
                    if outline.type == OutlineType.LINE:
                        for point in outline.points:
                            path_data += "L {0},{1}".format(
                                point.end[0], point.end[1]
                            )
                    elif outline.type == OutlineType.BEZIER:
                        for point in outline.points:
                            path_data += "C {0} {1}, {2} {3}, {4} {5}".format(
                                point.control1[0], point.control1[1],
                                point.control2[0], point.control2[1],
                                point.end[0], point.end[1]
                            )
                out.write('    <path fill="none" '
                          'stroke="#000000" '
                          'stroke-width="1" '
                          'vector-effect="non-scaling-stroke" '
                          'd="{0}" />\n'.format(path_data))
            for rhinestone in path.rhinestone_segments:
                out.write('    <circle fill="none" '
                          'stroke="#000000" '
                          'stroke-width="1" '
                          'vector-effect="non-scaling-stroke" '
                          'cx="{0}" cy="{1}" r="{2}mm" />\n'.format(
                    rhinestone.end[0], rhinestone.end[1], path.rhinestone_diameter / 2.0
                ))
        out.write("  </g>\n")
    out.write("</svg>\n")
