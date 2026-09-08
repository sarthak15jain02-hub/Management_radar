# Management Radar — HDFC AMC Intern Build Challenge

## What this does
Ingests BSE exchange filings and YouTube management interviews for Maruti
Suzuki and Infosys, stores them in SQLite, and lets an analyst ask questions
answered only from retrieved source text, with citations (PDF+page or
video+timestamp).

## Setup
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# then paste your LLM API key into .env
\`\`\`

## Fetch pipeline (Step 1)
\`\`\`bash
python src/fetch/run_fetch.py
\`\`\`
- Downloads 7 BSE PDFs, extracts text page-by-page.
- Fetches transcripts for 3 YouTube interviews with timestamps.
- Idempotent: re-running skips anything already cached (verified — see NOTES.md).
- Failures (bad link, missing transcript, blocked download) are logged to
  \`cache/fetch_log.json\` and do not crash the run.

## Status
- [x] Step 1: Fetch & read
- [ ] Step 2: Store (SQLite schema)
- [ ] Step 3: Understand & answer (tagging + RAG chat)
- [ ] Step 4: Front end