#!/usr/bin/env python3
"""Generate the acoustic-measurement practice materials (Module 2).

Writes, into this script's own directory:

  formants-practice.csv        42 synthetic formant measurements over two
                               synthetic speakers, carrying FOUR SEEDED ITEMS
                               (three tracker errors and one item that LOOKS
                               like an error and is not)
  measurement-log.csv          empty template for the hand-measurement
                               exercise

EVERYTHING HERE IS SYNTHETIC. The values are drawn around textbook adult
F1/F2 targets with deterministic jitter; no real participant recording or
measurement is used, and none may be. See people/training/data-ethics-for-ras.md.

These outputs are MACHINE-WRITTEN. Per the lab's provenance norm, do not
hand-edit them -- change this script and re-run:

    python3 make_practice_data.py

Standard library only, by design: an RA must be able to regenerate the
practice set on any machine without installing anything.
"""

from __future__ import annotations

import csv
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
SEED = 20260805

# --------------------------------------------------------------------------
# Reference targets, in Hz: (F1, F2, F3) per vowel, per speaker group.
#
# STATUS: ASSUMPTION -- these are conventional textbook adult values used to
# generate plausible practice data. They are NOT a lab measurement standard
# and NOTHING in this repo ratifies them. An RA can check the shape of these
# bands independently against the Peterson & Barney (1952) measurements
# distributed as `phonTools::pb52` in R (ledger keys `peterson1952control`,
# `barreda2023phontools`, both VERIFIED).
# --------------------------------------------------------------------------

TARGETS = {
    "F": {  # higher-formant speaker (synthetic speaker P01)
        "IY": (400, 2650, 3050),
        "IH": (490, 2200, 2900),
        "EH": (650, 2000, 2800),
        "AE": (860, 1900, 2750),
        "AA": (900, 1300, 2700),
        "AO": (760, 1100, 2700),
        "UW": (420, 1100, 2600),
    },
    "M": {  # lower-formant speaker (synthetic speaker P02)
        "IY": (320, 2200, 2900),
        "IH": (420, 1900, 2600),
        "EH": (560, 1750, 2500),
        "AE": (660, 1700, 2450),
        "AA": (720, 1200, 2500),
        "AO": (620, 1000, 2450),
        "UW": (350, 1050, 2350),
    },
}

# (word, vowel, following_phone)
WORDS = [
    ("league",  "IY", "G"),
    ("people",  "IY", "P"),
    ("keep",    "IY", "P"),
    ("big",     "IH", "G"),
    ("still",   "IH", "L"),
    ("did",     "IH", "D"),
    ("said",    "EH", "D"),
    ("check",   "EH", "K"),
    ("left",    "EH", "F"),
    ("back",    "AE", "K"),
    ("that",    "AE", "T"),
    ("hand",    "AE", "N"),   # pre-nasal -- see SEEDED ITEM 4
    ("job",     "AA", "B"),
    ("stop",    "AA", "P"),
    ("watched", "AA", "CH"),
    ("walk",    "AO", "K"),
    ("coffee",  "AO", "F"),
    ("talk",    "AO", "K"),
    ("school",  "UW", "L"),
    ("two",     "UW", "sp"),
    ("food",    "UW", "D"),
]

SPEAKERS = [("P01", "F"), ("P02", "M")]

# --------------------------------------------------------------------------
# SEEDED ITEMS, keyed by (speaker, word). Each maps to an override dict.
# Do not "fix" these -- they are the exercise.
#
#   1. P01 "keep"    F2 has locked onto F3 and F3 onto F4: the tracker
#                    skipped a formant. F1 is untouched, which is the tell.
#   2. P02 "people"  F1 is impossible for a high front vowel -- a ceiling /
#                    tracking failure at the bottom of the spectrum.
#   3. P01 "did"     duration below the lab's documented 0.05 s floor; the
#                    values are junk because there is not enough vowel to
#                    measure. Mechanically excluded regardless of values.
#   4. BOTH "hand"   NOT AN ERROR. Pre-nasal /ae/ is raised (lower F1) and
#                    fronted (higher F2) in BOTH speakers, in the same
#                    direction. That is a systematic context effect -- the
#                    short-a conditioning the lab actually measures -- not
#                    tracker noise. The correct action is to keep it and
#                    code the context.
# --------------------------------------------------------------------------

OVERRIDES = {
    ("P01", "keep"):   {"F1": 405, "F2": 3050, "F3": 3900},
    ("P02", "people"): {"F1": 715, "F2": 2150, "F3": 2880},
    ("P01", "did"):    {"dur": 0.031, "F1": 545, "F2": 2380, "F3": 2960},
    ("P01", "hand"):   {"F1": 700, "F2": 2180},
    ("P02", "hand"):   {"F1": 570, "F2": 1950},
}


def main() -> None:
    rng = random.Random(SEED)
    rows = []

    for speaker, group in SPEAKERS:
        n = 0
        for word, vowel, following in WORDS:
            n += 1
            f1_t, f2_t, f3_t = TARGETS[group][vowel]

            # Deterministic jitter: +/- ~4% on formants, plausible durations.
            f1 = round(f1_t * rng.uniform(0.96, 1.04))
            f2 = round(f2_t * rng.uniform(0.96, 1.04))
            f3 = round(f3_t * rng.uniform(0.97, 1.03))
            dur = round(rng.uniform(0.065, 0.175), 3)

            over = OVERRIDES.get((speaker, word), {})
            f1 = over.get("F1", f1)
            f2 = over.get("F2", f2)
            f3 = over.get("F3", f3)
            dur = over.get("dur", dur)

            rows.append({
                "token_id": f"{speaker}-{n:03d}",
                "speaker": speaker,
                "speaker_group": group,
                "word": word,
                "vowel": vowel,
                "stress": 1,
                "dur_s": f"{dur:.3f}",
                "F1_Hz": f1,
                "F2_Hz": f2,
                "F3_Hz": f3,
                "following_phone": following,
            })

    out = HERE / "formants-practice.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote formants-practice.csv      ({len(rows)} tokens, "
          f"{len(SPEAKERS)} speakers)")

    # Empty log for the hand-measurement exercise.
    log = HERE / "measurement-log.csv"
    with log.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "token_id", "measured_by", "date", "synth_F1_Hz", "synth_F2_Hz",
            "measured_F1_Hz", "measured_F2_Hz", "abs_diff_F1_Hz",
            "abs_diff_F2_Hz", "within_tolerance", "notes",
        ])
    print("wrote measurement-log.csv        (header only -- you fill it in)")


if __name__ == "__main__":
    main()
