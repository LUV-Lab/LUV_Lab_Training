<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 867e294 on 2026-08-26.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# practice-data/praat/ — materials for Module 2 (Praat / acoustic measurement)

**Owner: undergrad-mentor.** Used by `people/training/praat-acoustics.md`.

> **All data here is SYNTHETIC.** Formant values are generated around textbook
> adult targets with deterministic jitter. **No real participant recording,
> transcript, measurement, or metadata is used here, and none may ever be
> added.** Practice materials are synthetic or published only — see
> `people/training/data-ethics-for-ras.md`.

## Files

| File | What it is |
|---|---|
| `formants-practice.csv` | 42 synthetic formant measurements, 2 synthetic speakers (`P01` higher-formant, `P02` lower-formant), 7 vowels × 3 words each. **Carries four seeded items** for Exercise 2 — three tracker errors and one item that looks like an error but is not. |
| `synthesize-practice-vowels.praat` | Convenience script for Exercise 1: synthesizes vowels with F1/F2 *you* specify, so you can measure them back against known truth. **Its `Create KlattGrid from vowel` call is `[confirm]`** — verify the argument order against your Praat version, or use the VowelEditor GUI route in the module instead. The exercise does not depend on the script. |
| `measurement-log.csv` | Header-only template you fill in during Exercise 1. |
| `make_practice_data.py` | Generator for the two CSVs. Standard library only. |

## Regenerating

The CSVs are **machine-written**. Per the lab's provenance norm, never
hand-edit them — change the generator and re-run:

```bash
python3 make_practice_data.py
```

The seed is fixed (`SEED = 20260805`), so the same values come back every time
and the answer key in the module stays valid. **If you change the seed, the
targets, or the word list, the module's answer key stops matching** — update
both together or not at all.

## A note on the reference targets

The F1/F2 targets in the generator are conventional textbook adult values,
marked `ASSUMPTION` in the code. **They are not a lab measurement standard and
nothing in this repo ratifies them.** They are here to make plausible practice
data, not to define what counts as a correct measurement. To sanity-check
their shape against published data, load `phonTools::pb52` in R — the
Peterson & Barney (1952) vowel measurements (ledger keys
`peterson1952control`, `barreda2023phontools`, both VERIFIED).
