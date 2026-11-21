#!/usr/bin/env python3
"""Entry point: write the travel poster for MIRELL to /output/entry.png.

The poster is generated at run time by poster.py (PIL, bundled fonts, no
network, deterministic). If Pillow is unavailable in the sandbox, the
pre-rendered entry.png shipped in this repository -- produced by the same
poster.py -- is copied instead, so the entry is still valid.

Output directory: $MAKEFUN_OUTPUT_DIR, else /output, else ./output.
The written file is validated against the gate: a whole PNG, 1024x1024,
at most 1,048,576 bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576


def output_dir():
    for cand in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output"):
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
            probe = os.path.join(cand, ".write-test")
            with open(probe, "w") as f:
                f.write("ok")
            os.remove(probe)
            return cand
        except OSError:
            continue
    local = os.path.join(HERE, "output")
    os.makedirs(local, exist_ok=True)
    return local


def main():
    out_dir = output_dir()
    out = os.path.join(out_dir, "entry.png")
    try:
        from poster import render

        render(out)
        print("rendered poster with PIL")
    except ImportError:
        if not os.path.isfile(ASSET):
            sys.exit("Pillow is missing and no pre-rendered entry.png is shipped")
        shutil.copyfile(ASSET, out)
        print("Pillow missing; copied pre-rendered entry.png")
    if not os.path.isfile(out):
        sys.exit(f"no output written at {out}")
    size = os.path.getsize(out)
    if size > MAX_BYTES:
        sys.exit(f"entry.png too large: {size} bytes (max {MAX_BYTES})")
    with open(out, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (1024, 1024):
        sys.exit(f"entry.png is {width}x{height}, expected 1024x1024")
    print(f"wrote {out} ({size} bytes, 1024x1024 PNG)")


if __name__ == "__main__":
    main()
