#!/bin/bash
# v10 (isolated-pawn penalty -15cp per isolated pawn, inlined in ev(),
# bit-mask arithmetic, packed with dict 16384 -> 4,095 bytes)
# practice trials 1, 0, 2 in order.
# Replicates the v3/v5/v6/v7/v8/v9 pipeline: run_trial.sh + official scorer.
set -u
cd ~/workspace/agent-bounty/chess
K=kit/tiny-chess-01-kit
for N in 1 0 2; do
  echo "=== v10 trial $N start $(date '+%H:%M:%S %Z') ==="
  bash tests/run_trial.sh $N src/main-v10.py v10
  mkdir -p tests/scores$N-v10
  MAKEFUN_OUTPUT_DIR=tests/env$N-v10/state/export \
  MAKEFUN_REFERENCE_DIR=$K/practice/trial-$N/reference \
  MAKEFUN_SCORES_DIR=tests/scores$N-v10 \
  node $K/program/scorer/score.mjs
  echo "--- trial $N scores ---"
  cat tests/scores$N-v10/scores.json 2>/dev/null || echo "SCORES MISSING for trial $N"
done
echo "=== ALL V10 TRIALS DONE ==="
