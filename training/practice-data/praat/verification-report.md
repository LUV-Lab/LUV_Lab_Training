<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 0fa324c8 on 2026-09-04.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# verification-report.md — Module 2 audio fixtures, measured with Praat

**MACHINE-WRITTEN by `verify_practice_data.py` — do not hand-edit; re-run the script.**

- Run date: 2026-09-02
- Engine: Praat 6.1.38 via praat-parselmouth 0.4.7
- Generator settings under test: `SOURCE_TILT_CORNER_HZ=150`, `VOWEL_BANDWIDTHS=(60, 90, 120)`, `HIGHER_FORMANTS=((3400, 120), (4200, 150))`, `FRICATIVE_VOICING_DB=3.0`, `JOIN_S=0.004`, `EDGE_RAMP_S=0.004`, `AUDIO_SEED=20260828`
- Analysis settings (the module's): `To Formant (burg)` with 5 formants, 0.025 s window, 0.005 s step, pre-emphasis from 50 Hz, at the ceilings 5,000 Hz and 5,500 Hz; median over the middle 20–80 % of each vowel. Pass = within ±50 Hz (F1) / ±100 Hz (F2) of the generator's target (the module's PI-ratified tolerance, 2026-08-30). F3 is reported, not graded.
**Result: PASS — every check passed.**


## 1. Vowel formants — does Praat measure the targets back?

| file | vowel | target F1/F2/F3 | ceiling | Praat F1 / F2 / F3 | ΔF1 | ΔF2 | result |
|---|---|---|---|---|---|---|---|
| `practice-vowels.wav` | IY (0.250–0.650 s) | 320/2200/2900 | 5,000 Hz | 346 / 2195 / 2909 | +26 | -5 | PASS |
| `practice-vowels.wav` | IY (0.250–0.650 s) | 320/2200/2900 | 5,500 Hz | 343 / 2187 / 2945 | +23 | -13 | PASS |
| `practice-vowels.wav` | AA (0.950–1.350 s) | 720/1200/2500 | 5,000 Hz | 715 / 1203 / 2492 | -5 | +3 | PASS |
| `practice-vowels.wav` | AA (0.950–1.350 s) | 720/1200/2500 | 5,500 Hz | 707 / 1188 / 2478 | -13 | -12 | PASS |
| `practice-vowels.wav` | UW (1.650–2.050 s) | 350/1050/2350 | 5,000 Hz | 348 / 1051 / 2340 | -2 | +1 | PASS |
| `practice-vowels.wav` | UW (1.650–2.050 s) | 350/1050/2350 | 5,500 Hz | 345 / 1037 / 2318 | -5 | -13 | PASS |
| `practice-vot.wav` | AA (0.351–0.649 s) | 720/1200/2500 | 5,000 Hz | 709 / 1191 / 2492 | -11 | -9 | PASS |
| `practice-vot.wav` | AA (0.351–0.649 s) | 720/1200/2500 | 5,500 Hz | 704 / 1181 / 2481 | -16 | -19 | PASS |
| `practice-vot.wav` | IY (0.947–1.245 s) | 320/2200/2900 | 5,000 Hz | 346 / 2188 / 2906 | +26 | -12 | PASS |
| `practice-vot.wav` | IY (0.947–1.245 s) | 320/2200/2900 | 5,500 Hz | 343 / 2179 / 2943 | +23 | -21 | PASS |
| `practice-fricatives.wav` | AA (0.150–0.328 s) | 720/1200/2500 | 5,000 Hz | 716 / 1203 / 2486 | -4 | +3 | PASS |
| `practice-fricatives.wav` | AA (0.150–0.328 s) | 720/1200/2500 | 5,500 Hz | 714 / 1203 / 2500 | -6 | +3 | PASS |
| `practice-fricatives.wav` | AA (0.544–0.722 s) | 720/1200/2500 | 5,000 Hz | 725 / 1209 / 2483 | +5 | +9 | PASS |
| `practice-fricatives.wav` | AA (0.544–0.722 s) | 720/1200/2500 | 5,500 Hz | 721 / 1207 / 2502 | +1 | +7 | PASS |
| `practice-fricatives.wav` | IY (0.872–1.050 s) | 320/2200/2900 | 5,000 Hz | 345 / 2198 / 2910 | +25 | -2 | PASS |
| `practice-fricatives.wav` | IY (0.872–1.050 s) | 320/2200/2900 | 5,500 Hz | 346 / 2202 / 2910 | +26 | +2 | PASS |
| `practice-fricatives.wav` | IY (1.266–1.444 s) | 320/2200/2900 | 5,000 Hz | 344 / 2194 / 2908 | +24 | -6 | PASS |
| `practice-fricatives.wav` | IY (1.266–1.444 s) | 320/2200/2900 | 5,500 Hz | 344 / 2196 / 2906 | +24 | -4 | PASS |
| `practice-fricatives.wav` | AA (1.594–1.754 s) | 720/1200/2500 | 5,000 Hz | 713 / 1199 / 2495 | -7 | -1 | PASS |
| `practice-fricatives.wav` | AA (1.594–1.754 s) | 720/1200/2500 | 5,500 Hz | 712 / 1196 / 2493 | -8 | -4 | PASS |
| `practice-fricatives.wav` | AA (1.934–2.094 s) | 720/1200/2500 | 5,000 Hz | 720 / 1204 / 2493 | +0 | +4 | PASS |
| `practice-fricatives.wav` | AA (1.934–2.094 s) | 720/1200/2500 | 5,500 Hz | 724 / 1209 / 2500 | +4 | +9 | PASS |
| `practice-connected.wav` | IY (0.200–0.458 s) | 320/2200/2900 | 5,000 Hz | 349 / 2189 / 2888 | +29 | -11 | PASS |
| `practice-connected.wav` | IY (0.200–0.458 s) | 320/2200/2900 | 5,500 Hz | 343 / 2186 / 2944 | +23 | -14 | PASS |
| `practice-connected.wav` | AA (0.634–0.902 s) | 720/1200/2500 | 5,000 Hz | 719 / 1207 / 2480 | -1 | +7 | PASS |
| `practice-connected.wav` | AA (0.634–0.902 s) | 720/1200/2500 | 5,500 Hz | 715 / 1203 / 2498 | -5 | +3 | PASS |
| `practice-connected.wav` | UW (1.214–1.492 s) | 350/1050/2350 | 5,000 Hz | 355 / 1066 / 2334 | +5 | +16 | PASS |
| `practice-connected.wav` | UW (1.214–1.492 s) | 350/1050/2350 | 5,500 Hz | 346 / 1048 / 2335 | -4 | -2 | PASS |

## 2. Spectrogram visibility — are F1–F3 above Praat's 50 dB display floor?

Level of the strongest spectrogram bin within ±100 Hz of each target formant, at the vowel's midpoint (5 ms Gaussian window, as Praat's default view), relative to the file's spectrogram maximum. Anything below −50 dB renders white in Praat's default view. Pass = F1 and F2 above the floor (F3 reported).

| file | vowel | F1 level | F2 level | F3 level | result |
|---|---|---|---|---|---|
| `practice-vowels.wav` | IY | -6.4 dB | -26.4 dB | -29.4 dB | PASS |
| `practice-vowels.wav` | AA | -8.4 dB | -16.0 dB | -37.8 dB | PASS |
| `practice-vowels.wav` | UW | -4.9 dB | -22.0 dB | -42.9 dB | PASS |
| `practice-vot.wav` | AA | -5.3 dB | -13.3 dB | -32.6 dB | PASS |
| `practice-vot.wav` | IY | -6.4 dB | -20.1 dB | -20.7 dB | PASS |
| `practice-fricatives.wav` | AA | -5.1 dB | -12.4 dB | -31.4 dB | PASS |
| `practice-fricatives.wav` | AA | -6.1 dB | -12.1 dB | -33.1 dB | PASS |
| `practice-fricatives.wav` | IY | -6.4 dB | -26.0 dB | -29.2 dB | PASS |
| `practice-fricatives.wav` | IY | -8.6 dB | -29.5 dB | -33.1 dB | PASS |
| `practice-fricatives.wav` | AA | -4.1 dB | -9.3 dB | -29.8 dB | PASS |
| `practice-fricatives.wav` | AA | -4.3 dB | -10.3 dB | -29.5 dB | PASS |
| `practice-connected.wav` | IY | -6.3 dB | -25.7 dB | -27.5 dB | PASS |
| `practice-connected.wav` | AA | -8.1 dB | -17.1 dB | -37.8 dB | PASS |
| `practice-connected.wav` | UW | -4.7 dB | -22.3 dB | -44.6 dB | PASS |

## 3. Fricative voicing — is `Z` voiced and are `S`/`SH` not?

Praat `To Pitch` (defaults) and `To Harmonicity (cc)` (defaults) over the middle 60 % of each fricative. Pass = a voiced fricative has ≥ 80 % voiced frames, a voiceless one ≤ 20 %.

| file | fricative | expected | voiced frames | median HNR | result |
|---|---|---|---|---|---|
| `practice-fricatives.wav` | S (0.328–0.544 s) | voiceless | 0 % | -0.3 dB | PASS |
| `practice-fricatives.wav` | SH (1.050–1.266 s) | voiceless | 0 % | -2.8 dB | PASS |
| `practice-fricatives.wav` | Z (1.754–1.934 s) | voiced | 100 % | 6.3 dB | PASS |
| `practice-connected.wav` | S (0.458–0.634 s) | voiceless | 0 % | 0.0 dB | PASS |

## 4. Boundaries — the key against the samples

For every boundary out of silence: the first non-zero sample must sit within the boundary's tolerance of the key time. For every join between two sounds: there must be **no run of exact digital zeros** within ±10 ms of the key time (the pre-2026-09-02 fixtures notched to zero at every join, which is what red-team finding M7 objected to). Not-markable / not-graded rows are listed, not tested.

| file | # | key time | left → right | type | tol (ms) | check | result |
|---|---|---|---|---|---|---|---|
| `practice-vowels.wav` | 1 | 0.2500 | sil → IY | abrupt | 20 | first non-zero sample at 0.2500 s (+0.0 ms) | PASS |
| `practice-vowels.wav` | 2 | 0.6500 | IY → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-vowels.wav` | 3 | 0.9500 | sil → AA | abrupt | 20 | first non-zero sample at 0.9500 s (+0.0 ms) | PASS |
| `practice-vowels.wav` | 4 | 1.3500 | AA → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-vowels.wav` | 5 | 1.6500 | sil → UW | abrupt | 20 | first non-zero sample at 1.6501 s (+0.1 ms) | PASS |
| `practice-vowels.wav` | 6 | 2.0500 | UW → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-vot.wav` | 1 | 0.2000 | sil → closure | not-markable | — | — | listed |
| `practice-vot.wav` | 2 | 0.2800 | closure → burst | abrupt | 5 | first non-zero sample at 0.2800 s (+0.0 ms) | PASS |
| `practice-vot.wav` | 3 | 0.2850 | burst → aspiration | not-graded | — | — | listed |
| `practice-vot.wav` | 4 | 0.3510 | aspiration → AA | abrupt | 10 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-vot.wav` | 5 | 0.6490 | AA → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-vot.wav` | 6 | 0.8490 | sil → closure | not-markable | — | — | listed |
| `practice-vot.wav` | 7 | 0.9290 | closure → burst | abrupt | 5 | first non-zero sample at 0.9290 s (-0.0 ms) | PASS |
| `practice-vot.wav` | 8 | 0.9340 | burst → aspiration | not-graded | — | — | listed |
| `practice-vot.wav` | 9 | 0.9469 | aspiration → IY | abrupt | 10 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-vot.wav` | 10 | 1.2449 | IY → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-fricatives.wav` | 1 | 0.1500 | sil → AA | abrupt | 20 | first non-zero sample at 0.1500 s (+0.0 ms) | PASS |
| `practice-fricatives.wav` | 2 | 0.3280 | AA → S | abrupt | 15 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-fricatives.wav` | 3 | 0.5440 | S → AA | abrupt | 15 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-fricatives.wav` | 4 | 0.7220 | AA → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-fricatives.wav` | 5 | 0.8720 | sil → IY | abrupt | 20 | first non-zero sample at 0.8720 s (+0.0 ms) | PASS |
| `practice-fricatives.wav` | 6 | 1.0500 | IY → SH | abrupt | 15 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-fricatives.wav` | 7 | 1.2660 | SH → IY | abrupt | 15 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-fricatives.wav` | 8 | 1.4440 | IY → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-fricatives.wav` | 9 | 1.5940 | sil → AA | abrupt | 20 | first non-zero sample at 1.5940 s (+0.0 ms) | PASS |
| `practice-fricatives.wav` | 10 | 1.7540 (window 1.7340–1.7740 s) | AA → Z | gradual | 30 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-fricatives.wav` | 11 | 1.9340 (window 1.9140–1.9540 s) | Z → AA | gradual | 30 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-fricatives.wav` | 12 | 2.0940 | AA → sil | abrupt | 20 | fade into silence (by construction) | PASS |
| `practice-connected.wav` | 1 | 0.2000 | sil → IY | abrupt | 20 | first non-zero sample at 0.2000 s (+0.0 ms) | PASS |
| `practice-connected.wav` | 2 | 0.4580 | IY → S | abrupt | 15 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-connected.wav` | 3 | 0.6340 | S → AA | abrupt | 15 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-connected.wav` | 4 | 0.9020 (window 0.8720–0.9320 s) | AA → M | gradual | 40 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-connected.wav` | 5 | 1.1120 | M → closure | abrupt | 10 | fade into silence (by construction) | PASS |
| `practice-connected.wav` | 6 | 1.1820 | closure → burst | abrupt | 5 | first non-zero sample at 1.1820 s (-0.0 ms) | PASS |
| `practice-connected.wav` | 7 | 1.1870 | burst → aspiration | not-graded | — | — | listed |
| `practice-connected.wav` | 8 | 1.2140 | aspiration → UW | abrupt | 10 | longest zero run within ±10 ms: 0 samples | PASS |
| `practice-connected.wav` | 9 | 1.4920 | UW → sil | abrupt | 20 | fade into silence (by construction) | PASS |

## 4b. Step or ramp? — what the answer key to Exercise 4(c) claims, measured

At each vowel→fricative boundary: the 10 %→90 % rise time of power above 4 kHz (frication arriving) and the fraction of voiced frames (Praat `To Pitch`, defaults) in the 30 ms after the key time. The key says a voiceless fricative starts as a step with voicing stopping, and the voiced one as a ramp with voicing continuing. Pass = rise time < 12 ms and voicing ≤ 20 % after a voiceless boundary; rise time ≥ 20 ms and voicing ≥ 80 % after the voiced one.

| file | boundary | high-band rise time | voiced frames after | result |
|---|---|---|---|---|
| `practice-fricatives.wav` | AA → S at 0.3280 s | 5.0 ms | 0 % | PASS |
| `practice-fricatives.wav` | IY → SH at 1.0500 s | 5.0 ms | 0 % | PASS |
| `practice-fricatives.wav` | AA → Z at 1.7540 s | 31.0 ms | 100 % | PASS |
| `practice-connected.wav` | IY → S at 0.4580 s | 3.0 ms | 0 % | PASS |

## 5. VOT — computed from the key (burst onset → voicing onset)

Class labels apply to `practice-vot.wav` only (long-lag at ≥ 40 ms, as the exercise uses the terms).

| file | token | burst onset | voicing onset | VOT | class |
|---|---|---|---|---|---|
| `practice-vot.wav` | 1 | 0.2800 s | 0.3510 s | 71.0 ms | long-lag |
| `practice-vot.wav` | 2 | 0.9290 s | 0.9469 s | 17.9 ms | short-lag |
| `practice-connected.wav` | 1 | 1.1820 s | 1.2140 s | 32.0 ms | — (not graded) |

## 6. Exercise 1, Route B — the five `synthesize-practice-vowels.praat` vowels, measured back

Synthesized here with Praat's `Create KlattGrid from vowel` using the values read from the committed script (duration 0.4 s, pitch 120 Hz, B1 50, B2 70, F3 2800, B3 110, F4 3600, bandwidth fraction 0.05, formant interval 1000 Hz), then `To Sound` and the module's `To Formant (burg)` settings. This is what the Exercise 1 answer key quotes; Route A (the VowelEditor) synthesizes differently and may differ in detail.

| vowel | true F1 / F2 | 5,500 Hz (Praat default) | 5,000 Hz | 3,000 Hz (too low) | 8,000 Hz (too high) |
|---|---|---|---|---|---|
| FLEECE | 350 / 2400 | 360 / 2399 / 2799 | 359 / 2392 / 2778 | 357 / 634 / 1733 | 2530 / 3383 / 4813 |
| KIT | 480 / 2000 | 482 / 2010 / 2798 | 480 / 1995 / 2776 | 478 / 658 / 1778 | 476 / 2408 / 3406 |
| DRESS | 620 / 1850 | 609 / 1844 / 2797 | 606 / 1826 / 2772 | 601 / 709 / 1841 | 714 / 2373 / 3350 |
| TRAP | 800 / 1700 | 812 / 1689 / 2799 | 806 / 1679 / 2777 | 642 / 828 / 1681 | 1372 / 1863 / 3200 |
| LOT | 750 / 1200 | 735 / 1201 / 2801 | 730 / 1196 / 2775 | 728 / 748 / 1202 | 1015 / 3166 / 4572 |

*(Cells are F1 / F2 / F3 as Praat labels them. At 5,500 and 5,000 Hz the pass tolerance applies and is checked; the 3,000 and 8,000 Hz columns document what a wrong ceiling does and are not graded.)*

