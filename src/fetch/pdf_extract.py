import csv
import json
import os
import fitz  # PyMuPDF

CSV_PATH = "data/disclosure_links.csv"
PDF_DIR = "cache/pdfs"


def load_rows(source_type):
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["type"] == source_type]


def extract_pdfs():
    rows = load_rows("BSE_PDF")
    for row in rows:
        no = row["no"]
        pdf_path = f"{PDF_DIR}/{no}.pdf"
        out_path = f"{PDF_DIR}/{no}_extracted.json"

        if not os.path.exists(pdf_path):
            print(f"[skip] {no} not downloaded, run pdf_fetch first")
            continue

        if os.path.exists(out_path):
            print(f"[skip] {no} already extracted")
            continue

        try:
            doc = fitz.open(pdf_path)
            pages = [
                {"page_num": i + 1, "text": page.get_text()}
                for i, page in enumerate(doc)
            ]
            doc.close()

            with open(out_path, "w", encoding="utf-8") as f:
                json.dump({"source_no": no, "pages": pages}, f, indent=2)
            print(f"[ok] {no} extracted, {len(pages)} pages")
        except Exception as e:
            print(f"[fail] {no}: {e}")


if __name__ == "__main__":
    extract_pdfs()