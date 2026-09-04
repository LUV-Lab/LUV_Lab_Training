#!/usr/bin/env python3
"""Verify the Module 2 audio fixtures AGAINST THE SIGNAL, with Praat itself.

Writes `verification-report.md` (MACHINE-WRITTEN -- never hand-edit; re-run
this script) and exits non-zero if any check fails.

Why this exists. The fixtures are synthesized by `make_practice_data.py`, and
the answer key in `people/training/praat-acoustics.md` makes claims about what
a student will SEE and MEASURE in those files. Until 2026-09-02 those claims
had been checked only against the synthesizer's intent (filter coefficients),
never against the rendered audio -- and a red-team cold read on 2026-08-30
showed several of them false of the audio (findings B2, B3, M2, M5, M7). This
script closes that gap: every claim the answer key makes about the audio is
measured here, with Praat's own analysis engine, and the numbers the key
quotes come from the report this writes.

Requirements: `pip install praat-parselmouth` (Praat's analysis code as a
Python module; the generator itself stays standard-library). Praat-version
sensitivity is small for these measures, and the report records the exact
Praat version it ran under. Opening the files in Praat's editor is still worth
five minutes -- this script reports numbers, not what a spectrogram looks like
to a person.

Usage:
    python3 verify_practice_data.py            # writes verification-report.md
    python3 verify_practice_data.py --date YYYY-MM-DD   # override the run date
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import math
import pathlib
import re
import statistics
import sys

try:
    import parselmouth as pm
    from parselmouth.praat import call
except ImportError:  # pragma: no cover
    sys.exit("verify_practice_data.py needs praat-parselmouth: pip install praat-parselmouth")

import make_practice_data as gen

HERE = pathlib.Path(__file__).resolve().parent
KEY = HERE / "segmentation-key.csv"
REPORT = HERE / "verification-report.md"
PRAAT_SCRIPT = HERE / "synthesize-practice-vowels.praat"

# The module's analysis settings (Module 2 §3.1 and §3.3; the lab-ratified
# ceilings, PI 2026-08-30) and its ratified pass tolerance (PI 2026-08-30).
CEILINGS = (5000, 5500)
N_FORMANTS = 5
WINDOW_S = 0.025
STEP_S = 0.005
PRE_EMPH_HZ = 50
TOL_F1, TOL_F2 = 50, 100
DYN_RANGE_DB = 50.0          # Praat's default spectrogram dynamic range
VOWELS = set(gen.TARGETS["M"].keys())
FRICATIVES = {"S": False, "SH": False, "Z": True}   # label -> expected voiced?


def _med(vals):
    vals = [v for v in vals if v == v]
    return statistics.median(vals) if vals else float("nan")


def _fmt(v, nd=0, sign=False):
    if v != v:
        return "undefined"
    return f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}"


def read_segments():
    """Rebuild per-file segments (label, start, end) from the boundary key."""
    with KEY.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    files = {}
    for r in rows:
        files.setdefault(r["file"], []).append(r)
    segments = {}
    for name, brs in files.items():
        dur = pm.Sound(str(HERE / name)).get_total_duration()
        segs = []
        start, label = 0.0, brs[0]["left_label"]
        for b in brs:
            t = float(b["time_s"])
            segs.append((label, start, t))
            start, label = t, b["right_label"]
        segs.append((label, start, dur))
        segments[name] = segs
    return rows, segments


def formants_in(snd, a, b, ceiling):
    fm = snd.to_formant_burg(time_step=STEP_S, max_number_of_formants=N_FORMANTS,
                             maximum_formant=ceiling, window_length=WINDOW_S,
                             pre_emphasis_from=PRE_EMPH_HZ)
    lo, hi = a + 0.2 * (b - a), a + 0.8 * (b - a)
    ts = [lo + i * STEP_S for i in range(int((hi - lo) / STEP_S) + 1)]
    return [_med([fm.get_value_at_time(k, t) for t in ts]) for k in (1, 2, 3)]


def spectrogram_levels(snd, t, freqs):
    """dB of the strongest bin within +/-100 Hz of each freq at time t, re the file's spectrogram max."""
    sp = snd.to_spectrogram(window_length=0.005, maximum_frequency=5000)
    xs, ys, vals = sp.xs(), sp.ys(), sp.values
    mx = vals.max()
    ti = min(range(len(xs)), key=lambda i: abs(xs[i] - t))
    out = []
    for f in freqs:
        fi = [i for i, y in enumerate(ys) if abs(y - f) <= 100]
        out.append(10 * math.log10(max(vals[fi, ti].max(), 1e-30) / mx))
    return out


def voicing_in(snd, a, b):
    pitch = snd.to_pitch()                      # Praat defaults: 75-600 Hz
    harm = snd.to_harmonicity_cc()              # Praat defaults
    lo, hi = a + 0.2 * (b - a), a + 0.8 * (b - a)
    ts = [lo + i * 0.005 for i in range(int((hi - lo) / 0.005) + 1)]
    f0 = [pitch.get_value_at_time(t) for t in ts]
    voiced = sum(1 for v in f0 if v == v)
    return voiced / len(ts), _med([harm.get_value(t) for t in ts])


def zero_run_near(samples, t, half_window_s=0.010):
    i0 = max(0, int((t - half_window_s) * gen.SR))
    i1 = min(len(samples), int((t + half_window_s) * gen.SR))
    best = run = 0
    for v in samples[i0:i1]:
        run = run + 1 if v == 0 else 0
        best = max(best, run)
    return best


def first_nonzero_after(samples, t):
    i = int(t * gen.SR)
    while i < len(samples) and samples[i] == 0:
        i += 1
    return i / gen.SR


def band_rise_time(snd, t_key, lo_hz, hi_hz):
    """10 %->90 % rise time of band power across a boundary.

    Band power from a 5 ms / 1 ms spectrogram, smoothed over 5 ms; the two
    levels are the MEDIANS 10-50 ms before and 10-50 ms after the key time,
    so a noise peak inside the fricative cannot masquerade as the "top".
    """
    sp = snd.to_spectrogram(window_length=0.005, maximum_frequency=gen.SR / 2, time_step=0.001)
    xs, ys, vals = sp.xs(), sp.ys(), sp.values
    fi = [i for i, y in enumerate(ys) if lo_hz <= y <= hi_hz]
    power = [vals[fi, i].sum() for i in range(len(xs))]
    sm = [statistics.fmean(power[max(0, i - 2):i + 3]) for i in range(len(power))]
    before = [sm[i] for i, x in enumerate(xs) if t_key - 0.050 <= x <= t_key - 0.010]
    after = [sm[i] for i, x in enumerate(xs) if t_key + 0.010 <= x <= t_key + 0.050]
    lo, hi = statistics.median(before), statistics.median(after)
    p10, p90 = lo + 0.1 * (hi - lo), lo + 0.9 * (hi - lo)
    idx = [i for i, x in enumerate(xs) if t_key - 0.050 <= x <= t_key + 0.050]
    t10 = next(xs[i] for i in idx if sm[i] >= p10)
    t90 = next(xs[i] for i in idx if xs[i] >= t10 and sm[i] >= p90)
    return (t90 - t10) * 1000


def voiced_fraction_after(snd, t_key, span_s=0.030):
    pitch = snd.to_pitch()
    ts = [t_key + 0.005 + i * 0.005 for i in range(int(span_s / 0.005))]
    return sum(1 for t in ts if pitch.get_value_at_time(t) == pitch.get_value_at_time(t)) / len(ts)


def parse_praat_script():
    """Pull the five (label, F1, F2) and the fixed settings out of the .praat script."""
    txt = PRAAT_SCRIPT.read_text(encoding="utf-8")
    labels = dict(re.findall(r'vowelLabel\$ \[(\d)\] = "([A-Z]+)"', txt))
    f1s = dict(re.findall(r"f1 \[(\d)\] =\s*(\d+)", txt))
    f2s = dict(re.findall(r"f2 \[(\d)\] =\s*(\d+)", txt))

    def setting(name):
        m = re.search(rf"^{name}\s*=\s*([0-9.]+)", txt, flags=re.M)
        return float(m.group(1))

    s = {k: setting(k) for k in ("duration", "pitch", "bandwidth1", "bandwidth2",
                                "f3", "bandwidth3", "f4", "bandwidthFraction",
                                "formantInterval")}
    vowels = [(labels[i], int(f1s[i]), int(f2s[i])) for i in sorted(labels)]
    return vowels, s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    args = ap.parse_args()

    failures = []
    L = []
    L.append("# verification-report.md — Module 2 audio fixtures, measured with Praat\n")
    L.append("**MACHINE-WRITTEN by `verify_practice_data.py` — do not hand-edit; re-run the script.**\n")
    L.append(f"- Run date: {args.date}")
    L.append(f"- Engine: Praat {pm.PRAAT_VERSION} via praat-parselmouth {pm.__version__}")
    L.append(f"- Generator settings under test: `SOURCE_TILT_CORNER_HZ={gen.SOURCE_TILT_CORNER_HZ}`, "
             f"`VOWEL_BANDWIDTHS={gen.VOWEL_BANDWIDTHS}`, `HIGHER_FORMANTS={gen.HIGHER_FORMANTS}`, "
             f"`FRICATIVE_VOICING_DB={gen.FRICATIVE_VOICING_DB}`, `JOIN_S={gen.JOIN_S}`, "
             f"`EDGE_RAMP_S={gen.EDGE_RAMP_S}`, `AUDIO_SEED={gen.AUDIO_SEED}`")
    L.append(f"- Analysis settings (the module's): `To Formant (burg)` with {N_FORMANTS} formants, "
             f"{WINDOW_S} s window, {STEP_S} s step, pre-emphasis from {PRE_EMPH_HZ} Hz, at the ceilings "
             f"{' and '.join(f'{c:,} Hz' for c in CEILINGS)}; median over the middle 20–80 % of each vowel. "
             f"Pass = within ±{TOL_F1} Hz (F1) / ±{TOL_F2} Hz (F2) of the generator's target "
             f"(the module's PI-ratified tolerance, 2026-08-30). F3 is reported, not graded.")
    L.append("")

    rows, segments = read_segments()
    targets = gen.TARGETS["M"]

    # ---- 1. vowel formants ------------------------------------------------
    L.append("## 1. Vowel formants — does Praat measure the targets back?\n")
    L.append("| file | vowel | target F1/F2/F3 | ceiling | Praat F1 / F2 / F3 | ΔF1 | ΔF2 | result |")
    L.append("|---|---|---|---|---|---|---|---|")
    for name, segs in segments.items():
        snd = pm.Sound(str(HERE / name))
        for label, a, b in segs:
            if label not in VOWELS:
                continue
            t1, t2, t3 = targets[label]
            for ceiling in CEILINGS:
                f1, f2, f3 = formants_in(snd, a, b, ceiling)
                d1, d2 = f1 - t1, f2 - t2
                ok = d1 == d1 and d2 == d2 and abs(d1) <= TOL_F1 and abs(d2) <= TOL_F2
                if not ok:
                    failures.append(f"{name} {label} @ {ceiling}: F1 {_fmt(f1)} F2 {_fmt(f2)}")
                L.append(f"| `{name}` | {label} ({a:.3f}–{b:.3f} s) | {t1}/{t2}/{t3} | {ceiling:,} Hz | "
                         f"{_fmt(f1)} / {_fmt(f2)} / {_fmt(f3)} | {_fmt(d1, 0, sign=True)} | {_fmt(d2, 0, sign=True)} | "
                         f"{'PASS' if ok else 'FAIL'} |")
    L.append("")

    # ---- 2. spectrogram visibility ----------------------------------------
    L.append("## 2. Spectrogram visibility — are F1–F3 above Praat's 50 dB display floor?\n")
    L.append("Level of the strongest spectrogram bin within ±100 Hz of each target formant, at the vowel's "
             "midpoint (5 ms Gaussian window, as Praat's default view), relative to the file's spectrogram "
             f"maximum. Anything below −{DYN_RANGE_DB:.0f} dB renders white in Praat's default view. "
             "Pass = F1 and F2 above the floor (F3 reported).\n")
    L.append("| file | vowel | F1 level | F2 level | F3 level | result |")
    L.append("|---|---|---|---|---|---|")
    for name, segs in segments.items():
        snd = pm.Sound(str(HERE / name))
        for label, a, b in segs:
            if label not in VOWELS:
                continue
            l1, l2, l3 = spectrogram_levels(snd, (a + b) / 2, targets[label])
            ok = l1 > -DYN_RANGE_DB and l2 > -DYN_RANGE_DB
            if not ok:
                failures.append(f"{name} {label}: spectrogram level F1 {l1:.1f} F2 {l2:.1f} dB")
            L.append(f"| `{name}` | {label} | {l1:.1f} dB | {l2:.1f} dB | {l3:.1f} dB | {'PASS' if ok else 'FAIL'} |")
    L.append("")

    # ---- 3. fricative voicing ---------------------------------------------
    L.append("## 3. Fricative voicing — is `Z` voiced and are `S`/`SH` not?\n")
    L.append("Praat `To Pitch` (defaults) and `To Harmonicity (cc)` (defaults) over the middle 60 % of each "
             "fricative. Pass = a voiced fricative has ≥ 80 % voiced frames, a voiceless one ≤ 20 %.\n")
    L.append("| file | fricative | expected | voiced frames | median HNR | result |")
    L.append("|---|---|---|---|---|---|")
    for name, segs in segments.items():
        snd = pm.Sound(str(HERE / name))
        for label, a, b in segs:
            if label not in FRICATIVES:
                continue
            frac, hnr = voicing_in(snd, a, b)
            exp = FRICATIVES[label]
            ok = frac >= 0.8 if exp else frac <= 0.2
            if not ok:
                failures.append(f"{name} {label}: voiced fraction {frac:.2f}")
            L.append(f"| `{name}` | {label} ({a:.3f}–{b:.3f} s) | {'voiced' if exp else 'voiceless'} | "
                     f"{frac * 100:.0f} % | {hnr:.1f} dB | {'PASS' if ok else 'FAIL'} |")
    L.append("")

    # ---- 4. boundaries ----------------------------------------------------
    L.append("## 4. Boundaries — the key against the samples\n")
    L.append("For every boundary out of silence: the first non-zero sample must sit within the boundary's "
             "tolerance of the key time. For every join between two sounds: there must be **no run of exact "
             "digital zeros** within ±10 ms of the key time (the pre-2026-09-02 fixtures notched to zero at "
             "every join, which is what red-team finding M7 objected to). Not-markable / not-graded rows are "
             "listed, not tested.\n")
    L.append("| file | # | key time | left → right | type | tol (ms) | check | result |")
    L.append("|---|---|---|---|---|---|---|---|")
    samples_by_file = {name: pm.Sound(str(HERE / name)).values[0].tolist() for name in segments}
    for r in rows:
        name, t = r["file"], float(r["time_s"])
        smp = samples_by_file[name]
        btype, tol = r["boundary_type"], r["tolerance_ms"]
        left, right = r["left_label"], r["right_label"]
        if btype in ("not-markable", "not-graded"):
            check, res = "—", "listed"
        elif left in gen.SILENT_LABELS and right not in gen.SILENT_LABELS:
            onset = first_nonzero_after(smp, max(0.0, t - 0.001))
            err_ms = (onset - t) * 1000
            ok = abs(err_ms) <= float(tol)
            check, res = f"first non-zero sample at {onset:.4f} s ({err_ms:+.1f} ms)", "PASS" if ok else "FAIL"
            if not ok:
                failures.append(f"{name} boundary {r['boundary_index']} onset error {err_ms:+.1f} ms")
        elif right in gen.SILENT_LABELS:
            check, res = "fade into silence (by construction)", "PASS"
        else:
            zr = zero_run_near(smp, t)
            ok = zr == 0
            check, res = f"longest zero run within ±10 ms: {zr} samples", "PASS" if ok else "FAIL"
            if not ok:
                failures.append(f"{name} boundary {r['boundary_index']} zero run {zr}")
        win = f" (window {r['window_start_s']}–{r['window_end_s']} s)" if r["window_start_s"] else ""
        L.append(f"| `{name}` | {r['boundary_index']} | {t:.4f}{win} | {left} → {right} | {btype} | "
                 f"{tol or '—'} | {check} | {res} |")
    L.append("")

    # ---- 4b. step vs ramp at vowel -> fricative -------------------------------
    L.append("## 4b. Step or ramp? — what the answer key to Exercise 4(c) claims, measured\n")
    L.append("At each vowel→fricative boundary: the 10 %→90 % rise time of power above 4 kHz (frication "
             "arriving) and the fraction of voiced frames (Praat `To Pitch`, defaults) in the 30 ms after the key "
             "time. The key says a voiceless fricative starts as a step with voicing stopping, and the voiced one "
             "as a ramp with voicing continuing. Pass = rise time < 12 ms and voicing ≤ 20 % after a voiceless "
             "boundary; rise time ≥ 20 ms and voicing ≥ 80 % after the voiced one.\n")
    L.append("| file | boundary | high-band rise time | voiced frames after | result |")
    L.append("|---|---|---|---|---|")
    for r in rows:
        if r["left_label"] not in VOWELS or r["right_label"] not in FRICATIVES:
            continue
        snd = pm.Sound(str(HERE / r["file"]))
        t = float(r["time_s"])
        rise = band_rise_time(snd, t, 4000, gen.SR / 2)
        vf = voiced_fraction_after(snd, t)
        voiced = FRICATIVES[r["right_label"]]
        ok = (rise >= 20 and vf >= 0.8) if voiced else (rise < 12 and vf <= 0.2)
        if not ok:
            failures.append(f"{r['file']} {r['left_label']}→{r['right_label']}: rise {rise:.1f} ms, voiced after {vf:.2f}")
        L.append(f"| `{r['file']}` | {r['left_label']} → {r['right_label']} at {t:.4f} s | {rise:.1f} ms | "
                 f"{vf * 100:.0f} % | {'PASS' if ok else 'FAIL'} |")
    L.append("")

    # ---- 5. VOT from the key ----------------------------------------------
    L.append("## 5. VOT — computed from the key (burst onset → voicing onset)\n")
    L.append("Class labels apply to `practice-vot.wav` only (long-lag at ≥ 40 ms, as the exercise uses the terms).\n")
    L.append("| file | token | burst onset | voicing onset | VOT | class |")
    L.append("|---|---|---|---|---|---|")
    for name, brs in {n: [r for r in rows if r["file"] == n] for n in segments}.items():
        bursts = [float(r["time_s"]) for r in brs if r["right_label"] == "burst"]
        voicings = [float(r["time_s"]) for r in brs if r["left_label"] == "aspiration"]
        for i, (bt, vt) in enumerate(zip(bursts, voicings), start=1):
            vot = (vt - bt) * 1000
            cls = ("long-lag" if vot >= 40 else "short-lag") if name == "practice-vot.wav" else "— (not graded)"
            L.append(f"| `{name}` | {i} | {bt:.4f} s | {vt:.4f} s | {vot:.1f} ms | {cls} |")
    L.append("")

    # ---- 6. Route B synthesis (Exercise 1) --------------------------------
    L.append("## 6. Exercise 1, Route B — the five `synthesize-practice-vowels.praat` vowels, measured back\n")
    vowels, s = parse_praat_script()
    L.append(f"Synthesized here with Praat's `Create KlattGrid from vowel` using the values read from the "
             f"committed script (duration {s['duration']} s, pitch {s['pitch']:.0f} Hz, B1 {s['bandwidth1']:.0f}, "
             f"B2 {s['bandwidth2']:.0f}, F3 {s['f3']:.0f}, B3 {s['bandwidth3']:.0f}, F4 {s['f4']:.0f}, "
             f"bandwidth fraction {s['bandwidthFraction']}, formant interval {s['formantInterval']:.0f} Hz), "
             f"then `To Sound` and the module's `To Formant (burg)` settings. This is what the Exercise 1 "
             f"answer key quotes; Route A (the VowelEditor) synthesizes differently and may differ in detail.\n")
    L.append("| vowel | true F1 / F2 | 5,500 Hz (Praat default) | 5,000 Hz | 3,000 Hz (too low) | 8,000 Hz (too high) |")
    L.append("|---|---|---|---|---|---|")
    for label, f1, f2 in vowels:
        kg = call("Create KlattGrid from vowel", label, s["duration"], s["pitch"], f1, s["bandwidth1"],
                  f2, s["bandwidth2"], s["f3"], s["bandwidth3"], s["f4"], s["bandwidthFraction"],
                  s["formantInterval"])
        snd = call(kg, "To Sound")
        cells = []
        for ceiling in (5500, 5000, 3000, 8000):
            m = formants_in(snd, 0.0, s["duration"], ceiling)
            cells.append(f"{_fmt(m[0])} / {_fmt(m[1])} / {_fmt(m[2])}")
            if ceiling in (5500, 5000):
                ok = abs(m[0] - f1) <= TOL_F1 and abs(m[1] - f2) <= TOL_F2
                if not ok:
                    failures.append(f"Route B {label} @ {ceiling}: F1 {_fmt(m[0])} F2 {_fmt(m[1])}")
        L.append(f"| {label} | {f1} / {f2} | {' | '.join(cells)} |")
    L.append("\n*(Cells are F1 / F2 / F3 as Praat labels them. At 5,500 and 5,000 Hz the pass tolerance "
             "applies and is checked; the 3,000 and 8,000 Hz columns document what a wrong ceiling does "
             "and are not graded.)*\n")

    # ---- summary ------------------------------------------------------------
    L.insert(6, f"**Result: {'PASS — every check passed' if not failures else 'FAIL — ' + str(len(failures)) + ' check(s) failed'}.**\n")
    if failures:
        L.append("## Failures\n")
        L += [f"- {f}" for f in failures]
        L.append("")
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {REPORT.name}: {'PASS' if not failures else 'FAIL (%d)' % len(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
