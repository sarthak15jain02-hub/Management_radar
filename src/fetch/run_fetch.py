from pdf_fetch import fetch_pdfs
from pdf_extract import extract_pdfs
from youtube_fetch import fetch_transcripts

if __name__ == "__main__":
    print("== Fetching PDFs ==")
    fetch_pdfs()

    print("\n== Extracting PDF text ==")
    extract_pdfs()

    print("\n== Fetching YouTube transcripts ==")
    fetch_transcripts()

    print("\nDone.")