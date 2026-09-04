<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 0fa324c8 on 2026-09-04.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# practice-data/praat/ — materials for Module 2 (Praat / acoustic measurement)

**Owner: undergrad-mentor.** Used by `people/training/praat-acoustics.md`.

> **All data here is SYNTHETIC.** Formant values are generated around textbook
> adult targets with deterministic jitter; the audio is synthesized from scratch.
> **No real participant recording, transcript, measurement, or metadata is used
> here, and none may ever be added.** Practice materials are synthetic or
> published only — see `people/training/data-ethics-for-ras.md`.

> **Answers are not in this file.** The exercises are graded against files in this
> directory that the module tells you not to open until you have finished. This README
> describes what each file *is*, not what you are supposed to find in it. *(Rewritten
> 2026-09-02 after the 2026-08-30 red-team read, finding M4: the previous version of this
> table gave away the answers to Exercises 4(b), 4(c) and 4(d).)*

## Files

| File | What it is |
|---|---|
| `formants-practice.csv` | 42 synthetic formant measurements, 2 synthetic speakers (`P01` higher-formant, `P02` lower-formant), 7 vowels × 3 words each. **Carries four seeded items across five rows** for Exercise 2 — three tracker errors and one item that looks like an error but is not (the fourth item is present in both speakers on purpose). *(Count corrected 2026-09-02, review m4.)* |
| `synthesize-practice-vowels.praat` | Convenience script for Exercise 1: synthesizes vowels with F1/F2 *you* specify, so you can measure them back against known truth. **Run successfully in Praat by the PI on 2026-08-29**, producing the five named Sound objects; its `Create KlattGrid from vowel` call is also checked against Praat's own manual page (twelve arguments), and the script's header explains what each argument does — including why F4 takes a bandwidth *fraction* rather than a bandwidth. The VowelEditor GUI route in the module is an equally good alternative if you would rather not run a script. **The five vowels it makes were measured back with Praat on 2026-09-02** (`verification-report.md` §6). |
| `measurement-log.csv` | Header-only template you fill in during Exercise 1. |
| `practice-vowels.wav` | **Exercise 4(a).** Three steady vowels (`IY`, `AA`, `UW`) separated by silence, 2.30 s. Synthesized at the generator's lower-formant (`M`) targets, so it also serves formant measurement — and, since 2026-09-02, Praat has been shown to measure those targets back (`verification-report.md` §1). |
| `practice-vot.wav` | **Exercise 4(b).** Two stop-plus-vowel tokens laid out as silence · closure · burst · aspiration · vowel, 1.45 s. You determine the two VOTs and their categories. |
| `practice-fricatives.wav` | **Exercise 4(c).** Three VCV tokens with three different fricatives, 2.24 s. You determine which boundary is hardest to place and why. |
| `practice-connected.wav` | **Exercise 4(d).** A short connected sequence between silences — vowel, fricative, vowel, nasal, stop, vowel — 1.69 s: eight speech segments, ten counting the two silences, nine boundaries. *(Count corrected 2026-09-02, review M3: earlier text said "seven-segment" in one place and "ten-segment" in another.)* |
| `segmentation-key.csv` | Ground truth for the four `.wav` files, **one row per boundary**: `file`, `boundary_index`, `time_s`, `left_label`, `right_label`, `boundary_type` (`abrupt` / `gradual` / `not-markable` / `not-graded`), `tolerance_ms`, `window_start_s` / `window_end_s` (filled for gradual boundaries), and a note. The generator writes it from the durations it used — **nothing here was measured by ear.** *(Schema changed 2026-09-02 from one row per segment: a boundary shared by two segments carried two tolerances, review m3.)* **Do not open it until the module says so.** |
| `make_practice_data.py` | Generator for the two CSVs, the four `.wav` files and the key. **Standard library only** (`math`, `wave`, `random`, `struct`) — no numpy, nothing to install. Its docstring carries a dated change record. |
| `verify_practice_data.py` | Checks the generated audio **against the signal, with Praat** — formants measured back, spectrogram visibility, fricative voicing, boundaries, VOT, and the Route B vowels — and writes `verification-report.md`. Needs `pip install praat-parselmouth` (Praat's analysis engine as a Python module); the generator does not. Exits non-zero on any failure. |
| `verification-report.md` | **Machine-written** by the verifier — dated, with the Praat version it ran under. The answer key in the module quotes its numbers. **Do not open it until the module says so** (it states results). |

## Regenerating

The CSVs are **machine-written**. Per the lab's provenance norm, never
hand-edit them — change the generator and re-run:

```bash
python3 make_practice_data.py            # standard library; rewrites everything
python3 verify_practice_data.py          # needs praat-parselmouth; must PASS
```

**The audio is machine-written too.** It is synthesized from scratch by a Klatt-style cascade
of two-pole resonators driven by a tilted impulse train (voiced) or by noise (voiceless) —
**no recording of any kind is read, and no participant audio may ever be placed in this
directory.** The synthesizer uses its own generator instance and its own seed
(`AUDIO_SEED = 20260828`) precisely so that adding or rebuilding audio cannot perturb the CSV
values; the CSVs were byte-identical before and after the audio was added on 2026-08-28, and
again before and after the audio was rebuilt on 2026-09-02.

**Verification — corrected 2026-09-02.** The paragraph that stood here from 2026-08-28 read:

> ~~*Verification of the audio, recorded so it is not re-litigated:* formant peaks measured
> from the filter's impulse response by DFT land within **10 Hz** of their targets — the
> analysis grid step, i.e. exact to the measurement (`IY` 320/2200/2900 → 320/2200/2890; `AA`
> 720/1200/2500 → 720/1190/2490; `UW` 350/1050/2350 → 350/1040/2340). Segment boundaries were
> checked against a 10 ms RMS envelope and match the key to within the window step. **Praat
> itself is not installed in the environment that generated these**, so nothing here rests on
> a visual check in Praat.~~

**Struck** after the red-team cold read of 2026-08-30 (finding B3). It verified the resonator
coefficients, which were never in doubt — not the rendered audio, which is what a student
opens. Measured in Praat, the 2026-08-28 vowels gave F1/F2 of 263/381 (`IY`), 300/709 (`AA`)
and 274/364 (`UW`) at the module's 5,000 Hz ceiling: the glottal source's spectral tilt had
pushed F2 and F3 below the spectrogram's 50 dB floor, and the tracker fitted a spurious low
pole instead. The same read found the "voiced" fricative unvoiced (its voicing was mixed about
21 dB below its own noise) and every join notched to digital zero. The audio was rebuilt on
2026-09-02 (the generator's docstring records exactly what changed and why), and it is now
verified **against the signal, with Praat's own engine**: `verify_practice_data.py` writes
`verification-report.md`, which records the run date, the Praat version, every measurement,
and a PASS/FAIL. **Last run: 2026-09-02, Praat 6.1.38 via praat-parselmouth 0.4.7 — PASS.**
Re-run it after any change to the generator; the report must pass before the module's answer
key is trusted. *One disclosure for readers of the public mirror (added 2026-09-02, re-check
m-8): every `.md` file in this directory — this machine-written report included — has a
provenance banner prepended at publish time. That banner is the only alteration, so the mirror's
copy of the report will not byte-match a fresh run's output; everything below the banner does.* A five-minute look at the files in Praat's editor is still worth doing — the
report gives numbers, not what a spectrogram looks like to a person.

The formant-CSV seed is fixed (`SEED = 20260805`), so the same values come back every time
and the answer key in the module stays valid. **If you change either seed, the targets, the
word list, or any synthesis setting, the module's answer key stops matching** — update both
together or not at all, and re-run the verifier.

## A note on the reference targets

The F1/F2 targets in the generator are conventional textbook adult values,
marked `ASSUMPTION` in the code. **They are not a lab measurement standard and
nothing in this repo ratifies them.** They are here to make plausible practice
data, not to define what counts as a correct measurement. To sanity-check
their shape against published data, load `phonTools::pb52` in R — the
Peterson & Barney (1952) vowel measurements (ledger keys
`peterson1952control`, `barreda2023phontools`, both VERIFIED). The synthesis
settings that were tuned on 2026-09-02 (source tilt, bandwidths, the two fixed
higher formants) are likewise `ASSUMPTION`s about what a plausible synthetic
speaker looks like — chosen so that Praat recovers the targets, and recorded
as such in the generator.
