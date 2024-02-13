# FCM Parser

This project contains my current research into writing a
free software implementation of brother's FCM format.

The data types used by the web app are documented in [fcm_format.txt].

Current Status:

- Can read and parse all FCM files I've found so far  
  **If you discover a file that fails to parse, please send it to me!**
- Should be enough to build a rudimentary fcm viewer
- 27 unknown parameters left to discover

SVG to FCM:
- https://stackoverflow.com/questions/734076/how-to-best-approximate-a-geometrical-arc-with-a-bezier-curve
- https://stackoverflow.com/questions/3162645/convert-a-quadratic-bezier-to-a-cubic-one

[fcm_format.txt]: docs/fcm_format.txt
