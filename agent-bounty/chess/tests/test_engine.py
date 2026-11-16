import importlib.util
import sys
import time

spec = importlib.util.spec_from_file_location(
    "engine", sys.argv[1] if len(sys.argv) > 1 else "src/engine.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


def perft(p, d):
    if d == 0:
        return 1
    n = 0
    side = p.side
    for m in E.gm(p):
        E.mk(p, m)
        if not E.at(p, p.ksq[side], 1 - side):
            n += perft(p, d - 1)
        E.um(p)
    return n


def check(fen, depth, want):
    p = E.sf(E.Pos(), fen)
    got = perft(p, depth)
    ok = "OK " if got == want else "FAIL"
    print(f"{ok} perft({depth}) = {got} (want {want})  {fen[:40]}")
    return got == want


START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
KIWI = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
POS3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
POS4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
POS5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
EP = "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3"

ok = True
ok &= check(START, 3, 8902)
ok &= check(KIWI, 2, 2039)
ok &= check(POS3, 3, 2812)
ok &= check(POS4, 2, 264)
ok &= check(POS5, 2, 1486)

# en passant: e5xf6 e.p. must be generated and legal
p = E.sf(E.Pos(), EP)
ep_move = 52 | 37 << 7  # e5 -> f6
legal = []
for m in E.gm(p):
    E.mk(p, m)
    if not E.at(p, p.ksq[0], 1):
        legal.append(m)
    E.um(p)
print(("OK " if any((m & 0x1FFFF) == ep_move for m in legal) else "FAIL") + " en passant capture generated")
ok &= any((m & 0x1FFFF) == ep_move for m in legal)

# make/unmake integrity: hash and scores return to the FEN values
p = E.sf(E.Pos(), KIWI)
h0, s0 = p.h, (p.smg, p.seg, p.ph)
for m in E.gm(p):
    E.mk(p, m)
    E.um(p)
    assert p.h == h0 and (p.smg, p.seg, p.ph) == s0, "unmake mismatch"
print("OK  make/unmake integrity")

# speed: nodes/sec on a middlegame position
p = E.sf(E.Pos(), KIWI)
E.seen.clear()
E.TT.clear()
t = time.time()
E.NODE_CAP = 10 ** 9
try:
    E.nodes = 0
    import threading

    def run():
        E.sr(p)
    th = threading.Thread(target=run, daemon=True)
    th.start()
    th.join(5)
    dt = time.time() - t
    print(f"speed: {E.nodes} nodes in {dt:.1f}s -> {E.nodes / max(dt, .01):,.0f} nps (5s window)")
except Exception as e:
    print("speed test error", e)

# search sanity: mate in 1 (Ra8#) must be found
p = E.sf(E.Pos(), "6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1")
E.seen.clear(); E.TT.clear(); E.NODE_CAP = 70000
mv = E.tu(E.sr(p))
print(("OK " if mv == "a1a8" else "FAIL") + f" mate-in-1 -> {mv}")
ok &= mv == "a1a8"

# search sanity: hanging queen must be taken (Qxh8 wins the queen for free)
p = E.sf(E.Pos(), "k6q/8/5K2/8/8/8/8/7R w - - 0 1")
E.seen.clear(); E.TT.clear()
mv = E.tu(E.sr(p))
print(("OK " if mv == "h1h8" else "FAIL") + f" win-queen -> {mv}")
ok &= mv == "h1h8"

# self-play smoke test: 60 plies, every move legal, no crash
E.NODE_CAP = 3000
played = []
for ply in range(60):
    q = E.sf(E.Pos(), START)
    hist = set()
    for u in played:
        hist.add(q.h); E.mk(q, E.pu(u))
    E.seen = hist
    side = q.side
    legal = []
    for m in E.gm(q):
        E.mk(q, m)
        if not E.at(q, q.ksq[side], 1 - side):
            legal.append(m)
        E.um(q)
    assert legal, "no legal moves"
    mv = E.sr(q)
    assert mv in legal, f"illegal move chosen: {E.tu(mv)}"
    played.append(E.tu(mv))
print("OK  self-play 60 plies:", " ".join(played[:12]), "...")

print("ALL OK" if ok else "SOME FAILED")
