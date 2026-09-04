<!-- Public mirror of the LUV Lab training corpus (luv-lab.info).
     Published from the lab's internal repository @ 0fa324c8 on 2026-09-04.
     Materials: CC BY 4.0 · Scripts: MIT (see repository README).
     Internal cross-references (roster, handbook, project analyses) may not resolve here. -->

# eeg-pipeline practice bundle — real OpenNeuro data

Hands-on practice data for the `people/training/eeg-pipeline-run.md` module.
Everything in `outputs/` is **real pipeline output** generated from public
OpenNeuro data with the commands documented below — nothing is synthetic or
hand-edited.

Built 2026-08-12 against **eeg-pipeline v2.2.0 (tag = commit `8c31db2`)** — see
`knowledge/eeg-pipeline.md` for the interface digest. The first build ran at the
code-identical pre-bump commit `b3cdd52`; `outputs/` was regenerated under
v2.2.0 the same day. Every scientific value was identical between the two runs;
only the wall-clock `t_*_s` timing columns moved.

## Dataset provenance

| | |
|---|---|
| Dataset | **PURSUE MMN Auditory Oddball** |
| Accession | **OpenNeuro ds007069**, v1.0.0 |
| DOI | doi:10.18112/openneuro.ds007069.v1.0.0 |
| License | **CC0** (public domain dedication) |
| Authors | Couperus, J.W.; Bukach, C.M.; Reed, C.L. |
| Size | 280 participants; ~46 MB per subject (EEGLAB `.set`, 500 Hz, 29 EEG + 3 EOG, actiCHamp) |
| Task | Passive auditory oddball using the **ERP CORE MMN task design** (Kappenman et al., 2021, NeuroImage 225:117465) |
| Event codes | standard = 80, deviant = 70, block-start warm-up standards = 180 |

**Relation to ERP CORE:** the ERP CORE datasets themselves are hosted on OSF
(CC BY-SA), not OpenNeuro. What OpenNeuro hosts is the PURSUE project's data
(pursueerp.com) — recorded at three primarily-undergraduate institutions using
the ERP CORE MMN paradigm, expressly for undergraduate EEG training, which is
exactly this module's purpose. The pipeline's `--erp-core` preset parameters
apply to it directly (this bundle's `config.yaml` writes those values into the
config instead of using the flag, so the config stays the single source of
truth — the preset would otherwise *override* config values; see the digest).

**Accession verification (2026-08-12):** openneuro.org itself was egress-blocked
in the build environment, so the accession was verified against OpenNeuro's two
official distribution channels: the public S3 bucket
(`https://s3.amazonaws.com/openneuro.org/ds007069/dataset_description.json`,
which names the dataset, authors, license, and DOI quoted above) and the
OpenNeuroDatasets GitHub mirror (`OpenNeuroDatasets/ds007069`). Widely repeated
claims that ERP CORE proper lives on OpenNeuro (e.g. under ds004660) were
checked the same way and found to be wrong.

## Why the raw data is not committed

This is public, de-identified, CC0 data — the lab's raw-data privacy norm
targets **our own identifiable community recordings**, not this. It stays out
of the repo anyway, for hygiene: ~46 MB per subject does not belong in git.
Committed here: the config, the fetch script, and ~1.4 MB of dataset-level
derived tables. Raw data and per-subject derivatives (~180 MB for two
subjects) live outside the repo (default `$HOME/eeg-practice/`).

## Contents

```
config.yaml       practice config (BIDS mode, ERP CORE-style parameters,
                  MMN_125_225 window, theta TFR) — Exercise 1 edits this
fetch_data.sh     downloads N subjects (default 1001 1002) from OpenNeuro S3
                  via plain HTTPS and prepares the events files (see below)
outputs/          REAL dataset-level outputs from the run documented below:
  dataset_description.json            derivatives dataset descriptor
  eeg/desc-summary_qc.tsv (+.json)    QC: 1 row/recording, 59 cols — Exercise 3
  eeg/desc-erp_metrics.tsv (+.json)   ERP windowed metrics (MMN_125_225)
  eeg/desc-tfr_metrics.tsv (+.json)   theta TFR metrics (time_decim: 4)
  eeg/desc-erp_timeseries.parquet (+.json)  ERP time-series (figure input)
  eeg/task-AuditoryOddball_desc-grandaverage-{standard,deviant}_ave.fif (+.json)
```

Not committed (regenerate locally): per-subject `desc-preproc_eeg.fif`,
`_epo.fif`, per-subject metrics/QC/evokeds — everything under
`derivatives/eeg-pipeline/sub-*/`.

## Reproduce (the commands that built `outputs/`)

One substitution: the recorded run used the build session's scratchpad
directory as `TARGET_DIR`, not `$HOME/eeg-practice`. That is why absolute paths
inside `outputs/` — the `SourceDatasets` URL in `dataset_description.json` and
the `behavior_source_path` column in `desc-summary_qc.tsv` — show a `BUILD_DIR/...`
prefix: the build machine's real directory was substituted with the constant
`BUILD_DIR` when this public mirror was published — the only alteration to these
machine-written files, with all numeric content byte-identical to the internal
record (Exercise 3 will make you notice these paths). Use any directory you like as `TARGET_DIR`; subjects, flags,
and config below are verbatim from the recorded run.

```bash
# 1. Get the data (2 subjects, ~90 MB with metadata)
./fetch_data.sh "$HOME/eeg-practice" 1001 1002

# 2. Install the pipeline (from the lab's clone, or github.com/berrygrant/eeg-pipeline)
git clone --branch v2.2.0 https://github.com/berrygrant/eeg-pipeline
python3 -m venv eegenv && ./eegenv/bin/pip install -e "./eeg-pipeline[viz]"

# 3. Full run: preprocess -> epochs -> evokeds -> metrics -> aggregation
D="$HOME/eeg-practice/ds007069"
python -m eeg_pipeline.cli --config config.yaml \
  --bids_root "$D" --derivatives_root "$D/derivatives" \
  --process_data --get_metrics

# 4. Metrics-only rerun (this is what refreshed outputs/ after the TFR
#    time_decim change — Exercise 2's scenario)
python -m eeg_pipeline.cli --config config.yaml \
  --bids_root "$D" --derivatives_root "$D/derivatives" \
  --get_metrics
```

**Events preparation (done by `fetch_data.sh`, step 1):** eeg-pipeline requires
the BIDS events `value` column to be numeric in every row; ds007069 has one
non-numeric `boundary` row per subject, which would otherwise error that
recording. The script drops non-numeric rows (keeping the original as
`*_events.tsv.orig`). The events files carry a numeric `sample` column, so the
pipeline uses those positions directly — no alignment heuristics run.

## Measured timings (this build; containerized Linux, Python 3.11.15, MNE 1.12.1, 1 core, `n_jobs: 1`)

| Step | Wall clock |
|---|---|
| Download, 2 subjects + metadata (~90 MB) | 7 s |
| `python3 -m venv` | 5 s |
| `pip install -e ".[viz]"` (warm PyPI cache) | 39 s |
| Full run, 2 subjects (`--process_data --get_metrics`) | 22 s total |
| — per-subject stages (from QC): preprocess 1.2–2.5 s, ICA check 0.4–0.9 s, epoching 0.25 s, metrics 3.3–3.5 s, I/O 0.8 s | ~8 s/subject |
| Metrics-only rerun, 2 subjects (`--get_metrics`) | 11 s |

Times on a laptop with network-dependent download and cold pip cache will be
higher (expect minutes, not tens of minutes). The per-stage numbers come from
the QC table's `t_<stage>_s` columns — reading them **is** part of the module.

## What the outputs show (for checking your own rerun)

- Both subjects `status: OK`; epoch rejection 3.2% / 3.6% (32 and 35 of 985);
  ICA in `auto` mode did **not** trigger (blink rates 1.4 and 6.8 per min,
  threshold 15) — blink detection used the real EOG channels.
- A clean MMN: `DEV_MINUS_STD` mean amplitude in 125–225 ms at Fz of
  **−3.00 µV** (sub-1001) and **−4.76 µV** (sub-1002), peaks ~150–170 ms —
  textbook ERP CORE MMN morphology.
- If your rerun of the same subjects with an unmodified `config.yaml` differs
  by more than floating-point noise, something is wrong — diff your config
  first.

## Version notes

- Pipeline installed editable from the lab clone of
  `github.com/berrygrant/eeg-pipeline` at **v2.2.0** (= `8c31db2`). The
  per-subject QC files (`sub-*_desc-summary_qc.tsv`), per-stage `t_*_s` timing
  columns, and the safe `--get_metrics --subjects` semantics used here are
  **new in v2.2.0** — install from the tag as above; a plain
  `pip install eeg-pipeline==2.1.0` will not have them.
- Dataset pinned at ds007069 v1.0.0 (the only version as of 2026-08-12).
  `fetch_data.sh` reads the bucket's current state; if OpenNeuro publishes a
  new version, re-verify event codes before trusting old expected values.
