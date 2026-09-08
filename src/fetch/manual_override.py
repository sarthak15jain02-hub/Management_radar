import json
import os

PDF_DIR = "cache/pdfs"
OVERRIDE_DIR = "cache/manual_overrides"


def apply_override(source_no):
    md_path = f"{OVERRIDE_DIR}/{source_no}_manual.md"
    out_path = f"{PDF_DIR}/{source_no}_extracted.json"

    if not os.path.exists(md_path):
        print(f"[skip] no manual override found at {md_path}")
        return

    with open(md_path, encoding="utf-8") as f:
        text = f.read()

    # single page entry since we don't have per-page boundaries from markdown
    data = {"source_no": source_no, "pages": [{"page_num": 1, "text": text}]}

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[ok] manual override applied for {source_no}, {len(text)} chars")


if __name__ == "__main__":
    apply_override("2")