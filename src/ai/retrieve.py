"""Simple transparent lexical retrieval for a small, fixed source collection."""
import re
import sqlite3
from pathlib import Path

DB_PATH = Path("data/mgmt_radar.db")
STOP_WORDS = {"a", "an", "and", "are", "about", "did", "does", "for", "from", "has", "have", "in", "is", "it", "management", "of", "on", "said", "the", "to", "what", "with"}


def terms(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-zA-Z0-9]{3,}", text.lower()) if word not in STOP_WORDS}


def retrieve(question: str, company_id: int, limit: int = 6) -> list[dict]:
    query_terms = terms(question)
    if not query_terms:
        return []
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""SELECT ch.id AS chunk_id, ch.text, ch.page_number, ch.timestamp_start,
                                    s.id AS source_id, s.title, s.type, s.url
                             FROM chunks ch
                             JOIN sources s ON s.id = ch.source_id
                             WHERE s.company_id = ?""", (company_id,)).fetchall()
    ranked = []
    for row in rows:
        words = terms(row["text"])
        score = len(query_terms & words)
        if score:
            ranked.append((score, dict(row)))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [row for _, row in ranked[:limit]]


def source_label(row: dict) -> str:
    if row["type"] == "pdf":
        return f"[S{row['source_id']} p.{row['page_number']}]"
    seconds = int(row["timestamp_start"])
    return f"[S{row['source_id']} {seconds // 60}:{seconds % 60:02d}]"


def context(rows: list[dict]) -> str:
    return "\n\n".join(f"{source_label(row)} {row['text']}" for row in rows)
