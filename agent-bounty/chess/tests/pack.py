#!/usr/bin/env python3
"""Pack src/engine.py -> src/main.py (<=4096 bytes, make.fun tiny-chess-01).

Reproduces the v1 packing exactly: lzma FORMAT_ALONE of the raw source,
embedded as a latin-1 string literal; only \\, ', newline, CR and NUL are
escaped, all other bytes go in raw. No minification step (v1 payload is
byte-identical to engine.py).
"""
import io
import lzma
import os
import sys
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src", "engine.py")
OUT = os.path.join(HERE, "..", "src", "main.py")


def minify(data):
    """Drop comments and blank lines only (no renaming, no whitespace tricks).
    Output stays valid Python and keeps engine.py as the readable source."""
    lines = data.decode("utf-8").split("\n")
    toks = list(tokenize.generate_tokens(io.StringIO(data.decode("utf-8")).readline))
    cut = {}
    for t in toks:
        if t.type == tokenize.COMMENT:
            cut.setdefault(t.start[0] - 1, t.start[1])
    out = []
    for i, line in enumerate(lines):
        if i in cut:
            line = line[:cut[i]].rstrip()
        if line.strip():
            out.append(line.rstrip())
    return ("\n".join(out) + "\n").encode("utf-8")


def esc(s):
    """Escape a latin-1 payload string for a single-quoted Python literal.
    NUL must be \\x00 (not \\0) when an octal digit follows, else the digit
    is eaten by the octal escape -- the bug that cost v1's packer 2 bytes."""
    out = []
    for i, ch in enumerate(s):
        if ch == "\\":
            out.append("\\\\")
        elif ch == "'":
            out.append("\\'")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\x00":
            nxt = s[i + 1] if i + 1 < len(s) else ""
            out.append("\\x00" if nxt in "01234567" else "\\0")
        else:
            out.append(ch)
    return "".join(out)


def pack(src_path, out_path):
    data = open(src_path, "rb").read()
    mini = minify(data)
    filters = [{"id": lzma.FILTER_LZMA1, "dict_size": 12288,
                "lc": 3, "lp": 0, "pb": 0, "preset": 6}]
    payload = lzma.compress(mini, format=lzma.FORMAT_ALONE, filters=filters)
    s = esc(payload.decode("latin-1"))
    out = "#coding:l1\nimport lzma;exec(lzma.decompress('" + s + "'.encode('l1')))\n"
    open(out_path, "w", encoding="latin-1").write(out)
    return len(data), len(mini), len(payload), len(out.encode("latin-1"))


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else SRC
    out = sys.argv[2] if len(sys.argv) > 2 else OUT
    raw, mini, pay, total = pack(src, out)
    print(f"source {raw} bytes, minified {mini} bytes, payload {pay} bytes, "
          f"packed {total} bytes "
          f"({'OK <=4096' if total <= 4096 else 'OVER 4096 by ' + str(total - 4096)})")
