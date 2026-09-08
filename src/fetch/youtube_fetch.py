import csv
import json
import os
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

CSV_PATH = "data/disclosure_links.csv"
TRANSCRIPT_DIR = "cache/transcripts"
LOG_PATH = "cache/fetch_log.json"


def load_rows(source_type):
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["type"] == source_type]


def extract_video_id(url):
    parsed = urlparse(url)
    return parse_qs(parsed.query)["v"][0]


def log_error(no, url, error):
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            logs = json.load(f)
    logs.append({"source_no": no, "url": url, "error": str(error)})
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)


def fetch_transcripts():
    rows = load_rows("YOUTUBE")
    for row in rows:
        no = row["no"]
        url = row["url"]
        out_path = f"{TRANSCRIPT_DIR}/{no}.json"

        if os.path.exists(out_path):
            print(f"[skip] {no} already cached")
            continue

        try:
            video_id = extract_video_id(url)
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id)
            segments = [
                {"start_sec": snippet.start, "text": snippet.text}
                for snippet in fetched
            ]
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump({"source_no": no, "segments": segments}, f, indent=2)
            print(f"[ok] {no} transcript fetched, {len(segments)} segments")
        except Exception as e:
            print(f"[fail] {no}: {e}")
            log_error(no, url, e)


if __name__ == "__main__":
    fetch_transcripts()