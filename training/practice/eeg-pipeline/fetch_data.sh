#!/usr/bin/env bash
# fetch_data.sh -- download the eeg-pipeline practice dataset (OpenNeuro ds007069,
# "PURSUE MMN Auditory Oddball", CC0) into a LOCAL, NON-REPO directory.
#
#   ./fetch_data.sh [TARGET_DIR] [SUBJECT ...]
#
#   TARGET_DIR  where the BIDS dataset lands (default: $HOME/eeg-practice)
#               The dataset is written to TARGET_DIR/ds007069/.
#   SUBJECT     bare subject labels (default: 1001 1002)
#
# Never point TARGET_DIR inside the lab's internal repository. Raw data -- even public,
# de-identified data like this -- stays out of the repo (repo hygiene: the
# committed bundle stays small; only configs and tiny derived tables are
# committed).
#
# Downloads use OpenNeuro's public S3 bucket over plain HTTPS (no AWS
# credentials, no aws-cli needed):
#   https://s3.amazonaws.com/openneuro.org/ds007069/...
#
# After downloading, each subject's *_events.tsv is prepared for the pipeline:
# eeg-pipeline requires the BIDS events `value` column to be numeric in every
# row (it reads codes with pandas errors="raise"), but ds007069 contains one
# non-numeric "boundary" row per subject. The script keeps the original file
# as *_events.tsv.orig and writes a numeric-only version in its place. Codes
# are otherwise untouched (standard=80, deviant=70, block-start warm-up
# standards=180, stray start markers).
set -euo pipefail

ACCESSION="ds007069"
S3_BASE="https://s3.amazonaws.com/openneuro.org/${ACCESSION}"
TASK="AuditoryOddball"

TARGET_ROOT="${1:-${HOME}/eeg-practice}"
shift || true
SUBJECTS=("${@:-}")
if [[ ${#SUBJECTS[@]} -eq 0 || -z "${SUBJECTS[0]}" ]]; then
    SUBJECTS=(1001 1002)
fi

BIDS_ROOT="${TARGET_ROOT}/${ACCESSION}"
mkdir -p "${BIDS_ROOT}"

fetch() { # fetch <relative-key> <dest-path>
    local key="$1" dest="$2"
    if [[ -s "${dest}" && "${FORCE:-0}" != "1" ]]; then
        echo "  [skip] ${dest} (exists; FORCE=1 to re-download)"
        return
    fi
    mkdir -p "$(dirname "${dest}")"
    echo "  [get ] ${key}"
    # Download to a temp name and rename only on success: an interrupted
    # transfer must never leave a truncated file at ${dest}, because the -s
    # skip test above would treat it as complete on the next run.
    rm -f "${dest}.part"
    curl -fsSL --retry 3 -o "${dest}.part" "${S3_BASE}/${key}"
    mv "${dest}.part" "${dest}"
}

started=$(date +%s)
echo "Fetching ${ACCESSION} metadata -> ${BIDS_ROOT}"
fetch "dataset_description.json" "${BIDS_ROOT}/dataset_description.json"
fetch "README"                   "${BIDS_ROOT}/README"
fetch "CHANGES"                  "${BIDS_ROOT}/CHANGES"
fetch "participants.tsv"         "${BIDS_ROOT}/participants.tsv"
fetch "participants.json"        "${BIDS_ROOT}/participants.json"

for sub in "${SUBJECTS[@]}"; do
    base="sub-${sub}/eeg/sub-${sub}_task-${TASK}"
    echo "Fetching sub-${sub} (~46 MB) ..."
    fetch "${base}_eeg.set"       "${BIDS_ROOT}/${base}_eeg.set"
    fetch "${base}_eeg.json"      "${BIDS_ROOT}/${base}_eeg.json"
    fetch "${base}_channels.tsv"  "${BIDS_ROOT}/${base}_channels.tsv"
    fetch "${base}_events.tsv"    "${BIDS_ROOT}/${base}_events.tsv"

    # Prepare events for eeg-pipeline: drop rows whose `value` is non-numeric
    # (the "boundary" annotation). Original kept as *_events.tsv.orig.
    python3 - "${BIDS_ROOT}/${base}_events.tsv" <<'PYEOF'
import shutil, sys
path = sys.argv[1]
orig = path + ".orig"
with open(path, encoding="utf-8") as fh:
    lines = fh.read().splitlines()
header = lines[0].split("\t")
try:
    vcol = header.index("value")
except ValueError:
    sys.exit(f"No 'value' column in {path}")

def numeric(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

kept = [lines[0]] + [ln for ln in lines[1:] if ln.strip() and numeric(ln.split("\t")[vcol])]
dropped = len(lines) - len(kept)
if dropped:
    shutil.copyfile(path, orig)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(kept) + "\n")
    print(f"  [prep] {path}: dropped {dropped} non-numeric event row(s); original -> {orig}")
else:
    print(f"  [prep] {path}: already numeric-only; nothing to do")
PYEOF
done

elapsed=$(( $(date +%s) - started ))
echo
echo "Done in ${elapsed}s. BIDS root: ${BIDS_ROOT}"
du -sh "${BIDS_ROOT}" 2>/dev/null || true
echo
echo "Next (from this bundle directory):"
echo "  python -m eeg_pipeline.cli --config config.yaml \\"
echo "      --bids_root \"${BIDS_ROOT}\" --derivatives_root \"${BIDS_ROOT}/derivatives\" \\"
echo "      --process_data --get_metrics"
