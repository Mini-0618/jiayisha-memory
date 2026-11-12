#!/usr/bin/env python3
"""加伊莎工作室本地知识库：把 workspace 下的 Markdown 文档建成 SQLite FTS5 全文索引。

用法：
  python3 build_kb.py            # 重建索引
  python3 kb.py 克隆音           # 查一个词
  python3 kb.py 密度 280         # 多词按 OR 匹配，按相关度排序

收录范围：~/workspace/jiayisha 与 ~/workspace/daishi-guanhua 下的全部 .md，
排除 Marvis 导入包目录（那 18 篇是复制件，避免重复命中）。
"""
import os
import re
import sqlite3
import sys

HOME = os.path.expanduser("~")
KB_DIR = os.path.join(HOME, "workspace", "jiayisha", "知识库")
DB_PATH = os.path.join(KB_DIR, "kb.db")
ROOTS = [
    os.path.join(HOME, "workspace", "jiayisha"),
    os.path.join(HOME, "workspace", "daishi-guanhua"),
]
EXCLUDE_DIRS = {"Marvis知识库-加伊莎工作室", "3D模型", "preview-build",
                "preview-main", "preview-build10", "preview01", "lemo-test"}


def collect_md_files():
    files = []
    for root in ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fn in filenames:
                if fn.endswith(".md"):
                    files.append(os.path.join(dirpath, fn))
    return sorted(files)


def chunk_text(text):
    """按标题与空行切块，每块不超过约 800 字，返回 (heading, chunk) 列表。"""
    chunks = []
    heading = ""
    buf = []
    buf_len = 0

    def flush():
        nonlocal buf, buf_len
        t = "\n".join(buf).strip()
        if t:
            chunks.append((heading, t))
        buf, buf_len = [], 0

    for line in text.splitlines():
        if line.startswith("#"):
            flush()
            heading = line.lstrip("#").strip()
            continue
        if not line.strip():
            if buf_len > 400:
                flush()
            continue
        buf.append(line)
        buf_len += len(line)
        if buf_len >= 800:
            flush()
    flush()
    return chunks


def build():
    os.makedirs(KB_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "CREATE VIRTUAL TABLE kb USING fts5(path, heading, text, tokenize='unicode61')"
    )
    cur.execute("CREATE TABLE docs(path TEXT PRIMARY KEY, mtime REAL)")
    files = collect_md_files()
    n_chunks = 0
    for f in files:
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        rel = os.path.relpath(f, os.path.join(HOME, "workspace"))
        for heading, chunk in chunk_text(text):
            cur.execute(
                "INSERT INTO kb(path, heading, text) VALUES (?, ?, ?)",
                (rel, heading, chunk),
            )
            n_chunks += 1
        cur.execute(
            "INSERT INTO docs(path, mtime) VALUES (?, ?)",
            (rel, os.path.getmtime(f)),
        )
    con.commit()
    cur.execute("SELECT COUNT(*) FROM docs")
    n_docs = cur.fetchone()[0]
    con.close()
    print(f"indexed {n_docs} files, {n_chunks} chunks -> {DB_PATH}")
    return n_docs, n_chunks


if __name__ == "__main__":
    build()
