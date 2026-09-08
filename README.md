# Management Radar

A small research tool for Maruti Suzuki and Infosys. It puts exchange filings and timestamped management interviews in one place, then answers questions only from the passages it retrieves.

## Run it

This was built and tested with Python 3.12.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put an OpenAI API key in `.env`. `OPENAI_MODEL` is configurable there too. The key is deliberately excluded from Git.

The fetch cache is included, so a reviewer does not need to hit BSE or YouTube to run the project. Rebuild the database from those local files:

```bash
python src/store/init_db.py --reset
python src/store/load_sources.py
python src/store/load_chunks.py
python src/ai/enrich_sources.py
streamlit run src/app/app.py
```

Open the local URL Streamlit prints. The final command is the only long-running one; leave it open while demoing.

## What is inside

- `src/fetch/` downloads BSE PDFs, extracts each page, and fetches YouTube captions without dropping timestamps. Each stage is cache-aware.
- `src/store/` writes the supplied source list and 268 small searchable text chunks into `data/mgmt_radar.db`.
- `src/ai/` stores source summaries/topic tags and uses transparent lexical retrieval before asking the model to answer. It never lets the model search outside the selected company’s cached material.
- `src/app/app.py` is the single-page analyst view: source timeline on the left, grounded chat and the retrieved evidence on the right.

## Evidence and guardrails

Every displayed source links to the original BSE filing or YouTube video. Chat citations show a PDF page number or a video timestamp; the same retrieved sources are listed beneath each answer. If no text matches a question, the app does not call the model and says it could not find the answer.

The model receives public source excerpts as **untrusted reference material**. Both prompts explicitly tell it to ignore instructions embedded in those documents. This is a practical guardrail against prompt injection, not a claim that public documents are inherently safe.

## Known limitation

Source 2 is a documented manual text override: BSE returned an HTML SPA shell instead of the linked PDF despite a session request with browser headers. Its extracted text uses the same format as PDF output, and its status is visible in the database. The raw PDF is therefore not present for that one source.
