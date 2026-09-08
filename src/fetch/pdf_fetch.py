import csv
import json
import os
import requests

CSV_PATH = "data/disclosure_links.csv"
PDF_DIR = "cache/pdfs"
LOG_PATH = "cache/fetch_log.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bseindia.com/",
}


def load_rows(source_type):
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["type"] == source_type]


def log_error(no, url, error):
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            logs = json.load(f)
    logs.append({"source_no": no, "url": url, "error": str(error)})
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)


def fetch_pdfs():
    rows = load_rows("BSE_PDF")
    for row in rows:
        no = row["no"]
        url = row["url"]
        out_path = f"{PDF_DIR}/{no}.pdf"

        if os.path.exists(out_path):
            print(f"[skip] {no} already cached")
            continue

        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print(f"[ok] {no} downloaded")
        except Exception as e:
            print(f"[fail] {no}: {e}")
            log_error(no, url, e)


if __name__ == "__main__":
    fetch_pdfs()