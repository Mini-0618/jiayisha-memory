#!/bin/bash
# v6 (EG king centralization boost) practice trials 1, 0, 2 in order.
# Replicates the v3/v5 pipeline: run_trial.sh + official scorer.
set -u
cd ~/workspace/agent-bounty/chess
K=kit/tiny-chess-01-kit
for N in 1 0 2; do
  echo "=== v6 trial $N start $(date '+%H:%M:%S %Z') ==="
  bash tests/run_trial.sh $N src/main-v6.py v6
  mkdir -p tests/scores$N-v6
  MAKEFUN_OUTPUT_DIR=tests/env$N-v6/state/export \
  MAKEFUN_REFERENCE_DIR=$K/practice/trial-$N/reference \
  MAKEFUN_SCORES_DIR=tests/scores$N-v6 \
  node $K/program/scorer/score.mjs
  echo "--- trial $N scores ---"
  cat tests/scores$N-v6/scores.json 2>/dev/null || echo "SCORES MISSING for trial $N"
done
echo "=== ALL V6 TRIALS DONE ==="
