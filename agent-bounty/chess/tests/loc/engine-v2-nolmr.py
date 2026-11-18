# tiny-chess-01 entry (original code).
import json, os, random, urllib.request
VAL = [0,100,320,330,500,900,0,0,0,100,320,330,500,900,0]
PHW = [0,0,1,1,2,4,0,0,0,0,1,1,2,4,0]
# 0x88 negamax + TT, quiescence, null-move pruning, tapered PST eval.
def _exp(T):
 out = []
 for row in T:
  f = []
  for r in range(8):
   h = row[r*4:r*4+4]; f += h + h[::-1]
  out.append(f)
 return out
PM = _exp([
[0,0,0,0,50,50,50,50,10,10,20,30,5,5,10,25,0,0,0,20,5,-5,-10,0,5,10,10,-20,0,0,0,0],
[-50,-40,-30,-30,-40,-20,0,5,-30,5,10,15,-30,0,15,20,-30,5,15,20,-30,0,10,15,-40,-20,0,0,-50,-40,-30,-30],
[-20,-10,-10,-10,-10,5,0,0,-10,10,10,10,-10,0,10,10,-10,5,5,10,-10,0,5,10,-10,0,0,0,-20,-10,-10,-10],
[0,0,5,10,-5,0,0,0,-5,0,0,0,-5,0,0,0,-5,0,0,0,-5,0,0,0,5,10,10,10,0,0,5,10],
[-20,-10,-10,-5,-10,0,5,0,-10,5,5,5,-5,0,5,5,0,0,5,5,-10,0,5,5,-10,0,0,0,-20,-10,-10,-5],
[20,30,10,0,20,20,0,0,-10,-20,-20,-20,-20,-30,-30,-40,-30,-40,-40,-50,-30,-40,-40,-50,-30,-40,-40,-50,-30,-40,-40,-50]])
PE = _exp([
[0,0,0,0,40,40,40,40,30,30,30,30,20,20,20,20,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0,0],
[-50,-30,-30,-30,-30,-30,0,0,-30,-5,20,30,-30,-5,30,40,-30,-5,30,40,-30,-5,20,30,-30,-20,-5,0,-50,-40,-30,-20]])
PE = [PE[0], PM[1], PM[2], PM[3], PM[4], PE[1]]
EMG = [0]*15; EEG = [0]*15
for _p in range(1,7):
 EMG[_p] = [VAL[_p]+PM[_p-1][i] for i in range(64)]
 EEG[_p] = [VAL[_p]+PE[_p-1][i] for i in range(64)]
 EMG[_p+8] = [-(VAL[_p]+PM[_p-1][i ^ 56]) for i in range(64)]
 EEG[_p+8] = [-(VAL[_p]+PE[_p-1][i ^ 56]) for i in range(64)]
DIRS = [-16,16,-1,1,-15,-17,15,17]
NDIR = [-33,-31,-18,-14,14,18,31,33]
CMASK = [15]*128
CMASK[0] = 7; CMASK[4] = 3; CMASK[7] = 11
CMASK[112] = 13; CMASK[116] = 12; CMASK[119] = 14
_r = random.Random(987123)
ZB = [[_r.getrandbits(64) for _ in range(128)] for _ in range(15)]
ZSIDE = _r.getrandbits(64)
ZEP = ZB[13]
ZCAST = ZB[14][:16]
MATE = 100000
NODE_CAP = 70000
CAPF = 1 << 17

class Pos:
 __slots__ = ("b","side","cast","ep","half","smg","seg","ph","ksq","h","undo")
 def __init__(self):
  self.b = [0]*128; self.undo = []

def s6(sq): return (sq >> 4)*8 + (sq & 7)

def sf(p, fen):
 parts = fen.split()
 p.b = [0]*128; p.smg = p.seg = p.ph = 0; p.ksq = [0,0]
 h = 0
 for r, row in enumerate(parts[0].split("/")):
  f = 0
  for c in row:
   if c.isdigit(): f += int(c)
   else:
    pc = "PNBRQK".index(c.upper()) + 1 + (8 if c.islower() else 0)
    sq = r*16 + f; p.b[sq] = pc; i = s6(sq)
    p.smg += EMG[pc][i]; p.seg += EEG[pc][i]; p.ph += PHW[pc]
    if pc % 8 == 6: p.ksq[pc // 9] = sq
    h ^= ZB[pc][sq]; f += 1
 p.side = 0 if parts[1] == "w" else 1
 if p.side: h ^= ZSIDE
 p.cast = 0
 for i, c in enumerate("KQkq"):
  if c in parts[2]: p.cast |= 1 << i
 h ^= ZCAST[p.cast]
 p.ep = -1
 if parts[3] != "-":
  p.ep = "abcdefgh".index(parts[3][0]) + (8 - int(parts[3][1]))*16
  h ^= ZEP[p.ep]
 p.half = int(parts[4])
 p.h = h; p.undo = []
 return p

def at(p, sq, by):
 b = p.b; off = 8*by
 for d in ((15,17) if by == 0 else (-15,-17)):
  s = sq + d
  if not s & 0x88 and b[s] == 1 + off: return True
 for dirs, t0 in ((NDIR,2),(DIRS,6)):
  for d in dirs:
   s = sq + d
   if not s & 0x88 and b[s] == t0 + off: return True
 for i, d in enumerate(DIRS):
  s = sq + d
  while not s & 0x88:
   pc = b[s]
   if pc:
    t = pc % 8
    if pc // 9 == by and (t == 5 or (t == (3 if i >= 4 else 4))):
     return True
    break
   s += d
 return False

def gm(p, caps_only=False):
 b = p.b; side = p.side
 moves = []; ap = moves.append
 for sq in range(128):
  if sq & 0x88: continue
  pc = b[sq]
  if not pc or pc // 9 != side: continue
  t = pc % 8
  if t == 1:
   up = -16 if side == 0 else 16
   home = 6 if side == 0 else 1
   pre = 1 if side == 0 else 6
   row = sq >> 4; one = sq + up
   if not caps_only and not b[one]:
    if row == pre:
     for pr in (5,4,3,2): ap(sq | one << 7 | pr << 14)
    else:
     ap(sq | one << 7)
     if row == home and not b[sq + 2*up]: ap(sq | (sq + 2*up) << 7)
   for d in (up-1, up+1):
    to = sq + d
    if to & 0x88: continue
    tp = b[to]
    if tp and tp // 9 != side:
     if row == pre:
      for pr in (5,4,3,2): ap(sq | to << 7 | pr << 14 | CAPF)
     else: ap(sq | to << 7 | CAPF)
    elif to == p.ep: ap(sq | to << 7 | CAPF)
  elif t == 2:
   for d in NDIR:
    to = sq + d
    if to & 0x88: continue
    tp = b[to]
    if not tp or tp // 9 != side:
     if not caps_only or tp: ap(sq | to << 7 | (CAPF if tp else 0))
  elif t == 6:
   for d in DIRS:
    to = sq + d
    if to & 0x88: continue
    tp = b[to]
    if not tp or tp // 9 != side:
     if not caps_only or tp: ap(sq | to << 7 | (CAPF if tp else 0))
   if not caps_only and not at(p, sq, 1-side):
    for bit, emp, att, dest, rf, rook in (
      (1,(117,118),(117,118),118,119,4), (2,(115,114,113),(115,114),114,112,4),
      (4,(5,6),(5,6),6,7,12), (8,(3,2,1),(3,2),2,0,12)):
     if sq == (116 if bit < 4 else 4) and p.cast & bit and b[rf] == rook \
       and all(not b[s] for s in emp) and all(not at(p,s,1-side) for s in att):
      ap(sq | dest << 7)
  else:
   dirs = DIRS if t == 5 else (DIRS[4:] if t == 3 else DIRS[:4])
   for d in dirs:
    to = sq + d
    while not to & 0x88:
     tp = b[to]
     if tp:
      if tp // 9 != side: ap(sq | to << 7 | CAPF)
      break
     if not caps_only: ap(sq | to << 7)
     to += d
 return moves

def mk(p, m):
 if m == 0:
  p.undo.append((0, 0, p.cast, p.ep, p.half, 0))
  h = p.h ^ ZSIDE
  if p.ep >= 0: h ^= ZEP[p.ep]
  p.ep = -1; p.half += 1; p.h = h; p.side = 1 - p.side
  return
 b = p.b; frm = m & 127; to = (m >> 7) & 127; promo = (m >> 14) & 7
 pc = b[frm]; side = p.side; cap = b[to]; ep_cap = 0
 if pc % 8 == 1 and to == p.ep and not cap and (frm & 7) != (to & 7):
  ep_cap = b[to+16] if side == 0 else b[to-16]; cap = ep_cap
 p.undo.append((m, cap, p.cast, p.ep, p.half, ep_cap))
 h = p.h ^ ZSIDE
 if p.ep >= 0: h ^= ZEP[p.ep]
 nep = -1
 if cap:
  csq = to if not ep_cap else (to+16 if side == 0 else to-16)
  i = s6(csq)
  p.smg -= EMG[cap][i]; p.seg -= EEG[cap][i]; p.ph -= PHW[cap]
  h ^= ZB[cap][csq]; b[csq] = 0; p.half = 0
 elif pc % 8 == 1: p.half = 0
 else: p.half += 1
 i = s6(frm)
 p.smg -= EMG[pc][i]; p.seg -= EEG[pc][i]; h ^= ZB[pc][frm]; b[frm] = 0
 npc = pc + promo - 1 if promo else pc
 if promo:
  p.ph += PHW[npc] - PHW[pc]
 j = s6(to)
 p.smg += EMG[npc][j]; p.seg += EEG[npc][j]; h ^= ZB[npc][to]; b[to] = npc
 if pc % 8 == 6:
  p.ksq[side] = to
  if abs(to-frm) == 2:
   rf, rt = (frm+3, frm+1) if to > frm else (frm-4, frm-1)
   rook = b[rf]; i = s6(rf)
   p.smg -= EMG[rook][i]; p.seg -= EEG[rook][i]; h ^= ZB[rook][rf]; b[rf] = 0
   j = s6(rt)
   p.smg += EMG[rook][j]; p.seg += EEG[rook][j]; h ^= ZB[rook][rt]; b[rt] = rook
 if pc % 8 == 1 and abs(to-frm) == 32: nep = (frm+to) // 2; h ^= ZEP[nep]
 p.ep = nep
 nc = p.cast & CMASK[frm] & CMASK[to]
 if nc != p.cast: h ^= ZCAST[p.cast] ^ ZCAST[nc]; p.cast = nc
 p.h = h; p.side = 1 - side

def um(p):
 m, cap, cast, ep, half, ep_cap = p.undo.pop()
 if m == 0:
  p.side = 1 - p.side
  h = p.h ^ ZSIDE
  if p.ep >= 0: h ^= ZEP[p.ep]
  if ep >= 0: h ^= ZEP[ep]
  p.ep = ep; p.half = half; p.h = h
  return
 p.side = 1 - p.side; side = p.side; b = p.b
 frm = m & 127; to = (m >> 7) & 127; promo = (m >> 14) & 7
 npc = b[to]; pc = npc - promo + 1 if promo else npc
 h = p.h ^ ZSIDE
 if p.ep >= 0: h ^= ZEP[p.ep]
 if ep >= 0: h ^= ZEP[ep]
 j = s6(to)
 p.smg -= EMG[npc][j]; p.seg -= EEG[npc][j]; h ^= ZB[npc][to]; b[to] = 0
 if promo:
  p.ph -= PHW[npc] - PHW[pc]
 i = s6(frm)
 p.smg += EMG[pc][i]; p.seg += EEG[pc][i]; h ^= ZB[pc][frm]; b[frm] = pc
 if pc % 8 == 6:
  p.ksq[side] = frm
  if abs(to-frm) == 2:
   rf, rt = (frm+3, frm+1) if to > frm else (frm-4, frm-1)
   rook = b[rt]; j = s6(rt)
   p.smg -= EMG[rook][j]; p.seg -= EEG[rook][j]; h ^= ZB[rook][rt]; b[rt] = 0
   i = s6(rf)
   p.smg += EMG[rook][i]; p.seg += EEG[rook][i]; h ^= ZB[rook][rf]; b[rf] = rook
 if cap:
  csq = to if not ep_cap else (to+16 if side == 0 else to-16)
  i = s6(csq)
  p.smg += EMG[cap][i]; p.seg += EEG[cap][i]; p.ph += PHW[cap]
  h ^= ZB[cap][csq]; b[csq] = cap
 if cast != p.cast: h ^= ZCAST[p.cast] ^ ZCAST[cast]; p.cast = cast
 p.ep = ep; p.half = half; p.h = h

def ev(p):
 ph = min(p.ph, 24)
 s = (p.smg*ph + p.seg*(24-ph)) // 24
 return s if p.side == 0 else -s

class Stop(Exception): pass
TT = {}
nodes = 0
seen = set()

def ms(p, m, tt_move, ply):
 if m == tt_move: return 1 << 28
 f = m & 127; t = (m >> 7) & 127; pc = p.b[f]; pr = (m >> 14) & 7
 if m & CAPF: return (1 << 24) + VAL[p.b[t]]*32 - VAL[pc]
 if pr: return (1 << 24) + 900
 d = EMG[pc][s6(t)] - EMG[pc][s6(f)]
 return d if p.side == 0 else -d

def hb(p, side):
 return any(pc and pc // 9 == side and pc % 8 in (2,3,4,5) for pc in p.b)

def nx(p, depth, alpha, beta, ply, null_ok):
 global nodes
 nodes += 1
 if nodes & 1023 == 0 and nodes >= NODE_CAP: raise Stop
 if ply > 0 and p.half >= 100: return 0
 side = p.side
 incheck = at(p, p.ksq[side], 1-side)
 stand = None
 if depth <= 0 and not incheck:
  stand = ev(p)
  if stand >= beta: return stand
  if stand > alpha: alpha = stand
 alpha0 = alpha; tt_move = 0
 if depth > 0:
  ent = TT.get(p.h)
  if ent is not None:
   ed, ef, evv, em = ent; tt_move = em
   if ed >= depth and ply > 0:
    if ef == 0: return evv
    if ef == 1 and evv > alpha: alpha = evv
    elif ef == 2 and evv < beta: beta = evv
    if alpha >= beta: return evv
  if null_ok and depth >= 3 and not incheck and beta < MATE-1000 and hb(p, side):
   mk(p, 0)
   v = -nx(p, depth-3, -beta, -beta+1, ply+1, False)
   um(p)
   if v >= beta: return beta
 moves = gm(p, caps_only=(depth <= 0 and not incheck))
 scored = sorted(((ms(p, m, tt_move, ply), m) for m in moves), reverse=True)
 best = stand if stand is not None else -MATE - 1
 best_move = 0; legal = 0
 for i, (_, m) in enumerate(scored):
  mk(p, m)
  if at(p, p.ksq[side], 1-side):
   um(p); continue
  legal += 1
  if p.h in seen: v = 0
  elif i == 0 or depth <= 0:
   seen.add(p.h); v = -nx(p, depth-1, -beta, -alpha, ply+1, True); seen.discard(p.h)
  else:
   seen.add(p.h)
   v = -nx(p, depth-1, -alpha-1, -alpha, ply+1, True)
   if v > alpha and v < beta: v = -nx(p, depth-1, -beta, -alpha, ply+1, True)
   seen.discard(p.h)
  um(p)
  if v > best:
   best = v; best_move = m
   if v > alpha:
    alpha = v
    if alpha >= beta: break
 if legal == 0:
  if incheck: return -MATE + ply
  return stand if stand is not None else 0
 if depth > 0 and ply < 120:
  flag = 0 if alpha0 < best < beta else (1 if best >= beta else 2)
  TT[p.h] = (depth, flag, best, best_move)
 return best

def sr(p):
 global nodes
 nodes = 0
 side = p.side; legal = []
 for m in gm(p):
  mk(p, m)
  if not at(p, p.ksq[side], 1-side): legal.append(m)
  um(p)
 best = legal[0]; depth = 1
 try:
  while depth <= 64:
   scored = sorted(((ms(p, m, best, 0), m) for m in legal), reverse=True)
   alpha = -MATE - 1; cur = best
   for _, m in scored:
    mk(p, m)
    if p.h in seen: v = 0
    else:
     seen.add(p.h); v = -nx(p, depth-1, -MATE-1, -alpha, 1, True); seen.discard(p.h)
    um(p)
    if v > alpha: alpha = v; cur = m
   best = cur; depth += 1
 except Stop:
  pass
 return best

def tu(m):
 def name(sq): return "abcdefgh"[sq & 7] + str(8 - (sq >> 4))
 u = name(m & 127) + name((m >> 7) & 127)
 pr = (m >> 14) & 7
 if pr: u += "nbrq"[pr-2]
 return u

def pu(u):
 def sq(s): return "abcdefgh".index(s[0]) + (8 - int(s[1]))*16
 pr = "nbrq".index(u[4]) + 2 if len(u) > 4 else 0
 return sq(u[:2]) | sq(u[2:4]) << 7 | pr << 14

ENV_URL = os.environ.get("MAKEFUN_ENV_URL", "")
post = lambda path, body: json.load(urllib.request.urlopen(urllib.request.Request(
 ENV_URL + path, data=json.dumps(body).encode(),
 headers={"content-type": "application/json"})))

def play():
 while True:
  g = post("/game", {})
  if g["status"] == "done": return
  while g["status"] == "your_move":
   p = sf(Pos(), g["start_fen"])
   seen.clear()
   for u in g["moves"]:
    seen.add(p.h); mk(p, pu(u))
   u = tu(sr(p))
   if u not in g["legal_moves"]: u = g["legal_moves"][0]
   g = post("/move", {"game": g["game"], "move": u})

if ENV_URL: play()
