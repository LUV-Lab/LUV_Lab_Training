<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 0cb69cd on 2026-08-21.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

---
module: 6
title: Running the lab's eeg-pipeline (config → CLI → QC)
status: READY — PI authorized 2026-08-12 (content adversarially verified against pipeline v2.2.0 the same day)
prerequisite-for: Cognition-cluster analysis (CAREER task battery)
owner: undergrad-mentor
canonical-reference: knowledge/eeg-pipeline.md
last-reviewed: 2026-08-12
---

# Module 6 — Running the lab's `eeg-pipeline` (config → CLI → QC)

**Status: READY** — PI authorized 2026-08-12; interface facts verified against pipeline v2.2.0 (= `8c31db2`) by a 15-agent adversarial pass the same day.

**Purpose.** Be able to **run the lab's own EEG pipeline** on an existing study: **edit a
study `config.yaml`, invoke the CLI, and read the QC summary** to judge whether a run went
well. This module is a **practical on-ramp** — for anything specific (every flag, every
config field, exact outputs) the **canonical source is `knowledge/eeg-pipeline.md`**, and if
that digest and the pipeline repo ever disagree, **believe the repo.**

**~Time to complete** (compute and human time are different things — keep them separate):

- **Compute:** small. Measured on the practice bundle (2 subjects, 1 core; see the bundle
  README for the exact machine): download ~90 MB ≈ **7 s**; environment setup (venv + pip,
  warm cache) ≈ **45 s**; full run (`--process_data --get_metrics`) ≈ **22 s**; metrics-only
  rerun ≈ **11 s**. On a laptop with a cold pip cache and ordinary network, expect
  **minutes, not tens of minutes**. Nothing here needs a cluster.
- **Human:** budget **~2–3 hours** — reading this module and the digest sections it points
  to, doing the run yourself, and working the exercises against the real outputs.

(No real lab data until Module 0 is passed and IRB status is confirmed — the practice
bundle below is public data and needs no IRB confirmation, but Module 0 still comes first.)

> **Why the lab has its own pipeline.** It is **configuration-driven** and built for
> **reproducibility and auditability**: outputs carry **JSON sidecars**, and per-subject QC
> (rejection rates, blink metrics, ICA decisions, per-stage timings) is logged to TSV. Your
> job is to *drive* it correctly and *read* its QC — **not** to hand-roll an ad-hoc MNE
> script (`knowledge/eeg-pipeline.md`, "When to use it").

---

## 0. Prerequisites and the data rule

- **Module 0 (ethics) passed**; for any real study, **PI has confirmed IRB status**.
- **Data privacy is load-bearing (repeat from the digest):** the lab's own raw EEG
  (`.vhdr/.vmrk/.eeg`, `.set`) and BIDS **`sourcedata/`** are identifiable and **never enter
  this repo.** They live in the PI's **approved storage**, and you point the pipeline *at*
  that storage. Only **de-identified derivatives** — group-level QC/metrics tables
  (`.tsv`/`.parquet`), a de-identified grand-average `.fif`, figures — plus the
  **`config.yaml`** (de-identified text) may be committed under a project's `analysis/`.
- **The practice data is a different case, handled the same way.** This module's bundle uses
  **OpenNeuro ds007069 (PURSUE MMN Auditory Oddball)** — public, de-identified, **CC0**
  data. The privacy norm targets *our own* community recordings, not this; the raw data
  stays out of the repo anyway, for hygiene (~46 MB/subject does not belong in git). The
  bundle's `fetch_data.sh` pulls it to a **local, non-repo directory** (default
  `$HOME/eeg-practice/`); only the config, the fetch script, and small derived tables are
  committed. Learn the habit on the easy case: **raw data never goes in the repo, ever.**

---

## 1. The mental model: one config file *is* the analysis

All behavior lives in **one YAML file**. Design choices map to config sections
(`knowledge/eeg-pipeline.md`, "Design maps to config"):
- pre-registered **ERP components** → named `metrics.erp.windows`
- **TFR band/method** → `metrics.tfr`
- **artifact thresholds** → `artifacts`
- **ICA policy** → `ica`

So "changing the analysis" usually means **editing the config**, not the code — and because
the config is committed, the analysis is auditable. **Do not invent fields**: copy a
documented config shape (the lab's MMN config in `knowledge/eeg-pipeline.md`, or the
practice bundle's `config.yaml`) and edit within it.

**Setup / provenance (from the digest):** the pipeline is installed from its canonical
source into the project's pinned env (`pip install ".[viz]"`); the study `config.yaml`
lives under `analysis/`; and the **pipeline version + commit + exact invocation are
recorded in `analysis/README.md`** so a rerun is one command. Requirements: Python ≥ 3.10;
core deps `mne, numpy, pandas, pyarrow, PyYAML, scipy` (matplotlib/seaborn via the `[viz]`
extra, needed for figures).

---

## 2. Editing a study `config.yaml` (the fields you'll actually touch)

Start from a documented config — for practice, the bundle's `config.yaml` — and change only
what the **frozen analysis plan** specifies. Common edits:
- `task:` and `bids.tasks:` — the study/task name (the bundle: `mmn` / `["AuditoryOddball"]`).
- `paths:` — `bids_root`, `derivatives_root`, `sourcedata_root` pointing to **approved
  storage** (never a repo path for raw data). The bundle leaves these `null` and passes
  `--bids_root`/`--derivatives_root` on the CLI to keep the config portable.
- `bids.subjects:` (also `sessions`/`tasks`/`runs`) — restrict which recordings a run
  discovers; bare `["1001"]` or prefixed `["sub-1001"]` both work.
- `metrics.erp.windows:` — the named ERP windows, e.g. the lab's defaults `MMN_100_250`
  (0.10–0.25 s) and `P300_250_500` (0.25–0.50 s); the bundle uses the ERP CORE measurement
  window `MMN_125_225` (0.125–0.225 s).
- `metrics.tfr:` — method (`multitaper`), `fmin`/`fmax` (e.g. 3–8 Hz for theta).
- `artifacts:` — blink and voltage rejection. **Note:** each has both fixed thresholds
  (`threshold_uv`, `pos_uv`/`neg_uv`) and an optional per-subject `auto_percentile`; when a
  percentile is set, the threshold *actually applied* is computed per subject — the QC's
  `*_uv_used` columns record what was really applied (in the bundle's real QC,
  `volt_pos_uv_used` reads ~177.8 and ~239.6 µV, not the configured 150).
- `epoching:` — `tmin`, `tmax`, `baseline`.
- `channels:` — the LUV cap has no VEOG, so the lab default is `blink_proxy_chs: ["Fp1"]`;
  the practice dataset **has true EOG** (`eog_chs`), which takes precedence.
- `ica.mode:` — `off` / `auto` / `on` (lab default `auto`: ICA runs if **either** of two
  independent triggers fires — the blink rate reaches `auto_blink_rate_per_min` (default
  15/min), **or** the max EOG–EEG channel correlation `eog_corr_max` reaches
  `ica.corr_thresh` (0.30 in the bundle)).

**Typos fail loudly — on purpose.** Since v2.1.0, config validation **rejects unknown or
misspelled keys at load**: a typo'd field name stops the run with an error naming the bad
key, instead of silently falling back to a default. Exercise 1 makes you trigger this once
so you recognize it.

**Do not** silently change thresholds or windows to make results look better — those are
part of the frozen plan; edits are the methodologist's call and must be recorded. YAML is
whitespace-sensitive: use spaces (no tabs), keep indentation consistent.

---

## 3. Invoking the CLI

The standard invocation (BIDS in, preprocess through epoching, then metrics)
(`knowledge/eeg-pipeline.md`):
```bash
# Standard: BIDS in, preprocess + metrics
# (omitting all stage flags defaults to exactly this pair)
python -m eeg_pipeline.cli --config config.yaml --process_data --get_metrics

# Metrics-only rerun (epochs already exist — fast; use when you only changed metric settings)
python -m eeg_pipeline.cli --config config.yaml --get_metrics

# One subject only (entity filters: bare "1001" or prefixed "sub-1001" both work)
python -m eeg_pipeline.cli --config config.yaml --process_data --get_metrics \
  --subjects sub-1001

# Legacy (non-BIDS) input
python -m eeg_pipeline.cli --config config.yaml --legacy \
  --raw_dir /data/legacy_raw --subject_csv_dir /data/legacy_behavior \
  --process_data --get_metrics
```
Key flags: **`--config`** (required); stages **`--process_data`**, **`--get_metrics`**,
`--plot_figures`; entity filters `--subjects`/`--sessions`/`--tasks`/`--runs`; `--legacy`
(+ `--raw_dir`, `--subject_csv_dir`), `--convert_to_bids`; `--summarize_one_file`;
`--use_gpu`; `--n_jobs`. Equivalent **wrapper scripts** exist
(`scripts/process_eeg_data.py`, `scripts/compute_eeg_metrics.py`,
`scripts/plot_eeg_figures.py`), and there is an Electron GUI prototype (`npm run oneclick`).
**Record the exact command and pipeline version in `analysis/README.md`.**

**Filtered metrics reruns are now safe — and why that matters.** At the lab's pinned release
(**v2.2.0** = commit `8c31db2`; record both tag and hash in `analysis/README.md`),
`--get_metrics --subjects sub-07`
recomputes that
subject's per-subject metrics files and then **rebuilds the dataset-level tables from all
per-subject files on disk**. It was not always so: released v2.1.0 ignores filters on
metrics-only reruns, and an earlier state of the code **overwrote the combined tables with
only the filtered subject's rows, destroying everyone else's**. This is why the lab pins
and records the pipeline version, and why "just update the pipeline" is a real task, not
busywork. If you ever see a dataset-level metrics table containing a single subject, that
is the old bug — regenerate at HEAD. (Digest: "The `--get_metrics` subject-filter fix.")

> **⚠️ Do not pass `--erp-core` — especially not on the practice bundle.** The practice
> task *is* the ERP CORE MMN paradigm, so the flag looks tempting. But the preset behaves
> like flags typed on the command line: for seven fields (re-reference, filters, voltage
> method, artifact percentiles, ICA) it **overrides your config file**, and a flag typed at
> its default value cannot beat it. The lab norm is that **the config is the single source
> of truth** — so **six of the seven** preset values are written *into* the bundle's
> `config.yaml`; the seventh, ICA, deliberately is **not**: the preset forces `ica: on`
> (always run), while the bundle keeps the lab's `ica.mode: auto` policy. That is one more
> concrete reason never to pass the flag here — it would silently flip ICA to `on` and
> change the committed outputs (the real QC has `ica_ran: False` for both subjects).
> (Digest: "ERP CORE preset" and the precedence caveat.)

The pipeline also has an **HPC/SLURM mode** (`--skip_aggregate`, `--aggregate_only`,
`--n_jobs`, `hpc/` templates) for running many subjects in parallel on a cluster — RAs will
not use it; if a project ever needs it, the digest's "HPC / SLURM mode" section is the
reference.

---

## 4. Reading the QC summary

The pipeline writes a dataset-level **`desc-summary_qc.tsv`** (one row per recording
outcome, 59 columns in the practice bundle's real output) plus metrics tables
(`desc-erp_metrics.tsv`, `desc-tfr_metrics.tsv`, `desc-erp_timeseries.parquet`), and — at
the commit the lab runs — **the same QC row(s) also land next to each recording's own
derivatives** (`sub-*_desc-summary_qc.tsv`), even for recordings that crashed, so nothing
vanishes from QC.

**Sidecars and provenance — read the right file.** Every derivative gets a JSON sidecar,
but the depth differs: **full parameter provenance** (filter/re-reference/epoching/
artifact/ICA settings) is written on the **per-subject data files** from `--process_data`;
QC and table sidecars carry **no parameter provenance** — only a `Description`, plus (on
the QC sidecar) a `GeneratedBy` stanza naming the pipeline and its version. To know what
parameters a run used, read
the per-subject `.fif` sidecars or the config — never a table's sidecar. **Sidecars are
machine-written provenance; never delete or hand-edit them.**

Each QC row carries a **`status`** (`OK`, `ERROR`, or a `SKIP_*` code such as
`SKIP_REJECT_RATE`), epoch/rejection counts, blink and ICA diagnostics and decisions,
`review_flag`/`review_reasons`, and **per-stage wall-clock timings**
(`t_preprocess_s, t_ica_s, t_epoching_s, t_metrics_s, t_io_s`) that say where the time
went. Aggregation excludes any recording whose latest status is not `OK`. Read the table
to answer: *did each subject yield enough clean data?*
- **High `epoch_reject_rate` / low `n_epochs_final`** → noisy recording (movement, bad
  electrode, high impedance) → few usable trials → flag for review. (The config's
  `artifacts.max_reject_rate` — 0.5 in the bundle — auto-skips a subject above it.)
- **High `blink_rate_per_min`** → the participant blinked through stimuli (ties back to
  Module 5 in-session behavior); at ≥ 15/min, `ica.mode: auto` triggers ICA (blink rate is
  one of auto mode's two triggers — high `eog_corr_max` is the other; see §2).
- **`ica_ran` / `ica_applied` / `ica_exclude`** → what the ICA policy actually did; an
  unusually high exclusion count is worth a look.

You **flag** anomalies to the data-analyst/methodologist; **you do not decide exclusions
yourself** — those follow the frozen analysis plan.

---

## Exercises  *(practice bundle — real public data, real outputs)*

Use the practice bundle at **`people/training/practice/eeg-pipeline/`**: a real config, a
fetch script, and **real pipeline outputs** generated from **OpenNeuro ds007069 (PURSUE MMN
Auditory Oddball, CC0)** — nothing synthetic, nothing hand-edited. Read its `README.md`
first; run `./fetch_data.sh` to pull the 2 practice subjects (~90 MB) to a local, non-repo
directory, and reproduce the run with the commands documented there.

**Exercise 1 — Edit the config.** Starting from the bundle's `config.yaml`, write the YAML
changes to (a) restrict the run to sub-1001 only (in the config, not on the CLI), (b) add
an ERP window `P300_250_500` from 0.25–0.50 s alongside `MMN_125_225`, and (c) enforce a
**fixed** voltage rejection of ±120 µV — actually applied, not just written down (hint:
check the real QC's `volt_pos_uv_used` column against the configured `pos_uv` first). Show
only the changed lines and name their config sections. Then: you fat-finger
`thresold_uv:` under `artifacts.blink:` — what happens when you run, and why is that the
behavior you want?

**Exercise 2 — Pick the command.** The bundle's `outputs/` were refreshed after a change to
`metrics.tfr.time_decim` only; epochs already existed. (a) Which single invocation redoes
just the metrics, and about how long does it take on the practice data versus the full run?
(b) Now you want to recompute metrics for sub-1002 alone: is
`--get_metrics --subjects sub-1002` safe to run, and what would it have done on older
versions of the pipeline?

**Exercise 3 — Read the QC.** Open the bundle's real `outputs/eeg/desc-summary_qc.tsv`
(59 columns; the ones below are a selection). The first two rows are **real**; the third is
a **constructed example** for the flagging exercise — it is *not* in the bundle's real
output, and its numbers are invented for teaching:

| subject | status | n_epochs_final | epoch_reject_rate | blink_rate_per_min | ica_ran | t_metrics_s |
|---|---|---|---|---|---|---|
| sub-1001 *(real)* | OK | 953 | 0.032 | 1.42 | False | 3.34 |
| sub-1002 *(real)* | OK | 950 | 0.036 | 6.83 | False | 3.52 |
| sub-9999 *(constructed example)* | OK | 581 | 0.410 | 34.2 | True | 3.4 |

(a) On the **real** rows: did ICA run for either subject, and why or why not, given the
bundle config? Which processing stage dominated the runtime, per the `t_*_s` columns? And
look at the real file's `behavior_source_path` column — what do you notice about the paths,
and what does that tell you about where the committed outputs were generated? (b) On the
**constructed** sub-9999 row: would you flag it, on what evidence, and what do you do next
(and not do)? Why did the pipeline *not* auto-skip it, given the bundle's
`max_reject_rate: 0.5`?

---

## Answer key

**Ex. 1.**
- (a) Under `bids:`, set `subjects: ["1001"]` (or `["sub-1001"]` — bare and prefixed labels
  both work). Section: `bids` (discovery filters).
- (b) Under `metrics.erp.windows:`, **add** a list item
  `- { name: "P300_250_500", tmin: 0.25, tmax: 0.50 }` alongside `MMN_125_225` (don't
  delete the existing window). Section: `metrics.erp`.
- (c) Under `artifacts.voltage:`, set `pos_uv: 120.0`, `neg_uv: -120.0` **and**
  `auto_percentile: null`. The bundle config ships `auto_percentile: 97.5`, so the
  threshold actually applied is computed per subject — that is why the real QC's
  `volt_pos_uv_used` reads ~177.8 µV (sub-1001) and ~239.6 µV (sub-1002), not the
  configured 150. Leave the percentile in place and your ±120 is dead text; the
  `*_uv_used` QC columns are where you verify what a run really applied. Section:
  `artifacts`.
- Typo: the run **fails at config load** with an error naming the unknown key — since
  v2.1.0, validation rejects unknown/misspelled keys. That is the behavior you want:
  before, a typo'd field was silently ignored and the default (75.0 µV) used, and nothing
  told you. Loud and early beats silent and wrong. (In a real study, all of (a)–(c) must
  match the frozen analysis plan, not be chosen ad hoc.)

**Ex. 2.**
- (a) `python -m eeg_pipeline.cli --config config.yaml --bids_root "$D" --derivatives_root
  "$D/derivatives" --get_metrics` — a **metrics-only rerun** reuses the existing derivative
  epochs and skips preprocessing/epoching. Measured on the bundle: **~11 s** versus ~22 s
  for the full run — and on real-sized studies the gap is what makes iteration on metric
  settings practical. (This exact command is step 4 of the bundle README's "Reproduce"
  section — it is the run that built `outputs/`.)
- (b) **Safe at the lab's pinned release** (**v2.2.0** = `8c31db2`): it
  recomputes sub-1002's per-subject
  metrics files, then rebuilds the dataset-level tables **from all per-subject files on
  disk**, so sub-1001's rows survive. On released v2.1.0 the filter is silently ignored
  (every subject recomputed); on an earlier state of the code the filtered rerun
  **overwrote the combined tables with only sub-1002's rows, destroying sub-1001's**. Same
  command, three behaviors — which is why the pipeline version is pinned and recorded in
  `analysis/README.md`, and why you never assume flag semantics across versions without
  checking the digest.

**Ex. 3.**
- (a) **ICA ran for neither real subject**: `ica.mode: auto` has **two** independent
  triggers — blink rate ≥ `auto_blink_rate_per_min: 15.0` **or** `eog_corr_max` ≥
  `ica.corr_thresh: 0.30` — and both rows clear neither: measured blink rates are **1.42**
  and **6.83**/min (< 15), and `eog_corr_max` is **0.235** and **0.115** (< 0.30)
  (`ica_ran: False`; blink detection used the dataset's true EOG channels — see
  `blink_source`). The slowest stage was **metrics** (`t_metrics_s` ≈ 3.3–3.5 s,
  versus ~1.2–2.5 s preprocessing) — the TFR computation dominates on this small, clean
  data. The `behavior_source_path` values read `BUILD_DIR/...`: in the lab's internal
  fixtures they record the **build session's** working directory (QC is a machine-written
  record of the run that actually happened); in this public mirror that internal path was
  substituted with the constant `BUILD_DIR` at publish time — the only alteration, with
  every numeric value byte-identical to the internal record. Your own rerun will show
  *your* real paths, and QC files should never be hand-edited to look tidier.
- (b) **Flag sub-9999** *(constructed example — these numbers are invented for teaching)*:
  `epoch_reject_rate` **0.410** versus ~0.03 for its peers, only **581** epochs kept, and
  `blink_rate_per_min` **34.2** — which is ≥ 15, so `auto` mode ICA fired
  (`ica_ran: True`), consistent with a blink-heavy session. It was not auto-skipped
  because 0.410 < the config's `max_reject_rate: 0.5` — the automatic gate only catches
  the extreme cases, which is exactly why a human reads the QC. **Do:** report it to the
  data-analyst/methodologist; check its per-subject QC file, sidecars, and the session log
  for causes (impedances, movement). **Don't:** decide on your own to drop sub-9999 —
  exclusions follow the frozen plan, not an RA's judgment.

---

## Competence check *(PI-verifiable in minutes)*

On the **practice bundle** (`people/training/practice/eeg-pipeline/`), the RA:
- **Reproduces the run** from the bundle README (fetch → install → full run) and gets QC
  matching the committed `outputs/` (both subjects `OK`, ~3% rejection).
- Correctly **edits a config field** with valid YAML, and can say what happens to a
  misspelled key (rejected at load) and which QC column shows the threshold actually
  applied (`*_uv_used`).
- States the **right CLI command** for a metrics-only rerun, why it is fast, and whether
  `--subjects` filtering is safe at the lab's pinned commit.
- **Reads the real QC table** — why ICA didn't run, where the time went (`t_*_s`) — and,
  on the constructed bad-subject row, flags it *with the right evidence* while stating
  that **exclusion decisions are not the RA's to make.**
- Can point to **`knowledge/eeg-pipeline.md`** as the canonical reference, name the
  **data-privacy rule** (raw/`sourcedata` never in the repo; only de-identified
  derivatives + config), and say why the CC0 practice data stays out of the repo anyway.

This check is output-based and can be **delegated to the data-analyst or Lab Manager** to
verify, with the PI spot-checking.
