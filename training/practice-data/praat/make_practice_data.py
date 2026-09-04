#!/usr/bin/env python3
"""Generate the acoustic-measurement practice materials (Module 2).

Writes, into this script's own directory:

  formants-practice.csv        42 synthetic formant measurements over two
                               synthetic speakers, carrying FOUR SEEDED ITEMS
                               across five rows (three tracker errors and one
                               item, present in BOTH speakers, that LOOKS like
                               an error and is not)
  measurement-log.csv          empty template for the hand-measurement
                               exercise
  practice-vowels.wav          three steady vowels separated by silence
  practice-vot.wav             two CV tokens, long-lag vs short-lag VOT
  practice-fricatives.wav      three VCV tokens: voiceless sibilant, lower
                               sibilant, voiced fricative
  practice-connected.wav       a short connected sequence -- vowel, fricative,
                               vowel, nasal murmur, stop (closure, burst,
                               aspiration), vowel -- between silences: eight
                               speech segments, ten segments counting the two
                               silences, NINE boundaries, one of them
                               deliberately GRADUAL (vowel into nasal)
  segmentation-key.csv         ground truth for the four .wav files, ONE ROW
                               PER BOUNDARY: time, the labels either side, the
                               boundary type, the tolerance the answer key
                               grades against, and (for gradual boundaries)
                               the window over which the energy crosses over

EVERYTHING HERE IS SYNTHETIC. The values are drawn around textbook adult
F1/F2 targets with deterministic jitter; no real participant recording or
measurement is used, and none may be. See people/training/data-ethics-for-ras.md.

These outputs are MACHINE-WRITTEN. Per the lab's provenance norm, do not
hand-edit them -- change this script and re-run:

    python3 make_practice_data.py

Standard library only, by design: an RA must be able to regenerate the
practice set on any machine without installing anything. The companion
`verify_practice_data.py` is NOT standard library (it needs `praat-parselmouth`,
i.e. Praat's own analysis engine) and is what checks that the audio written
here actually measures the way the answer key says it does.

CHANGE RECORD
  2026-08-28  audio fixtures added (AUDIO_SEED = 20260828).
  2026-09-02  audio synthesis rebuilt after the 2026-08-30 red-team cold read
              (people/training/reviews/redteam-praat-ready-check-2026-08-30.md,
              path updated when the review left inbox/; findings B2, B3,
              M2, M3, M5, M7, m3, m4). What changed and why:
              * Voiced source: the old smooth-pulse source had a spectral
                tilt of roughly -25 to -35 dB/octave, so F2/F3 fell below
                Praat's 50 dB spectrogram floor and the Burg tracker fitted a
                spurious low pole (B3). It is now an impulse train through a
                one-pole low-pass (corner SOURCE_TILT_CORNER_HZ), i.e. about
                -6 dB/octave -- a textbook radiated-speech tilt. Tuned BY
                MEASUREMENT with Praat 6.1.38 via parselmouth on 2026-09-02:
                the setting that recovers every vowel target within the
                module's ratified +/-50 Hz (F1) / +/-100 Hz (F2) at both the
                5,000 Hz and 5,500 Hz ceilings, across every F0 used here.
              * Two fixed higher formants (HIGHER_FORMANTS) added to every
                vowel. With only three resonances in the signal, a
                five-formant analysis has two poles with nothing real to
                fit, and it put them between F1 and F2. Real vowels have
                F4 and F5; so do these now.
              * The voiced fricative Z: noise and voicing are each
                normalised to unit RMS BEFORE mixing (the old mix left the
                voicing about 21 dB below the noise -- inaudible and
                undetectable, B2), and the vowel-to-Z / Z-to-vowel joins are
                40 ms crossfades recorded as GRADUAL with a window, so the
                answer key's "a ramp, not a step" is true by construction.
              * Joins between two non-silent segments overlap by JOIN_S with
                a linear crossfade instead of each segment fading to an exact
                digital zero (M7): there is no longer a zero-amplitude notch
                at every boundary to "find". Fades to/from silence are
                EDGE_RAMP_S. Bursts still start from silence with no on-ramp.
              * The key is now one row per BOUNDARY, not per segment, so a
                shared boundary carries exactly one tolerance (m3). Boundaries
                with no acoustic correlate (silence into a silent closure) are
                `not-markable`; burst-into-aspiration is `not-graded` (M2).
              * The formant CSV and its seeded items are untouched: SEED and
                main() are unchanged, so formants-practice.csv and
                measurement-log.csv regenerate byte-identically.
"""

from __future__ import annotations

import csv
import math
import pathlib
import random
import struct
import wave

HERE = pathlib.Path(__file__).resolve().parent
SEED = 20260805

# Audio uses its OWN generator instance and its OWN seed, so that adding the
# .wav fixtures cannot perturb the CSV values above. Change either seed and
# the corresponding answer key stops matching -- change both together or
# neither (lab fixture rule).
AUDIO_SEED = 20260828
SR = 22050

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
# Do not "fix" these -- they are the exercise. Four items, five rows: item 4
# is present in both speakers on purpose.
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


# ==========================================================================
# AUDIO FIXTURES -- synthetic speech-like signals for the segmentation and
# hand-measurement exercises (Module 2).
#
# EVERYTHING HERE IS SYNTHESIZED FROM SCRATCH. No recording of any kind is
# read, and no participant audio may ever be placed in this directory.
#
# The synthesizer is a Klatt-style cascade of two-pole resonators driven by
# a tilted impulse train (voiced) or by white noise (voiceless) -- standard
# library only (math, wave, random, struct), deterministic under AUDIO_SEED.
#
# The fixture "speaker" is the lower-formant group (TARGETS["M"], F0 about
# 108-120 Hz), so the module's ratified 5,000 Hz adult male-range ceiling is
# the one to measure these files with. The vowels in practice-vowels.wav are
# therefore the same vowels the formant exercise teaches, and
# verify_practice_data.py checks that Praat measures them back.
# ==========================================================================

# Synthesis settings that were TUNED BY MEASUREMENT on 2026-09-02 (see the
# change record above). STATUS: ASSUMPTION about what a plausible synthetic
# speaker looks like -- nothing here is a lab measurement standard. Changing
# any of them invalidates verification-report.md until the verifier is re-run.
SOURCE_TILT_CORNER_HZ = 150          # one-pole low-pass on the impulse train: ~-6 dB/oct above this
VOWEL_BANDWIDTHS = (60, 90, 120)     # B1, B2, B3 for every vowel
HIGHER_FORMANTS = ((3400, 120), (4200, 150))   # (F4, B4), (F5, B5): fixed for the fixture speaker
FRICATIVE_VOICING_DB = 3.0           # voicing RMS relative to frication RMS in the voiced fricative
JOIN_S = 0.004                       # crossfade overlap at an ABRUPT join between two non-silent segments
EDGE_RAMP_S = 0.004                  # fade length into / out of digital silence


def _resonator(x, f, bw):
    """One two-pole formant resonator at f Hz with bandwidth bw Hz."""
    c = -math.exp(-2 * math.pi * bw / SR)
    b = 2 * math.exp(-math.pi * bw / SR) * math.cos(2 * math.pi * f / SR)
    a = 1 - b - c
    out = [0.0] * len(x)
    y1 = y2 = 0.0
    for i, sample in enumerate(x):
        v = a * sample + b * y1 + c * y2
        out[i] = v
        y2, y1 = y1, v
    return out


def _impulse_train(n, f0, rng, jitter=0.02):
    """One unit impulse per glottal period, with slight period jitter."""
    out = [0.0] * n
    pos = 0.0
    while pos < n:
        out[int(pos)] = 1.0
        pos += SR / f0 * (1 + rng.uniform(-jitter, jitter))
    return out


def _tilt(x, corner_hz):
    """One-pole low-pass: flat below corner_hz, about -6 dB/octave above it."""
    r = math.exp(-2 * math.pi * corner_hz / SR)
    out = [0.0] * len(x)
    y = 0.0
    for i, sample in enumerate(x):
        y = (1 - r) * sample + r * y
        out[i] = y
    return out


def _voiced_source(n, f0, rng):
    """Glottal source: tilted impulse train (see the 2026-09-02 change record)."""
    return _tilt(_impulse_train(n, f0, rng), SOURCE_TILT_CORNER_HZ)


def _noise(n, rng):
    return [rng.uniform(-1, 1) for _ in range(n)]


def _norm(sig, amp):
    """Peak-normalise to amp."""
    peak = max(1e-9, max(abs(v) for v in sig))
    return [v / peak * amp for v in sig]


def _rms_norm(sig, level):
    """RMS-normalise to level -- used so two components mix at a KNOWN ratio."""
    rms = max(1e-9, math.sqrt(sum(v * v for v in sig) / max(1, len(sig))))
    return [v / rms * level for v in sig]


def _vowel(dur, f0, formants, rng, amp=1.0):
    sig = _voiced_source(int(dur * SR), f0, rng)
    for f, bw in tuple(formants) + HIGHER_FORMANTS:
        sig = _resonator(sig, f, bw)
    return _norm(sig, amp)


def _murmur(dur, f0, rng, amp=0.5):
    """Nasal-like murmur: low first resonance, weak and damped higher ones."""
    sig = _voiced_source(int(dur * SR), f0, rng)
    for f, bw in ((250, 90), (1000, 220), (2200, 300)):
        sig = _resonator(sig, f, bw)
    return _norm(sig, amp)


def _fricative(dur, f, bw, amp, rng, voiced_f0=None):
    n = int(dur * SR)
    sig = _rms_norm(_resonator(_noise(n, rng), f, bw), 1.0)
    if voiced_f0:
        voicing = _voiced_source(n, voiced_f0, rng)
        for vf, vbw in ((300, 120), (1000, 300)):
            voicing = _resonator(voicing, vf, vbw)
        voicing = _rms_norm(voicing, 10 ** (FRICATIVE_VOICING_DB / 20))
        sig = [a + b for a, b in zip(sig, voicing)]
    return _norm(sig, amp)


def _burst(rng, amp=0.9):
    sig = _resonator(_noise(int(0.006 * SR), rng), 1800, 900)
    return _norm(sig, amp)


def _aspiration(dur, rng, amp=0.35):
    sig = _resonator(_noise(int(dur * SR), rng), 1500, 1000)
    return _norm(sig, amp)


def _silence(dur):
    return [0.0] * int(dur * SR)


def _write_wav(path, sig):
    sig = _norm(sig, 0.85)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, v)) * 32767)) for v in sig
        ))


SILENT_LABELS = {"sil", "closure"}


class Track:
    """Accumulates segments and remembers exactly where each boundary is.

    Boundary bookkeeping is the point of this class: the generator knows the
    ground truth by construction, so the answer key never depends on anyone
    measuring the output. One key row per boundary.

    Joins: silence <-> sound boundaries get an EDGE_RAMP_S fade (except a
    burst, which starts from silence with no on-ramp -- that is what a burst
    is); sound <-> sound boundaries are crossfaded over `overlap_s` (default
    JOIN_S), and the recorded boundary time is the MIDPOINT of the overlap,
    where the two segments carry equal weight. A long overlap is a GRADUAL
    boundary and the key records the whole window, because the honest answer
    to "where does the vowel end" there is "somewhere in this window".
    """

    def __init__(self, name):
        self.name = name
        self.samples = []
        self.last_label = None
        self.boundaries = []

    def add(self, label, sig, boundary="abrupt", tol_ms=20, note="",
            overlap_s=None, onset_ramp=True):
        silent = label in SILENT_LABELS
        sig = list(sig)
        k_edge = int(EDGE_RAMP_S * SR)
        window = ("", "")

        if self.last_label is None:
            if not silent and onset_ramp:
                for i in range(min(k_edge, len(sig))):
                    sig[i] *= i / k_edge
            self.samples.extend(sig)
            self.last_label = label
            return

        prev_silent = self.last_label in SILENT_LABELS

        if silent and prev_silent:
            t = len(self.samples) / SR
            self.samples.extend(sig)
        elif silent:
            # fade the previous (non-silent) segment's tail out to zero
            for i in range(min(k_edge, len(self.samples))):
                self.samples[-1 - i] *= i / k_edge
            t = len(self.samples) / SR
            self.samples.extend(sig)
        elif prev_silent:
            if onset_ramp:
                for i in range(min(k_edge, len(sig))):
                    sig[i] *= i / k_edge
            t = len(self.samples) / SR
            self.samples.extend(sig)
        else:
            k = int((JOIN_S if overlap_s is None else overlap_s) * SR)
            head = self.samples[-k:]
            del self.samples[len(self.samples) - k:]
            overlap_start = len(self.samples) / SR
            blended = [head[i] * (1 - i / k) + sig[i] * (i / k) for i in range(k)]
            self.samples.extend(blended)
            self.samples.extend(sig[k:])
            overlap_end = overlap_start + k / SR
            t = (overlap_start + overlap_end) / 2
            if boundary == "gradual":
                window = (f"{overlap_start:.4f}", f"{overlap_end:.4f}")
                note = note or "energy crosses over inside the window; key time is its midpoint"

        self.boundaries.append({
            "file": self.name,
            "boundary_index": len(self.boundaries) + 1,
            "time_s": f"{t:.4f}",
            "left_label": self.last_label,
            "right_label": label,
            "boundary_type": boundary,
            "tolerance_ms": "" if boundary in ("not-markable", "not-graded") else tol_ms,
            "window_start_s": window[0],
            "window_end_s": window[1],
            "note": note,
        })
        self.last_label = label


def build_audio():
    """Write the four .wav fixtures; return the ground-truth key rows."""
    rng = random.Random(AUDIO_SEED)
    key = []

    m = TARGETS["M"]

    def formants(vowel):
        return tuple(zip(m[vowel], VOWEL_BANDWIDTHS))

    # ---- 1. isolated vowels: the easiest segmentation task ----------------
    t = Track("practice-vowels.wav")
    t.add("sil", _silence(0.250))
    t.add("IY", _vowel(0.400, 118, formants("IY"), rng), "abrupt", 20, "silence into vowel")
    t.add("sil", _silence(0.300), "abrupt", 20, "vowel into silence")
    t.add("AA", _vowel(0.400, 112, formants("AA"), rng), "abrupt", 20, "silence into vowel")
    t.add("sil", _silence(0.300), "abrupt", 20, "vowel into silence")
    t.add("UW", _vowel(0.400, 110, formants("UW"), rng), "abrupt", 20, "silence into vowel")
    t.add("sil", _silence(0.250), "abrupt", 20, "vowel into silence")
    _write_wav(HERE / t.name, t.samples)
    key += t.boundaries

    # ---- 2. VOT: long-lag vs short-lag ------------------------------------
    t = Track("practice-vot.wav")
    t.add("sil", _silence(0.200))
    t.add("closure", _silence(0.080), "not-markable", "",
          "silence into a silent closure: no acoustic event exists here, so it is not graded")
    t.add("burst", _burst(rng), "abrupt", 5,
          "burst onset: the tightest boundary in the set", onset_ramp=False)
    t.add("aspiration", _aspiration(0.069, rng), "not-graded", "",
          "burst into aspiration: not a boundary annotators mark; the exercise asks for burst onset and voicing onset",
          overlap_s=0.002)
    t.add("AA", _vowel(0.300, 115, formants("AA"), rng), "abrupt", 10,
          "voicing onset ends the VOT (long-lag token)")
    t.add("sil", _silence(0.200), "abrupt", 20, "vowel into silence")
    t.add("closure", _silence(0.080), "not-markable", "",
          "silence into a silent closure: no acoustic event exists here, so it is not graded")
    t.add("burst", _burst(rng), "abrupt", 5, "burst onset", onset_ramp=False)
    t.add("aspiration", _aspiration(0.016, rng), "not-graded", "",
          "burst into aspiration: not a boundary annotators mark; the exercise asks for burst onset and voicing onset",
          overlap_s=0.002)
    t.add("IY", _vowel(0.300, 120, formants("IY"), rng), "abrupt", 10,
          "voicing onset ends the VOT (short-lag token)")
    t.add("sil", _silence(0.200), "abrupt", 20, "vowel into silence")
    _write_wav(HERE / t.name, t.samples)
    key += t.boundaries

    # ---- 3. fricatives: two voiceless, one voiced -------------------------
    t = Track("practice-fricatives.wav")
    t.add("sil", _silence(0.150))
    t.add("AA", _vowel(0.180, 114, formants("AA"), rng), "abrupt", 20, "silence into vowel")
    t.add("S", _fricative(0.220, 6500, 1400, 0.55, rng), "abrupt", 15,
          "vowel into voiceless sibilant: periodic energy stops, high-frequency noise starts")
    t.add("AA", _vowel(0.180, 112, formants("AA"), rng), "abrupt", 15,
          "voiceless sibilant into vowel")
    t.add("sil", _silence(0.150), "abrupt", 20, "vowel into silence")
    t.add("IY", _vowel(0.180, 118, formants("IY"), rng), "abrupt", 20, "silence into vowel")
    t.add("SH", _fricative(0.220, 3200, 1200, 0.60, rng), "abrupt", 15,
          "vowel into lower-frequency sibilant")
    t.add("IY", _vowel(0.180, 116, formants("IY"), rng), "abrupt", 15,
          "lower-frequency sibilant into vowel")
    t.add("sil", _silence(0.150), "abrupt", 20, "vowel into silence")
    t.add("AA", _vowel(0.180, 113, formants("AA"), rng), "abrupt", 20, "silence into vowel")
    t.add("Z", _fricative(0.220, 6500, 1400, 0.50, rng, voiced_f0=110), "gradual", 30,
          "vowel into VOICED fricative: voicing continues across the boundary while frication rises over the window; key time is its midpoint",
          overlap_s=0.040)
    t.add("AA", _vowel(0.180, 111, formants("AA"), rng), "gradual", 30,
          "VOICED fricative into vowel: voicing continues across the boundary while frication fades over the window; key time is its midpoint",
          overlap_s=0.040)
    t.add("sil", _silence(0.150), "abrupt", 20, "vowel into silence")
    _write_wav(HERE / t.name, t.samples)
    key += t.boundaries

    # ---- 4. connected: includes ONE deliberately gradual boundary ---------
    t = Track("practice-connected.wav")
    t.add("sil", _silence(0.200))
    t.add("IY", _vowel(0.260, 119, formants("IY"), rng), "abrupt", 20, "silence into vowel")
    t.add("S", _fricative(0.180, 6500, 1400, 0.55, rng), "abrupt", 15, "vowel into voiceless sibilant")
    t.add("AA", _vowel(0.300, 114, formants("AA"), rng), "abrupt", 15, "voiceless sibilant into vowel")
    t.add("M", _murmur(0.240, 110, rng), "gradual", 40,
          "vowel into nasal murmur: formant amplitudes fall and the low murmur resonance rises across the window; key time is its midpoint",
          overlap_s=0.060)
    t.add("closure", _silence(0.070), "abrupt", 10, "murmur into the silent closure of the stop")
    t.add("burst", _burst(rng), "abrupt", 5, "burst onset", onset_ramp=False)
    t.add("aspiration", _aspiration(0.030, rng), "not-graded", "",
          "burst into aspiration: not a boundary annotators mark", overlap_s=0.002)
    t.add("UW", _vowel(0.280, 108, formants("UW"), rng), "abrupt", 10, "voicing onset")
    t.add("sil", _silence(0.200), "abrupt", 20, "vowel into silence")
    _write_wav(HERE / t.name, t.samples)
    key += t.boundaries

    out = HERE / "segmentation-key.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(key[0].keys()))
        w.writeheader()
        w.writerows(key)
    return key


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

    key = build_audio()
    for name in ("practice-vowels.wav", "practice-vot.wav",
                 "practice-fricatives.wav", "practice-connected.wav"):
        size = (HERE / name).stat().st_size
        print(f"wrote {name:<28} ({size / 1024:.0f} KB)")
    print(f"wrote segmentation-key.csv       ({len(key)} boundaries, 4 files)")
    print("now run: python3 verify_practice_data.py   (needs praat-parselmouth)")


if __name__ == "__main__":
    main()
