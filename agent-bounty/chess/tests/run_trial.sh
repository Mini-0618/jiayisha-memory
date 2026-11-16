#!/bin/bash
# usage: run_trial.sh <trial_n> <bot_main.py> <tag>
N=$1; BOT=$2; TAG=$3
K=~/workspace/agent-bounty/chess/kit/tiny-chess-01-kit
W=~/workspace/agent-bounty/chess/tests/env$N-$TAG
mkdir -p $W/data $W/state
cp $K/practice/trial-$N/input/env/gauntlet.json $W/data/
MAKEFUN_ENV_DATA_DIR=$W/data MAKEFUN_STATE_DIR=$W/state MAKEFUN_ENV_PORT=$((8900+N)) \
  node $K/program/env/server.mjs > $W/env.log 2>&1 &
ENVPID=$!
sleep 2
MAKEFUN_ENV_URL=http://127.0.0.1:$((8900+N)) MAKEFUN_TRIAL_SEED=localtest \
  timeout 1700 python3 "$BOT" > $W/bot.log 2>&1
echo "bot exit: $?"
kill $ENVPID 2>/dev/null
ls $W/state/
