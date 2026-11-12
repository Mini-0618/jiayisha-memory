#!/usr/bin/env python3
"""Query the local studio knowledge base: python3 kb.py <keyword> [more words] [--all]"""
import os
import sqlite3
import sys

HOME = os.path.expanduser("~")
DB_PATH = os.path.join(HOME, "workspace", "jiayisha", "知识库", "kb.db")


def search(terms, limit=8):
    if not os.path.exists(DB_PATH):
        print("index missing, run: python3 build_kb.py")
        return 1
    clean = [t.replace('"', "") for t in terms if t.strip()]
    if not clean:
        print("usage: python3 kb.py <keyword>")
        return 1
    q = " OR ".join('"' + t + '"' for t in clean)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    rows = cur.execute(
        "SELECT path, heading, snippet(kb, 2, '[', ']', '...', 16) "
        "FROM kb WHERE kb MATCH ? ORDER BY rank LIMIT ?",
        (q, limit),
    ).fetchall()
    if not rows:
        # FTS unicode61 把连续汉字切成一个词，词中片段（如"参差多态"藏在
        # "参差多态乃幸福本源"里）查不到；回退到 LIKE 子串搜索。
        like_q = " OR ".join("text LIKE ?" for _ in clean)
        like_args = ["%" + t + "%" for t in clean]
        like_rows = cur.execute(
            "SELECT path, heading, text FROM kb WHERE " + like_q + " LIMIT ?",
            like_args + [limit],
        ).fetchall()
        rows = []
        for path, heading, text in like_rows:
            term = next(t for t in clean if t in text)
            pos = text.find(term)
            start = max(0, pos - 40)
            snip = ("..." if start > 0 else "") + text[start:start + 120].replace(
                term, "[" + term + "]", 1
            )
            rows.append((path, heading, snip))
    con.close()
    if not rows:
        print("no match. Try another word, or rebuild with: python3 build_kb.py")
        return 0
    for i, (path, heading, snip) in enumerate(rows, 1):
        title = "  # " + heading if heading else ""
        print(str(i) + ". " + path + title)
        print("   " + snip.strip())
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--all"]
    limit = 20 if "--all" in sys.argv[1:] else 8
    sys.exit(search(args, limit))
