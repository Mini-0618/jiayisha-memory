import importlib.util
import subprocess
import sys
import time

spec = importlib.util.spec_from_file_location("engine", "src/engine.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)
E.NODE_CAP = 70000

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
OPENINGS = [
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6",      # italian
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6",      # sicilian
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7",      # qgd
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5",      # french winawer
]
MAT = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9}


class UCI:
    def __init__(self, cmd):
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True)
        self.send("uci")
        self.wait_for("uciok")
        self.send("isready")
        self.wait_for("readyok")

    def send(self, s):
        self.p.stdin.write(s + "\n")
        self.p.stdin.flush()

    def wait_for(self, token):
        while True:
            line = self.p.stdout.readline()
            if token in line:
                return line

    def bestmove(self, moves):
        self.send("position startpos" + (" moves " + " ".join(moves) if moves else ""))
        self.send("go wtime 300000 btime 300000 nodes 50000")
        while True:
            line = self.p.stdout.readline()
            if line.startswith("bestmove"):
                return line.split()[1]


def legal_moves(p):
    side = p.side
    out = []
    for m in E.gm(p):
        E.mk(p, m)
        if not E.at(p, p.ksq[side], 1 - side):
            out.append(m)
        E.um(p)
    return out


def material(p):
    s = 0
    for pc in p.b:
        if pc:
            v = MAT.get(pc % 8, 0)
            s += v if pc < 8 else -v
    return s


def play_game(base, opening, mine_white):
    p = E.sf(E.Pos(), START)
    moves = []
    hist = {}
    for u in opening.split():
        hist[p.h] = hist.get(p.h, 0) + 1
        E.mk(p, E.pu(u))
        moves.append(u)
    while True:
        side = p.side
        legal = legal_moves(p)
        if not legal:
            incheck = E.at(p, p.ksq[side], 1 - side)
            if incheck:
                return 0 if side == 0 else 1, "checkmate", len(moves)
            return 0.5, "stalemate", len(moves)
        if p.half >= 100:
            return 0.5, "fifty-move", len(moves)
        if hist.get(p.h, 0) >= 2:
            return 0.5, "repetition", len(moves)
        if len(moves) >= 200:
            s = material(p)
            if s >= 5:
                return 1, "adjudication", len(moves)
            if s <= -5:
                return 0, "adjudication", len(moves)
            return 0.5, "adjudication", len(moves)
        hist[p.h] = hist.get(p.h, 0) + 1
        white_turn = side == 0
        if white_turn == mine_white:
            q = E.sf(E.Pos(), START)
            E.seen = set()
            for u in moves:
                E.seen.add(q.h)
                E.mk(q, E.pu(u))
            u = E.tu(E.sr(q))
        else:
            u = base.bestmove(moves)
        assert E.pu(u) in legal or u in [E.tu(m) for m in legal], f"illegal {u}"
        E.mk(p, E.pu(u))
        moves.append(u)


def main():
    base = UCI(["python3", "baseline/pst_entry.py"])
    score = 0.0
    games = 0
    results = []
    for oi, opening in enumerate(OPENINGS):
        for mine_white in (True, False):
            t = time.time()
            r, why, plies = play_game(base, opening, mine_white)
            mine_pts = r if mine_white else 1 - r
            score += mine_pts
            games += 1
            tag = "W" if mine_white else "B"
            results.append(f"game {games}: opening {oi} as {tag}: "
                           f"{mine_pts} ({why}, {plies} plies, {time.time()-t:.0f}s)")
            print(results[-1], flush=True)
    base.send("quit")
    print(f"TOTAL: mine {score}/{games} = {score/games:.3f}")


if __name__ == "__main__":
    main()
