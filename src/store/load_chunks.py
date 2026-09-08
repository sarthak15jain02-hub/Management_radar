"""Turn cached page text and timestamped transcript segments into searchable rows."""
import json
import re
import sqlite3
from pathlib import Path

DB_PATH = Path("data/mgmt_radar.db")
MAX_CHARS = 850


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_text(text: str) -> list[str]:
    text = clean(text)
    pieces = []
    while len(text) > MAX_CHARS:
        cut = text.rfind(". ", 0, MAX_CHARS)
        if cut < MAX_CHARS // 2:
            cut = text.rfind(" ", 0, MAX_CHARS)
        cut = cut if cut > 0 else MAX_CHARS
        pieces.append(text[:cut + 1].strip())
        text = text[cut + 1:].strip()
    return pieces + ([text] if text else [])


def pdf_chunks(source_no: str):
    data = json.loads(Path(f"cache/pdfs/{source_no}_extracted.json").read_text(encoding="utf-8"))
    for page in data["pages"]:
        for text in split_text(page["text"]):
            yield text, page["page_num"], None, None


def transcript_chunks(source_no: str):
    data = json.loads(Path(f"cache/transcripts/{source_no}.json").read_text(encoding="utf-8"))
    buffer, start = [], None
    for segment in data["segments"]:
        text = clean(segment["text"])
        if not text:
            continue
        if start is None:
            start = float(segment["start_sec"])
        if buffer and len(" ".join(buffer + [text])) > MAX_CHARS:
            yield " ".join(buffer), None, start, float(segment["start_sec"])
            buffer, start = [text], float(segment["start_sec"])
        else:
            buffer.append(text)
    if buffer:
        yield " ".join(buffer), None, start, float(data["segments"][-1]["start_sec"])


def load_chunks() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        sources = conn.execute("SELECT id, source_no, type FROM sources ORDER BY CAST(source_no AS INTEGER)").fetchall()
        for source_id, source_no, source_type in sources:
            conn.execute("DELETE FROM chunks WHERE source_id = ?", (source_id,))
            iterator = pdf_chunks(source_no) if source_type == "pdf" else transcript_chunks(source_no)
            rows = [(source_id, text, page, start, end, order) for order, (text, page, start, end) in enumerate(iterator)]
            conn.executemany("""INSERT INTO chunks (source_id, text, page_number, timestamp_start, timestamp_end, chunk_order)
                                VALUES (?, ?, ?, ?, ?, ?)""", rows)
            print(f"[ok] source {source_no}: {len(rows)} searchable chunks")


if __name__ == "__main__":
    load_chunks()
