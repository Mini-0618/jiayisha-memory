#!/usr/bin/env python3
"""Generate engine-v11.py: v3 with sunfish's Texel-tuned PST system ported in.

Derivation (all numbers from the baseline file itself, no hand tuning):
- Source: chess/baseline/pst_entry.py (commit e396948...), `piece` values and
  the `pst` dict. sunfish PST entries are DELTAS; the file joins them with
  piece values via padrow (x + piece[k]). Our EMG = VAL + PM is the same
  structure, so the port is: VAL <- sunfish piece values, PM <- sunfish PST.
- Symmetrization: our tables store only a-d files and mirror at startup
  (_exp), so each rank's 8 sunfish values are averaged in mirror pairs:
  a'=(a+h)/2, b'=(b+g)/2, c'=(c+f)/2, d'=(d+e)/2, Python round() (banker's).
  The tuned left-right asymmetry is averaged out -- documented loss.
- Quantization (compression-driven, measured): the raw port packs to 4,190
  bytes (over by 94) -- sunfish's irregular values compress far worse than
  our round hand-written ones, and no LZMA parameter rescues it (payload
  floor 4,041 at every dict size / preset 6 / 9). PM entries are therefore
  rounded to the nearest 10 (max +/-5cp per entry, documented); that packs
  to 4,078 bytes. VAL stays exact (479/929 untouched). Texel values at
  +/-5cp are noise-level; the tuned structure (center bonuses, edge
  penalties, 7th-rank pawn ~85) survives. The urllib alias trick from v9
  was tested here and made the payload WORSE (4,044 vs 4,041) -- not used.
- Scope: PM (MG) rows for all six pieces + VAL. PE (EG pawn/king rows) is
  untouched, but PE reuses PM[1..4] for N/B/R/Q, so their EG rows change as
  an architectural consequence (documented, not a second deliberate change).
- Everything else (search, killer, NMP, node cap 70k) is byte-identical to v3.
"""
import ast
import re

BASE = "/home/hatch/workspace/agent-bounty/chess/baseline/pst_entry.py"
V3 = "/home/hatch/workspace/agent-bounty/chess/src/engine-v3.py"
V11 = "/home/hatch/workspace/agent-bounty/chess/src/engine-v11.py"

src = open(BASE, encoding="utf-8").read()
m = re.search(r"pst = (\{.*?\n\})", src, re.S)
pst = ast.literal_eval(m.group(1))
m2 = re.search(r"piece = (\{.*?\})", src)
piece = ast.literal_eval(m2.group(1))
print("sunfish piece values:", piece)
for k, v in pst.items():
    assert len(v) == 64, (k, len(v))

# sunfish rows are rank 8 -> rank 1, files a -> h, white perspective.
# Our PM half-rows are the same rank order, files a-d only.
def sym(vals):
    out = []
    for r in range(8):
        row = vals[r * 8:(r + 1) * 8]
        out += [round((row[0] + row[7]) / 2), round((row[1] + row[6]) / 2),
                round((row[2] + row[5]) / 2), round((row[3] + row[4]) / 2)]
    return out

order = ["P", "N", "B", "R", "Q", "K"]
rows = {k: [round(v / 10) * 10 for v in sym(pst[k])] for k in order}
for k in order:
    print(k, rows[k])

val = [0, piece["P"], piece["N"], piece["B"], piece["R"], piece["Q"],
       0, 0, 0, piece["P"], piece["N"], piece["B"], piece["R"], piece["Q"], 0]

eng = open(V3, encoding="utf-8").read()
# VAL line
eng = re.sub(r"VAL = \[[^\]]*\]",
             "VAL = [" + ",".join(str(x) for x in val) + "]", eng, count=1)
# PM block: replace the six rows between "PM = _exp([" and "])\nPE = _exp(["
pm_text = "PM = _exp([\n" + ",\n".join(
    "[" + ",".join(str(x) for x in rows[k]) + "]" for k in order) + "])"
eng = re.sub(r"PM = _exp\(\[.*?\]\]\)", pm_text, eng, count=1, flags=re.S)
eng = eng.replace("# tiny-chess-01 entry (original code).",
                  "# tiny-chess-01 entry (v11: v3 + sunfish tuned PST port).")
open(V11, "w", encoding="utf-8").write(eng)
print("wrote", V11, len(eng), "bytes")
