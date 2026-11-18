import json, importlib.util, time, sys
BASE='/home/hatch/workspace/agent-bounty/chess'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ENG = {
 'v1': load('v1', f'{BASE}/src/engine.py'),
 'v2': load('v2', f'{BASE}/src/engine-v2.py'),
 'v2-nolmr': load('v2nolmr', f'{BASE}/tests/loc/engine-v2-nolmr.py'),
 'v2-novalsort': load('v2novalsort', f'{BASE}/tests/loc/engine-v2-novalsort.py'),
}
def full_moves(trial_dir, game_n):
    g = json.load(open(f'{BASE}/tests/{trial_dir}/data/gauntlet.json'))
    opening = [x['opening']['moves'] for x in g['games'] if x['game']==game_n][0]
    seq = list(opening)
    for ln in open(f'{BASE}/tests/{trial_dir}/state/export/transcript.ndjson'):
        e = json.loads(ln)
        if e.get('game') != game_n: continue
        if e['kind'] == 'start':
            if e.get('house_move'): seq.append(e['house_move'])
        elif e['kind'] == 'move':
            seq.append(e['move'])
            if e.get('house_move'): seq.append(e['house_move'])
    return seq
POSITIONS = [
 ('trial0 g1 ply23', 'env0-v1', 1, 22, 'e1g1', 'c1d2'),
 ('trial0 g6 ply18', 'env0-v1', 6, 17, 'e5d4', 'h7h6'),
 ('trial2 g2 ply24', 'env2-v1', 2, 23, 'e8g8', 'c6e5'),
 ('trial2 g4 ply22', 'env2-v1', 4, 21, 'e8c8', 'a8d8'),
]
START='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
for label, tdir, gn, npre, m1, m2 in POSITIONS:
    seq = full_moves(tdir, gn)
    prefix = seq[:npre]
    print(f'== {label} | prefix({npre}): {" ".join(prefix)} | v1={m1} v2={m2}', flush=True)
    for name, E in ENG.items():
        p = E.sf(E.Pos(), START)
        for u in prefix:
            E.mk(p, E.pu(u))
        E.TT = {}; E.seen = set(); E.nodes = 0
        t0=time.time()
        best = E.sr(p)
        dt=time.time()-t0
        print(f'   {name:14s} -> {E.tu(best)}  nodes={E.nodes}  {dt:.1f}s', flush=True)
