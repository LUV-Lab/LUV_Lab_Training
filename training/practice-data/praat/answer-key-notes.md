<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 0fa324c8 on 2026-09-04.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# answer-key-notes.md — grader's notes for the Module 2 fixtures

**Do not open this until you have finished Exercise 4.** It states what each fixture was
built to contain. The graded numbers themselves are in `segmentation-key.csv` (machine-written)
and `verification-report.md` (machine-written); this file is the design intent behind them, in
prose, for the person grading. It is deliberately **not linked from `README.md`** — it was
moved out of the README on 2026-09-02 (red-team review of 2026-08-30, finding M4) because the
module quarantines the key and then sent students to a README that gave the answers away.

Owner: undergrad-mentor. Last aligned with the fixtures: **2026-09-02** (fixtures rebuilt the
same day; every number below is from that day's `segmentation-key.csv` and
`verification-report.md`, Praat 6.1.38). If the generator changes, re-run the verifier and
re-check this file against it. *Two hand-copied numbers here drifted from the machine-written
files and were caught by the 2026-09-02 red-team re-check (m-3); both are corrected below with a
note. This file is hand-written prose — it is corrected by hand; the key and the report never are.*

## `formants-practice.csv` — Exercise 2

Four seeded items across five rows: `P01-003` (`keep`, skipped formant), `P02-002` (`people`,
lost F1), `P01-006` (`did`, 0.031 s — below the 0.05 s floor), and `P01-012` + `P02-012`
(`hand`, pre-nasal /æ/ raised and fronted in **both** speakers — not an error). The module's
Ex. 2 answer key has the full table.

## `practice-vowels.wav` — Exercise 4(a)

- Vowel onsets **0.250 / 0.950 / 1.650 s**, offsets **0.650 / 1.350 / 2.050 s**; ±20 ms.
- Bonus (formants): the vowels are the generator's `M` targets — **IY 320/2200/2900, AA
  720/1200/2500, UW 350/1050/2350** (F1/F2/F3). Praat's own medians over the middle 20–80 % at
  the 5,000 Hz ceiling (report §1): **IY 346/2195/2909 · AA 715/1203/2492 · UW 348/1051/2340**.
  Pass = within the ratified ±50/±100 of the targets. At 5,500 Hz the values are within 15 Hz of
  those. The fixture speaker is male-range (F0 ≈ 110–120 Hz), so 5,000 Hz is the ceiling the
  module prescribes for it.

## `practice-vot.wav` — Exercise 4(b)

- Token 1: burst **0.280**, voicing onset **0.351** → **VOT 71.0 ms, long-lag**.
- Token 2: burst **0.929**, voicing onset **0.947** → **VOT 17.9 ms, short-lag**.
- ±5 ms on bursts, ±10 ms on voicing onsets. The `sil → closure` boundaries (0.200, 0.849 —
  *0.847 corrected to the key's row 13, 2026-09-02, re-check m-3*) are
  `not-markable` — a closure after silence has no acoustic onset in these files — and
  `burst → aspiration` is `not-graded`. *(Until 2026-09-02 the key graded the closure onset at
  ±10 ms; review M2.)*

## `practice-fricatives.wav` — Exercise 4(c)

- `S` **0.328–0.544**, `SH` **1.050–1.266**, both ±15 ms.
- `Z` **1.754–1.934**, ±30 ms, both of its boundaries `gradual` with windows **1.734–1.774** and
  **1.914–1.954**.
- **The hardest one is `Z`, and the reason is in the signal** (report §§3–4b): Praat finds
  **100 % voiced frames** inside `Z` (HNR ≈ 6.3 dB — *6.5 corrected to report §3, 2026-09-02,
  re-check m-3*) and **0 %** inside `S` and `SH`; frication
  above 4 kHz rises to full level within a few milliseconds at the vowel→`S` join but across a
  ~40 ms window at vowel→`Z`, with voicing continuing throughout. A step versus a ramp. *(The
  2026-08-28 audio did not contain this contrast — review B2 — which is why the file was
  rebuilt.)*

## `practice-connected.wav` — Exercise 4(d)

- Nine boundaries: sil→IY **0.200** (±20) · IY→S **0.458** (±15) · S→AA **0.634** (±15) ·
  **AA→M 0.902, `gradual`, ±40, window 0.872–0.932** · M→closure **1.112** (±10) ·
  closure→burst **1.182** (±5) · burst→aspiration 1.187 (not graded) · aspiration→UW
  **1.214** (±10) · UW→sil **1.492** (±20).
- The one that matters is the vowel-to-nasal boundary. A student who marks anywhere in
  0.872–0.932 is right; one who flags it and gives the window is more right.
- The stop in this file has a 32 ms VOT; it is not graded for category.

## What the fixtures deliberately do **not** contain

No coarticulation, no breath noise, no room. Joins between sounds are 4 ms crossfades (not
fades to zero, as they were before 2026-09-02 — review M7), so there is no amplitude notch to
"find", but the boundaries are still far cleaner than any recording. The module's "What these
fixtures cannot teach you" paragraph is the honest statement of that limit; grade against it.
