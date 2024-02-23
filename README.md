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

SVG to FCM:
- https://stackoverflow.com/questions/734076/how-to-best-approximate-a-geometrical-arc-with-a-bezier-curve
- https://stackoverflow.com/questions/3162645/convert-a-quadratic-bezier-to-a-cubic-one

[fcm_format.txt]: docs/fcm_format.txt
