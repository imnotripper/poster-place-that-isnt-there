#!/usr/bin/env python3
"""Produce the MIRELL travel poster and hand it to the harness.

Running this script is the whole entry: it paints the poster for the isle
above the clouds (see poster.py) and drops the finished PNG at
``<output-dir>/entry.png``.  Where that directory lives is decided by
``pick_output_directory`` below.

Two ways to get the picture:

* the normal way — import :func:`poster.render` and paint the poster live
  with Pillow and the fonts bundled in this repo (no network, and the
  result is bit-for-bit reproducible);
* the fallback — if Pillow is not installed in the sandbox, reuse the
  ``entry.png`` already shipped in this repo, which was painted by the
  very same ``poster.py``.

Whatever path produced it, the file is then checked against the bounty
gate before the script reports success: it must be a real PNG, exactly
1024 by 1024 pixels, and no larger than 1,048,576 bytes.
"""

import os
import shutil
import sys

# Directory holding this script; the shipped fallback image lives here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FALLBACK_IMAGE = os.path.join(BASE_DIR, "entry.png")

OUTPUT_NAME = "entry.png"
SIZE_LIMIT = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Abort with a message on stderr and a non-zero exit code."""
    sys.exit(message)


def _writable(directory):
    """True when ``directory`` can be created and written to."""
    try:
        os.makedirs(directory, exist_ok=True)
        probe = os.path.join(directory, ".write-test")
        with open(probe, "w") as handle:
            handle.write("ok")
        os.remove(probe)
        return True
    except OSError:
        return False


def pick_output_directory():
    """Choose where ``entry.png`` goes.

    First the directory named by ``MAKEFUN_OUTPUT_DIR``, then ``/output``;
    the first of those that actually accepts a write wins.  When neither
    works, fall back to an ``output`` folder next to this script.
    """
    for candidate in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output"):
        if candidate and _writable(candidate):
            return candidate
    local_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(local_dir, exist_ok=True)
    return local_dir


def paint_poster(destination):
    """Create the poster at ``destination``, live or from the fallback."""
    try:
        from poster import render

        render(destination)
        print("poster painted live with Pillow")
    except ImportError:
        if not os.path.isfile(FALLBACK_IMAGE):
            fail("Pillow is missing and no pre-rendered entry.png is shipped")
        shutil.copyfile(FALLBACK_IMAGE, destination)
        print("Pillow missing; reused the pre-rendered entry.png")


def check_png(path):
    """Read ``path`` back and make sure it clears the bounty gate.

    Returns the file size in bytes.  Anything off — missing file, over
    the size cap, not a PNG, or the wrong dimensions — aborts the run.
    """
    if not os.path.isfile(path):
        fail("no output written at %s" % path)
    size = os.path.getsize(path)
    if size > SIZE_LIMIT:
        fail("entry.png too large: %d bytes (max %d)" % (size, SIZE_LIMIT))
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        fail("entry.png is not a PNG")
    # The IHDR chunk starts at byte 8; its width lives at bytes 16-19
    # and its height at bytes 20-23, both big-endian.
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(
            "entry.png is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    return size


def run():
    """Paint the poster, validate it, and report where it landed."""
    destination = os.path.join(pick_output_directory(), OUTPUT_NAME)
    paint_poster(destination)
    size = check_png(destination)
    print(
        "wrote %s (%d bytes, %dx%d PNG)"
        % (destination, size, EXPECTED_WIDTH, EXPECTED_HEIGHT)
    )


if __name__ == "__main__":
    run()
