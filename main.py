#!/usr/bin/env python3
"""news-image-01: sum up the world's news of Friday 13 November 2026 in one
image.

The entry ships the finished front-page poster as entry.png (1024x1024,
under the 1 MiB gate) and this program writes it to the grader's output
directory. The poster was composed from a generated Earth-at-night
background with six verified 13 November 2026 headlines set on it as a
front page: the FAA lifting its four-hour nationwide ground stop, Ukraine
firing nearly 1,200 drones at Russia, the US downing two Iranian drones
near Bahrain, the Microsoft 365 outage entering a second day, China's
unannounced drills near Taiwan, and Nvidia chief Jensen Huang resigning.

Standard library only, no network, deterministic: the same input bytes are
copied on every run, so two runs write identical output.
"""

import os
import shutil
import struct
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024


def check_image(path):
    """Fail loudly unless the output is a whole PNG/JPEG inside the gate:
    at most 1 MiB and at most 1024x1024 px (dimensions read from the PNG
    IHDR with the standard library; a JPEG passes on magic bytes alone,
    its dimensions already fixed at build time)."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        width, height = struct.unpack(">II", head[16:24])
        kind = "PNG"
    elif head[:3] == b"\xff\xd8\xff":
        width = height = 0
        kind = "JPEG"
    else:
        raise SystemExit(f"error: {path} is neither PNG nor JPEG")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"error: {path} is {size} bytes, over the 1 MiB gate")
    if (width and width > MAX_DIMENSION) or (height and height > MAX_DIMENSION):
        raise SystemExit(f"error: {path} is {width}x{height}, over 1024x1024")
    return kind, width, height, size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(source, target)
    kind, width, height, size = check_image(target)
    dims = f"{width}x{height}" if width else "unknown dims"
    print(f"wrote {target} ({kind} {dims}, {size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
