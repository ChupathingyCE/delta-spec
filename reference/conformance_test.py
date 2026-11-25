#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: MIT
"""conformance.py's own checks: python3 reference/conformance_test.py
(exit 0 when they all hold)."""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAG = bytes.fromhex("444c010202030000af")


def run(*args):
    return subprocess.run([sys.executable, str(HERE / "conformance.py"), *args], capture_output=True, text=True)


def main():
    failures = []

    def expect(code, *args):
        result = run(*args)
        if result.returncode != code:
            failures.append((args, result.stdout))

    plain = bytes.fromhex("2c000100") + bytes(13)
    expect(0, "advert", (plain + bytes(9)).hex())
    expect(0, "advert", (plain + TAG).hex())
    # (a layout 2 tag beside the old layout's claim: flag 0x04, major 1 at
    # byte 3, a wire ID after it, which released builds join as our wire)
    old = bytes.fromhex("2c000501") + b"chupa-44a" + bytes(4)
    expect(1, "advert", (old + TAG).hex())
    expect(1, "advert", (old + bytes(9)).hex())
    # (a kind at byte 3 with zeros after it is fine: a dedicated SWAT game)
    expect(0, "advert", (bytes.fromhex("2c000501") + bytes(13) + TAG).hex())
    with tempfile.TemporaryDirectory() as folder:
        empty = Path(folder) / "empty.txt"
        empty.write_text("# nothing\n")
        expect(1, "check", "--host", str(empty))
        expect(1, "check", str(empty))
    for args, output in failures:
        print(f"conformance_test: {' '.join(args)} gave the wrong answer:\n{output}")
    print("conformance_test: " + ("failed" if failures else "ok"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
