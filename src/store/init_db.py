"""Create the local SQLite database. Use --reset only when rebuilding from cache."""
import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path("data/mgmt_radar.db")
SCHEMA_PATH = Path("data/schema.sql")


def init_db(reset: bool = False) -> None:
    if DB_PATH.exists() and not reset:
        print(f"[skip] {DB_PATH} already exists; use --reset to rebuild it")
        return
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[ok] removed old {DB_PATH}")
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    print(f"[ok] created {DB_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="rebuild database from scratch")
    init_db(parser.parse_args().reset)
