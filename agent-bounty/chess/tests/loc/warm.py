import json, importlib.util, time
BASE='/home/hatch/workspace/agent-bounty/chess'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
V2 = load('v2w', f'{BASE}/src/engine-v2.py')
V1 = load('v1w', f'{BASE}/src/engine.py')
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
START='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# (label, trial_dir, game, our-colour-parity: our moves at even idx if black)
CASES = [
 ('trial2 g4 v2 (expect a8d8 at ply22)', 'env2-v2', 4, 21, 'a8d8'),
 ('trial0 g1 v2 (expect c1d2 at ply23)', 'env0-v2', 1, 22, 'c1d2'),
 ('trial0 g6 v2 (expect h7h6 at ply18)', 'env0-v2', 6, 17, 'h7h6'),
]
for label, tdir, gn, div_idx, expect in CASES:
    seq = full_moves(tdir, gn)
    print(f'== {label}', flush=True)
    V2.TT = {}
    # replay our moves up to and including divergence, warm TT, like play()
    for idx in range(0, div_idx+1):
        if (gn in (1,) and idx % 2 == 0) or True:
            pass
    # our moves are at indices with same parity as div_idx (divergence is our move)
    for idx in range(0, div_idx+1):
        if idx % 2 != div_idx % 2: continue
        p = V2.sf(V2.Pos(), START)
        for u in seq[:idx]:
            V2.mk(p, V2.pu(u))
        V2.seen = set()
        for u in seq[:idx]:
            # rebuild seen like play(): hashes of positions along the game
            pass
        # seen: play() adds p.h after each applied move from start_fen
        q = V2.sf(V2.Pos(), START)
        for u in seq[:idx]:
            V2.seen.add(q.h); V2.mk(q, V2.pu(u))
        V2.seen.add(q.h)
        t0=time.time()
        best = V2.sr(p)
        print(f'   ply {idx+1}: warm-TT v2 -> {V2.tu(best)} (transcript {seq[idx]}) {"OK" if V2.tu(best)==seq[idx] else "MISMATCH"} {time.time()-t0:.1f}s TTsize={len(V2.TT)}', flush=True)
