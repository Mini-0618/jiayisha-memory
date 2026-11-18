import json, importlib.util, time
BASE='/home/hatch/workspace/agent-bounty/chess'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
V1 = load('v1d', f'{BASE}/src/engine.py')
V2 = load('v2d', f'{BASE}/src/engine-v2.py')
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
def sr_trace(E, p, cap):
    # replicate sr() but report last completed depth + best + root score
    E.NODE_CAP = cap; E.nodes = 0; E.TT = {}; E.seen = set()
    side = p.side; legal = []
    for m in E.gm(p):
        E.mk(p, m)
        if not E.at(p, p.ksq[side], 1-side): legal.append(m)
        E.um(p)
    best = legal[0]; depth = 1; last_score = None
    try:
        while depth <= 64:
            scored = sorted(((E.ms(p, m, best, 0), m) for m in legal), reverse=True)
            alpha = -E.MATE - 1; cur = best
            for _, m in scored:
                E.mk(p, m)
                if p.h in E.seen: v = 0
                else:
                    E.seen.add(p.h); v = -E.nx(p, depth-1, -E.MATE-1, -alpha, 1, True); E.seen.discard(p.h)
                E.um(p)
                if v > alpha: alpha = v; cur = m
            best = cur; last_score = alpha; depth += 1
    except E.Stop:
        pass
    return E.tu(best), depth-1, last_score, E.nodes
POSITIONS = [
 ('trial0 g1 ply23', 'env0-v1', 1, 22, 'e1g1', 'c1d2'),
 ('trial0 g6 ply18', 'env0-v1', 6, 17, 'e5d4', 'h7h6'),
 ('trial2 g2 ply24', 'env2-v1', 2, 23, 'e8g8', 'c6e5'),
]
for label, tdir, gn, npre, m1, m2 in POSITIONS:
    seq = full_moves(tdir, gn)
    print(f'== {label} v1={m1} v2={m2}', flush=True)
    for name, E in [('v1-70k', V1), ('v2-70k', V2)]:
        p = E.sf(E.Pos(), START)
        for u in seq[:npre]: E.mk(p, E.pu(u))
        t0=time.time()
        b, d, s, n = sr_trace(E, p, 70000)
        print(f'   {name}: best={b} completed-depth={d} rootscore={s} nodes={n} {time.time()-t0:.1f}s', flush=True)
    # deep reference: v1 at 400k cap
    p = V1.sf(V1.Pos(), START)
    for u in seq[:npre]: V1.mk(p, V1.pu(u))
    t0=time.time()
    b, d, s, n = sr_trace(V1, p, 400000)
    print(f'   v1-400k(deep ref): best={b} completed-depth={d} rootscore={s} nodes={n} {time.time()-t0:.1f}s', flush=True)
