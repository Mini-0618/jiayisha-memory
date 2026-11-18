#!/bin/bash
# v8 (tempo bonus +10cp in ev()) practice trials 1, 0, 2 in order.
# Replicates the v3/v5/v6/v7 pipeline: run_trial.sh + official scorer.
set -u
cd ~/workspace/agent-bounty/chess
K=kit/tiny-chess-01-kit
for N in 1 0 2; do
  echo "=== v8 trial $N start $(date '+%H:%M:%S %Z') ==="
  bash tests/run_trial.sh $N src/main-v8.py v8
  mkdir -p tests/scores$N-v8
  MAKEFUN_OUTPUT_DIR=tests/env$N-v8/state/export \
  MAKEFUN_REFERENCE_DIR=$K/practice/trial-$N/reference \
  MAKEFUN_SCORES_DIR=tests/scores$N-v8 \
  node $K/program/scorer/score.mjs
  echo "--- trial $N scores ---"
  cat tests/scores$N-v8/scores.json 2>/dev/null || echo "SCORES MISSING for trial $N"
done
echo "=== ALL V8 TRIALS DONE ==="
