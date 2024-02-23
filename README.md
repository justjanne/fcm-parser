# FCM Parser

This project contains my current research into writing a
free software implementation of brother's FCM format.

The data types used by the web app are documented in [fcm_format.txt].

## Features

- Read any FCM file 
- Convert any FCM file to SVG

## Roadmap

- Allow writing FCM files
- Rewrite the parser and serializer in Rust
- 5 parameters left to discover:
  - PieceHeaderSection[0:4] (always 00000000)
  - PieceHeaderSection[4:8] (always 00000000)
  - PieceHeaderSection[16:20] (always 01000000)
  - PathHeaderSection[0:4] (always 04000000)
  - PathHeaderSection[16:20] (varies wildly)

SVG to FCM:
- https://stackoverflow.com/questions/734076/how-to-best-approximate-a-geometrical-arc-with-a-bezier-curve
- https://stackoverflow.com/questions/3162645/convert-a-quadratic-bezier-to-a-cubic-one

[fcm_format.txt]: docs/fcm_format.txt
