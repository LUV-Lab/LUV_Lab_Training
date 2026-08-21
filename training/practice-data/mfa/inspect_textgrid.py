#!/usr/bin/env python3
"""Dump a Praat/MFA long-format TextGrid as a plain table.

    python3 inspect_textgrid.py practice-aligned.TextGrid
    python3 inspect_textgrid.py practice-aligned.TextGrid --tier phones
    python3 inspect_textgrid.py practice-aligned.TextGrid --tier phones --min-dur 0.3

This is a VIEWING AID, not a QC tool. It reports what is in the file and
makes no judgement about whether any interval is right or wrong -- finding
the misalignment is your job, and `--min-dur` only sorts the haystack.

Standard library only: it runs anywhere, with or without Praat installed.
Praat itself remains the better view when you have audio, because you can
see the interval against the spectrogram. Use this when you do not.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

NUM_RE = re.compile(r"=\s*([-\d.eE+]+)")
STR_RE = re.compile(r'=\s*"(.*)"\s*$')


def parse_textgrid(path: pathlib.Path) -> dict[str, list[tuple[float, float, str]]]:
    """Return {tier_name: [(xmin, xmax, label), ...]} for interval tiers.

    Deliberately forgiving: it keys off `name =`, `xmin =`, `xmax =`,
    `text =` lines rather than enforcing the full grammar, which is enough
    for the well-formed files an aligner writes.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    tiers: dict[str, list[tuple[float, float, str]]] = {}

    current_name: str | None = None
    in_header = True          # tier header, before its first interval
    pending: list[float] = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("name ="):
            m = STR_RE.search(stripped)
            current_name = m.group(1) if m else None
            if current_name is not None:
                tiers.setdefault(current_name, [])
            in_header = True
            pending = []
            continue

        if stripped.startswith("intervals ["):
            in_header = False
            pending = []
            continue

        if in_header:
            # tier-level xmin/xmax -- not an interval, skip
            continue

        if stripped.startswith("xmin =") or stripped.startswith("xmax ="):
            m = NUM_RE.search(stripped)
            if m:
                pending.append(float(m.group(1)))
            continue

        if stripped.startswith("text ="):
            m = STR_RE.search(stripped)
            label = m.group(1) if m else ""
            if current_name is not None and len(pending) >= 2:
                tiers[current_name].append((pending[0], pending[1], label))
            pending = []
            continue

    return tiers


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("textgrid", type=pathlib.Path)
    ap.add_argument("--tier", default=None,
                    help="show only this tier (default: all)")
    ap.add_argument("--min-dur", type=float, default=None,
                    help="show only intervals at least this long, in seconds")
    ap.add_argument("--max-dur", type=float, default=None,
                    help="show only intervals at most this long, in seconds")
    ap.add_argument("--labelled-only", action="store_true",
                    help="hide empty intervals")
    args = ap.parse_args()

    if not args.textgrid.exists():
        print(f"no such file: {args.textgrid}", file=sys.stderr)
        return 1

    tiers = parse_textgrid(args.textgrid)
    if not tiers:
        print("no interval tiers found -- is this a long-format TextGrid?",
              file=sys.stderr)
        return 1

    for name, intervals in tiers.items():
        if args.tier and name != args.tier:
            continue

        shown = []
        for i, (start, end, label) in enumerate(intervals, start=1):
            dur = end - start
            if args.min_dur is not None and dur < args.min_dur:
                continue
            if args.max_dur is not None and dur > args.max_dur:
                continue
            if args.labelled_only and not label.strip():
                continue
            shown.append((i, start, end, dur, label))

        total = sum(e - s for s, e, _ in intervals)
        print(f"\ntier {name!r}: {len(intervals)} intervals, "
              f"spanning {total:.3f} s, {len(shown)} shown")
        print(f"{'idx':>5}  {'xmin':>8}  {'xmax':>8}  {'dur':>7}  label")
        print("-" * 52)
        for i, start, end, dur, label in shown:
            print(f"{i:>5}  {start:>8.3f}  {end:>8.3f}  {dur:>7.3f}  {label}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
