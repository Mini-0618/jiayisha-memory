#!/bin/bash
# v9 (doubled-pawn penalty -15cp per extra pawn on a file, inlined in ev(),
# urllib.request aliased to W to fit 4,096 bytes) practice trials 1, 0, 2 in order.
# Replicates the v3/v5/v6/v7/v8 pipeline: run_trial.sh + official scorer.
set -u
cd ~/workspace/agent-bounty/chess
K=kit/tiny-chess-01-kit
for N in 1 0 2; do
  echo "=== v9 trial $N start $(date '+%H:%M:%S %Z') ==="
  bash tests/run_trial.sh $N src/main-v9.py v9
  mkdir -p tests/scores$N-v9
  MAKEFUN_OUTPUT_DIR=tests/env$N-v9/state/export \
  MAKEFUN_REFERENCE_DIR=$K/practice/trial-$N/reference \
  MAKEFUN_SCORES_DIR=tests/scores$N-v9 \
  node $K/program/scorer/score.mjs
  echo "--- trial $N scores ---"
  cat tests/scores$N-v9/scores.json 2>/dev/null || echo "SCORES MISSING for trial $N"
done
echo "=== ALL V9 TRIALS DONE ==="
