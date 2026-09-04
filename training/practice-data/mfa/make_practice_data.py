#!/usr/bin/env python3
"""Generate the forced-alignment practice materials (Module 3).

Writes, into this script's own directory:

  practice-aligned.TextGrid   an MFA-style long-format TextGrid ("words" +
                              "phones" tiers) carrying THREE SEEDED DEFECTS.
                              Conventions follow MFA 3.x defaults: silence is
                              UNLABELLED on both tiers (cleanup_textgrids
                              strips silence labels; there is no "sp" phone in
                              3.x), words are lowercase, and phone labels are
                              ARPABET with stress digits as the
                              english_us_arpa models emit. An english_mfa
                              alignment uses IPA-style symbols instead -- the
                              structure is identical, the symbols are not.
  practice-transcript.lab     the orthographic transcript the alignment claims
                              to correspond to
  oov-report.txt              an out-of-vocabulary report of the kind an
                              aligner emits during validation
  alignment-coverage.csv      per-file coverage statistics for the
                              sparse-alignment detection exercise
  alignment-analysis-practice.csv
                              an MFA-style alignment-analysis table (one row
                              per utterance) for the alignment-analysis
                              reading exercise

EVERYTHING HERE IS SYNTHETIC. No real participant recording, transcript, or
metadata is used, and none may be. See people/training/data-ethics-for-ras.md.

These outputs are MACHINE-WRITTEN. Per the lab's provenance norm, do not
hand-edit them -- change this script and re-run:

    python3 make_practice_data.py

Standard library only, by design: an RA must be able to regenerate the
practice set on any machine without installing anything.
"""

from __future__ import annotations

import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# The utterance. Orthographic word -> ARPABET phones (CMU-style, stress digit
# on vowels). Durations in seconds.
#
# SEEDED DEFECTS (do not "fix" them here -- they are the exercise):
#   D1  word 5 "iggles" is out-of-vocabulary and aligns to a single 1.550 s
#       `spn` interval that swallows the surrounding speech.
#   D2  word 14 "watched": the AA1 nucleus is 0.710 s, far above any
#       plausible conversational vowel and above the 0.5 s max_duration_sec
#       filter one documented project applies (see Module 2).
#   D3  word 15 "the" is crushed to 0.018 s total. D2 and D3 are ONE error
#       region, not two: time over-assigned to the AA1 has to come out of a
#       neighbour. Misalignments come in compensating pairs.
# --------------------------------------------------------------------------

LEADING_SIL = 0.35
TRAILING_SIL = 0.40

# (word, [(phone, duration), ...], pause_after_seconds_or_0)
UTTERANCE = [
    ("MY",      [("M", 0.070), ("AY1", 0.155)], 0.0),
    ("COUSIN",  [("K", 0.065), ("AH1", 0.090), ("Z", 0.060), ("AH0", 0.045),
                 ("N", 0.060)], 0.0),
    ("WORE",    [("W", 0.060), ("AO1", 0.145), ("R", 0.075)], 0.090),
    ("HER",     [("HH", 0.050), ("ER0", 0.085)], 0.0),
    # ---- D1: out-of-vocabulary word swallowed by a single spn interval ----
    ("IGGLES",  [("spn", 1.550)], 0.0),
    ("JERSEY",  [("JH", 0.075), ("ER1", 0.120), ("Z", 0.055), ("IY0", 0.100)], 0.0),
    ("TO",      [("T", 0.055), ("UW1", 0.080)], 0.0),
    ("THE",     [("DH", 0.040), ("AH0", 0.045)], 0.0),
    ("GAME",    [("G", 0.060), ("EY1", 0.170), ("M", 0.070)], 0.0),
    ("LAST",    [("L", 0.065), ("AE1", 0.140), ("S", 0.095), ("T", 0.045)], 0.0),
    ("NIGHT",   [("N", 0.060), ("AY1", 0.175), ("T", 0.050)], 0.120),
    ("AND",     [("AE1", 0.075), ("N", 0.050), ("D", 0.035)], 0.0),
    ("WE",      [("W", 0.055), ("IY1", 0.105)], 0.0),
    # ---- D2: implausibly long stressed nucleus ----
    ("WATCHED", [("W", 0.060), ("AA1", 0.710), ("CH", 0.080), ("T", 0.045)], 0.0),
    # ---- D3: word crushed to near-zero, compensating for D2 ----
    ("THE",     [("DH", 0.009), ("AH0", 0.009)], 0.0),
    ("WHOLE",   [("HH", 0.055), ("OW1", 0.150), ("L", 0.070)], 0.0),
    ("LEAGUE",  [("L", 0.065), ("IY1", 0.135), ("G", 0.060)], 0.0),
    ("PLAYOFF", [("P", 0.055), ("L", 0.050), ("EY1", 0.145), ("AO2", 0.130),
                 ("F", 0.090)], 0.0),
]

OOV_WORDS = ["iggles"]


def r(x: float) -> float:
    """Round to millisecond precision so the two tiers agree exactly."""
    return round(x + 1e-12, 3)


def build_tiers():
    """Return (word_intervals, phone_intervals, xmax).

    Each interval is (xmin, xmax, label). Silence is UNLABELLED on BOTH
    tiers, which is what MFA 3.x emits by default (cleanup_textgrids=True
    strips silence labels; "sp" does not exist as a phone in 3.x). Word
    labels are lowercase, as MFA's normalization produces.
    """
    words: list[tuple[float, float, str]] = []
    phones: list[tuple[float, float, str]] = []

    t = 0.0
    words.append((r(t), r(t + LEADING_SIL), ""))
    phones.append((r(t), r(t + LEADING_SIL), ""))
    t += LEADING_SIL

    for word, phone_list, pause_after in UTTERANCE:
        w_start = t
        for phone, dur in phone_list:
            phones.append((r(t), r(t + dur), phone))
            t += dur
        words.append((r(w_start), r(t), word.lower()))

        if pause_after > 0:
            words.append((r(t), r(t + pause_after), ""))
            phones.append((r(t), r(t + pause_after), ""))
            t += pause_after

    words.append((r(t), r(t + TRAILING_SIL), ""))
    phones.append((r(t), r(t + TRAILING_SIL), ""))
    t += TRAILING_SIL

    return words, phones, r(t)


def write_textgrid(path: pathlib.Path, words, phones, xmax: float) -> None:
    """Write Praat long ("ooTextFile") format -- what MFA emits and praatio reads."""
    lines: list[str] = []
    a = lines.append

    a('File type = "ooTextFile"')
    a('Object class = "TextGrid"')
    a("")
    a("xmin = 0 ")
    a(f"xmax = {xmax} ")
    a("tiers? <exists> ")
    a("size = 2 ")
    a("item []: ")

    for tier_index, (name, intervals) in enumerate(
        [("words", words), ("phones", phones)], start=1
    ):
        a(f"    item [{tier_index}]:")
        a('        class = "IntervalTier" ')
        a(f'        name = "{name}" ')
        a("        xmin = 0 ")
        a(f"        xmax = {xmax} ")
        a(f"        intervals: size = {len(intervals)} ")
        for i, (start, end, label) in enumerate(intervals, start=1):
            a(f"        intervals [{i}]:")
            a(f"            xmin = {start} ")
            a(f"            xmax = {end} ")
            a(f'            text = "{label}" ')

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_transcript(path: pathlib.Path) -> None:
    """The .lab transcript an aligner consumes, paired 1:1 with an audio file."""
    text = " ".join(word.lower() for word, _, _ in UTTERANCE)
    path.write_text(text + "\n", encoding="utf-8")


def write_oov_report(path: pathlib.Path) -> None:
    path.write_text("\n".join(OOV_WORDS) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# alignment-coverage.csv -- the sparse-alignment detection exercise.
#
# Shape and failure mode are modelled on a real, documented QC event in the
# lab's own corpus work: a shipped alignment whose words tier carried a small
# fraction of the words actually spoken and stopped partway through each
# recording, so it was rejected and re-aligned from the verbatim transcripts.
# The corpus, the project and the source memo are named in the lab's internal
# records, not here. The NUMBERS BELOW ARE SYNTHETIC; only the failure
# pattern is drawn from that event.
#
# Seeded bad files: PX03, PX07, PX11.
# --------------------------------------------------------------------------

COVERAGE_ROWS = [
    # file_id, audio_duration_min, n_words_aligned, last_word_end_s
    ("PX01", 62.4, 8_233, 3_735.1),
    ("PX02", 55.1, 7_046, 3_299.4),
    ("PX03", 71.8, 402, 1_690.2),     # seeded: sparse + stops partway
    ("PX04", 48.6, 6_891, 2_910.0),
    ("PX05", 66.2, 9_120, 3_961.7),
    ("PX06", 59.9, 7_534, 3_580.3),
    ("PX07", 64.5, 118, 1_402.9),     # seeded: sparse + stops partway
    ("PX08", 52.3, 6_105, 3_120.8),
    ("PX09", 70.1, 9_884, 4_190.6),
    ("PX10", 45.7, 5_388, 2_733.9),
    ("PX11", 58.4, 479, 1_284.5),     # seeded: sparse + stops partway
    ("PX12", 61.0, 7_812, 3_648.2),
]


# --------------------------------------------------------------------------
# alignment-analysis-practice.csv -- reading an MFA-style alignment analysis.
#
# Column STRUCTURE mirrors the alignment-analysis table MFA can produce beside
# aligned TextGrids: file, begin, end, speaker, overall_log_likelihood,
# speech_log_likelihood, phone_duration_deviation, snr.
#
# EVERY VALUE BELOW IS INVENTED for this exercise. Nothing here is derived,
# rounded, or scaled from any real analysis of any real corpus, and no real
# alignment analysis may ever be committed to this repository -- those tables
# carry per-speaker identifiers and acoustic metadata about real people.
# The absolute scales are illustrative; the PATTERNS are the lesson.
#
# Seeded patterns:
#   P1  interview04 (spk04): metric columns EMPTY on both rows -- the analysis
#       produced nothing for that file. Loudest signal in the table.
#   P2  interview06 utterance 2: phone_duration_deviation 9.8, far above the
#       rest of the cohort -- the best "look at this file" flag.
#   P3  interview02 (spk02): snr 4.6 / 5.1, far below the cohort, with mildly
#       worse deviation -- recording quality, not aligner failure.
# --------------------------------------------------------------------------

ANALYSIS_ROWS = [
    # file, begin, end, speaker, overall_ll, speech_ll, phone_dur_dev, snr
    ("interview01", 12.400, 47.900, "spk01", -34.7, -32.1, 1.4, 22.8),
    ("interview01", 51.200, 88.650, "spk01", -35.9, -33.4, 1.1, 23.5),
    ("interview02", 8.900, 44.300, "spk02", -41.2, -39.6, 1.9, 4.6),
    ("interview02", 47.100, 82.750, "spk02", -40.8, -38.9, 2.2, 5.1),
    ("interview03", 15.600, 52.050, "spk03", -33.1, -30.7, 1.6, 25.4),
    ("interview03", 55.300, 91.800, "spk03", -34.4, -31.9, 1.3, 24.9),
    ("interview04", 10.200, 46.400, "spk04", None, None, None, None),
    ("interview04", 49.700, 85.100, "spk04", None, None, None, None),
    ("interview05", 9.500, 45.850, "spk05", -36.2, -33.8, 2.0, 19.7),
    ("interview05", 48.600, 84.200, "spk05", -35.5, -33.0, 1.7, 20.3),
    ("interview06", 13.800, 50.100, "spk06", -34.9, -32.6, 1.5, 21.6),
    ("interview06", 53.400, 89.950, "spk06", -38.6, -36.2, 9.8, 21.1),
    ("interview07", 11.300, 48.700, "spk07", -33.8, -31.5, 2.6, 26.7),
    ("interview07", 52.000, 87.400, "spk07", -34.2, -31.8, 0.9, 27.2),
]


def write_analysis(path: pathlib.Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "file",
                "begin",
                "end",
                "speaker",
                "overall_log_likelihood",
                "speech_log_likelihood",
                "phone_duration_deviation",
                "snr",
            ]
        )
        for row in ANALYSIS_ROWS:
            w.writerow(["" if v is None else v for v in row])


def write_coverage(path: pathlib.Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(
            ["file_id", "audio_duration_min", "n_words_aligned", "last_word_end_s"]
        )
        for row in COVERAGE_ROWS:
            w.writerow(row)


def main() -> None:
    words, phones, xmax = build_tiers()

    # Internal consistency guard: every phone must nest inside a word or a
    # silence, and the tiers must span identical time. If this ever fails the
    # generator is broken, not the student.
    assert words[0][0] == phones[0][0] == 0.0
    assert words[-1][1] == phones[-1][1] == xmax
    for i in range(len(words) - 1):
        assert abs(words[i][1] - words[i + 1][0]) < 1e-9, "gap in words tier"
    for i in range(len(phones) - 1):
        assert abs(phones[i][1] - phones[i + 1][0]) < 1e-9, "gap in phones tier"

    write_textgrid(HERE / "practice-aligned.TextGrid", words, phones, xmax)
    write_transcript(HERE / "practice-transcript.lab")
    write_oov_report(HERE / "oov-report.txt")
    write_coverage(HERE / "alignment-coverage.csv")
    write_analysis(HERE / "alignment-analysis-practice.csv")

    print(f"wrote practice-aligned.TextGrid  ({len(words)} word intervals, "
          f"{len(phones)} phone intervals, xmax={xmax}s)")
    print("wrote practice-transcript.lab")
    print("wrote oov-report.txt")
    print(f"wrote alignment-coverage.csv     ({len(COVERAGE_ROWS)} files)")
    print(f"wrote alignment-analysis-practice.csv ({len(ANALYSIS_ROWS)} rows)")


if __name__ == "__main__":
    main()
