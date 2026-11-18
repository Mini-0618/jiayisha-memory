import json, importlib.util, time
exec(open('/home/hatch/workspace/agent-bounty/chess/tests/loc/depthprobe.py').read().split('POSITIONS = [')[0])
POSITIONS = [
 ('trial0 g4 ply10 (5...f5?)', 'env0-v1', 4, 9, 'e4d6', 'f7f5'),
 ('trial2 g4 ply22 (O-O-O vs Rd8)', 'env2-v1', 4, 21, 'e8c8', 'a8d8'),
]
for label, tdir, gn, npre, m1, m2 in POSITIONS:
    seq = full_moves(tdir, gn)
    print(f'== {label} v1={m1} v2={m2}', flush=True)
    for name, E, cap in [('v1-70k', V1, 70000), ('v2-70k', V2, 70000)]:
        p = E.sf(E.Pos(), START)
        for u in seq[:npre]: E.mk(p, E.pu(u))
        t0=time.time()
        b, d, s, n = sr_trace(E, p, cap)
        print(f'   {name}: best={b} completed-depth={d} rootscore={s} nodes={n} {time.time()-t0:.1f}s', flush=True)
    p = V1.sf(V1.Pos(), START)
    for u in seq[:npre]: V1.mk(p, V1.pu(u))
    t0=time.time()
    b, d, s, n = sr_trace(V1, p, 400000)
    print(f'   v1-400k(deep ref): best={b} completed-depth={d} rootscore={s} nodes={n} {time.time()-t0:.1f}s', flush=True)
    # score both candidates with v1 fixed-depth-6 nx, fresh TT each, from side to move
    for cand in (m1, m2):
        p = V1.sf(V1.Pos(), START)
        for u in seq[:npre]: V1.mk(p, V1.pu(u))
        V1.TT = {}; V1.seen = set(); V1.nodes = 0; V1.NODE_CAP = 10**9
        mv = V1.pu(cand)
        V1.mk(p, mv)
        try:
            v = -V1.nx(p, 5, -V1.MATE-1, V1.MATE+1, 1, True)
        except V1.Stop:
            v = None
        V1.um(p)
        print(f'   v1 nx depth6 score({cand}) = {v} nodes={V1.nodes}', flush=True)
