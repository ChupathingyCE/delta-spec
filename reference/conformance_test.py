#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: MIT
"""conformance.py's own checks: python3 reference/conformance_test.py
(exit 0 when they all hold)."""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAG = bytes.fromhex("444c010202030000af")
# (delta_layout.c's facts and converter, run from a file: the facts of 11 to
# 45 a line each, or one record converted)
LAYOUT_TOOL = r"""
#include "delta_layout.h"
#include <stdio.h>
#include <stdlib.h>
static unsigned char in[20000], out[20000], extended[16];
int main(int argc, char **argv)
{
	if (argc == 1) {
		unsigned v; int k, b;
		for (v = 11; v <= 45; v++) {
			struct delta_layout l; delta_layout_built_in(v, &l);
			printf("%u %u %u %u %u %d %u %u %u |", v, l.settings_size, l.options_size, l.shield_effects_maximum,
				l.join_request_extra, l.join_request_version_at, l.header_extra, l.epoch_kind, l.rider_ejection_up);
			for (k = 1; k < 256; k++) if (delta_layout_drops(&l, (unsigned)k)) printf(" %d", k);
			printf(" |");
			for (b = 0; b < 8; b++) if (l.unit_part_size[b]) printf(" %d:%d:%d", b, l.unit_part_size[b], l.unit_part_at[b]);
			printf("\n");
		}
		return 0;
	} else {
		FILE *f = fopen(argv[1], "rb"); size_t size = fread(in, 1, sizeof(in), f); fclose(f);
		unsigned from_options = (unsigned)atoi(argv[2]), to_size = (unsigned)atoi(argv[3]), to_options = (unsigned)atoi(argv[4]);
		if (delta_layout_convert(in, size, from_options, out, to_size, to_options, extended)) return 2;
		f = fopen(argv[5], "wb"); fwrite(out, 1, to_size, f); fwrite(extended, 1, 16, f); fclose(f);
		return 0;
	}
}
"""
AT = {1: "after_up", 2: "last"}


def layout_checks(failures, folder):
    """layouts.json against delta_layout.c's built-in facts, and conformance.py's converter against its"""
    sys.path.insert(0, str(HERE))
    import conformance
    layouts = conformance.load_layouts()
    cc = next((shutil.which(name) for name in ("cc", "clang", "gcc") if shutil.which(name)), None)
    if not cc:
        print("conformance_test: no C compiler, layout checks against delta_layout.c skipped")
        return
    tool = Path(folder) / "layout_tool"
    (Path(folder) / "layout_tool.c").write_text(LAYOUT_TOOL)
    build = subprocess.run([cc, "-std=c99", "-I", str(HERE), str(HERE / "delta_layout.c"),
                            str(Path(folder) / "layout_tool.c"), "-o", str(tool)], capture_output=True, text=True)
    if build.returncode:
        failures.append((("build layout tool",), build.stderr))
        return
    for line in subprocess.run([str(tool)], capture_output=True, text=True, check=True).stdout.splitlines():
        head, drops, parts = line.split("|")
        v, size, options, shields, extra, at, header, epoch, ride = (int(x) for x in head.split())
        mine = conformance.layout_of(layouts, v)
        want = {"settings_size": size, "options_size": options, "shield_effects_maximum": shields,
                "join_request_extra": extra, "join_request_version_at": at if at >= 0 else None, "header_extra": header,
                "epoch_kind": epoch, "rider_ejection_up": ride, "dropped_messages": [int(x) for x in drops.split()],
                "unit_state_parts": [{"bit": int(b), "size": int(n), "at": AT[int(w)]}
                                     for b, n, w in (p.split(":") for p in parts.split())],
                "local_data_offset": 0x3320 + options, "trailing_size": size - 0x3320 - options - 4}
        got = {key: mine[key] for key in want}
        if got != want:
            failures.append((("layouts.json", str(v)), f"{got}\n!= delta_layout.c's {want}"))
    rng = random.Random(1124)
    cases = [(13120, 0x1C, 13200, 0x2C), (13136, 0x2C, 13200, 0x2C), (13200, 0x2C, 13120, 0x1C),
             (13200, 0x2C, 13136, 0x2C), (13120, 0x1C, 13136, 0x2C), (13244, 0x58, 13200, 0x2C),
             (13200, 0x2C, 13244, 0x58)]
    for from_size, from_options, to_size, to_options in cases:
        record = bytes(rng.randrange(256) for _ in range(from_size))
        source, target = Path(folder) / "in.bin", Path(folder) / "out.bin"
        source.write_bytes(record)
        subprocess.run([str(tool), str(source), str(from_options), str(to_size), str(to_options), str(target)], check=True)
        theirs = target.read_bytes()
        out, extended = conformance.convert_record(record, from_options, to_size, to_options)
        if out + extended != theirs:
            failures.append((("convert", str(from_size), str(to_size)), "conformance.py and delta_layout.c differ"))


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
        layout_checks(failures, folder)
        record = Path(folder) / "32.bin"
        record.write_bytes(bytes(13120))
        expect(0, "record", "32", str(record))
        expect(1, "record", "44", str(record))
        converted = Path(folder) / "44.bin"
        expect(0, "convert", "32", "44", str(record), str(converted))
        expect(0, "record", "44", str(converted))
        expect(0, "convert", "32", "44", str(record), str(Path(folder) / "again.bin"), "--expect", str(converted))
        wrong = bytearray(converted.read_bytes())
        wrong[0x3320 + 0x1E] = 0
        (Path(folder) / "wrong.bin").write_bytes(bytes(wrong))
        expect(1, "convert", "32", "44", str(record), str(Path(folder) / "again.bin"), "--expect",
               str(Path(folder) / "wrong.bin"))
        expect(1, "layout", "10")
        expect(0, "layout", "45")
    for args, output in failures:
        print(f"conformance_test: {' '.join(args)} gave the wrong answer:\n{output}")
    print("conformance_test: " + ("failed" if failures else "ok"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
