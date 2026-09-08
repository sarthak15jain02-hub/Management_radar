"""Load the supplied source list into SQLite. Safe to run more than once."""
import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("data/mgmt_radar.db")
CSV_PATH = Path("data/disclosure_links.csv")
COMPANIES = {
    "Maruti Suzuki": ("Maruti Suzuki India Limited", "MARUTI"),
    "Infosys": ("Infosys Limited", "INFY"),
}


def load_sources() -> None:
    if not DB_PATH.exists():
        raise SystemExit("Database missing. Run: python src/store/init_db.py")
    with CSV_PATH.open(newline="", encoding="utf-8") as handle, sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        for row in csv.DictReader(handle):
            company_name, ticker = COMPANIES[row["company"]]
            conn.execute("INSERT OR IGNORE INTO companies (name, ticker) VALUES (?, ?)", (company_name, ticker))
            company_id = conn.execute("SELECT id FROM companies WHERE ticker = ?", (ticker,)).fetchone()[0]
            is_pdf = row["type"] == "BSE_PDF"
            extracted_path = Path(f"cache/pdfs/{row['no']}_extracted.json") if is_pdf else Path(f"cache/transcripts/{row['no']}.json")
            raw_path = Path(f"cache/pdfs/{row['no']}.pdf") if is_pdf else None
            if not extracted_path.exists():
                print(f"[skip] source {row['no']}: cached text is missing")
                continue
            fetch_status = "manual_override" if is_pdf and not raw_path.exists() else "ok"
            cache_path = str(raw_path if raw_path and raw_path.exists() else extracted_path)
            conn.execute(
                """INSERT INTO sources
                   (company_id, source_no, type, title, url, published_date, cache_path, fetch_status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(source_no) DO UPDATE SET
                     company_id=excluded.company_id, type=excluded.type, title=excluded.title,
                     url=excluded.url, published_date=excluded.published_date,
                     cache_path=excluded.cache_path, fetch_status=excluded.fetch_status""",
                (company_id, row["no"], "pdf" if is_pdf else "youtube", row["title"], row["url"],
                 row["date"] or None, cache_path, fetch_status),
            )
            print(f"[ok] source {row['no']} loaded")


if __name__ == "__main__":
    load_sources()
