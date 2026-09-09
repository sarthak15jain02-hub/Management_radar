# Management Radar

A small research tool for Maruti Suzuki and Infosys. It brings exchange filings
and timestamped management interviews into one place, then answers questions
only from the passages it retrieves.

## Run it

Built and tested with Python 3.12.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put a Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

The API key is excluded from Git. Gemini free-tier limits can apply, but the
included database already contains the generated summaries and tags.

The cache and populated SQLite database are included, so a reviewer does not
need to fetch BSE PDFs or YouTube transcripts again. Start the dashboard with:

```bash
streamlit run src/app/app.py
```

Open the local URL Streamlit prints. This is the only long-running command.

## What is inside

- `src/fetch/` downloads BSE PDFs, extracts each page, and fetches YouTube
  captions without dropping timestamps. Each stage is cache-aware.
- `src/store/` writes the supplied source list and 268 searchable text chunks
  into `data/mgmt_radar.db`.
- `src/ai/` stores source summaries/topic tags and uses transparent lexical
  retrieval before asking the model to answer. It never lets the model search
  outside the selected company’s cached material.
- `src/app/app.py` is the single-page analyst view: source timeline on the
  left, grounded chat and retrieved evidence on the right.

## Evidence and guardrails

Every displayed source links to the original BSE filing or YouTube video. Chat
citations show a PDF page number or video timestamp; the retrieved evidence is
listed beneath each answer. If no text matches a question, the app does not
call the model and says it could not find the answer.

The model receives public source excerpts as **untrusted reference material**.
Both prompts explicitly tell it to ignore instructions embedded in those
documents. This is a practical guardrail against prompt injection, not a claim
that public documents are inherently safe.

## Known limitation

Source 2 is a documented manual text override: BSE returned an HTML SPA shell
instead of the linked PDF despite a session request with browser headers. Its
extracted text uses the same format as PDF output, and its status is visible in
the database. The raw PDF is therefore not present for that one source.


## Demo recording
https://drive.google.com/drive/folders/1rcP_4oQ7rWcIhc5WYQEzGbA_LXGt7Dwt?usp=drive_link