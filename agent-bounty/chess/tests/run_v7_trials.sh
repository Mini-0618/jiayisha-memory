#!/bin/bash
# v7 (pawn-shield king safety term) practice trials 1, 0, 2 in order.
# Replicates the v3/v5/v6 pipeline: run_trial.sh + official scorer.
set -u
cd ~/workspace/agent-bounty/chess
K=kit/tiny-chess-01-kit
for N in 1 0 2; do
  echo "=== v7 trial $N start $(date '+%H:%M:%S %Z') ==="
  bash tests/run_trial.sh $N src/main-v7.py v7
  mkdir -p tests/scores$N-v7
  MAKEFUN_OUTPUT_DIR=tests/env$N-v7/state/export \
  MAKEFUN_REFERENCE_DIR=$K/practice/trial-$N/reference \
  MAKEFUN_SCORES_DIR=tests/scores$N-v7 \
  node $K/program/scorer/score.mjs
  echo "--- trial $N scores ---"
  cat tests/scores$N-v7/scores.json 2>/dev/null || echo "SCORES MISSING for trial $N"
done
echo "=== ALL V7 TRIALS DONE ==="
