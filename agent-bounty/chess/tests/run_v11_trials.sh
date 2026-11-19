#!/bin/bash
# v11 (sunfish Texel-tuned PST port on top of v3; packed 4,078 bytes)
# practice trials 0 and 2 (trial 1 already done in the 02:21 round: Elo 1654).
set -u
cd ~/workspace/agent-bounty/chess
K=kit/tiny-chess-01-kit
for N in 0 2; do
  echo "=== v11 trial $N start $(date '+%H:%M:%S %Z') ==="
  bash tests/run_trial.sh $N src/main-v11.py v11
  mkdir -p tests/scores$N-v11
  MAKEFUN_OUTPUT_DIR=tests/env$N-v11/state/export \
  MAKEFUN_REFERENCE_DIR=$K/practice/trial-$N/reference \
  MAKEFUN_SCORES_DIR=tests/scores$N-v11 \
  node $K/program/scorer/score.mjs
  echo "--- trial $N scores ---"
  cat tests/scores$N-v11/scores.json 2>/dev/null || echo "SCORES MISSING for trial $N"
done
echo "=== V11 TRIALS 0+2 DONE ==="
