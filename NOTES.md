# Build notes

## Decisions I made

- I kept the source list fixed to the ten supplied links. The value of this prototype is in making that material searchable and auditable, not scraping a larger unbounded set.
- SQLite is enough here: the data is local, small, portable, and easy for a reviewer to inspect. The tables separate companies, sources, chunks, and AI outputs so re-running a stage does not mix responsibilities.
- PDF chunks retain page numbers. Transcript chunks combine nearby captions up to roughly 850 characters while retaining the first and final timestamps. That makes answers readable without losing their place in the video.
- I used lexical retrieval rather than adding a vector database. With 268 chunks, it is fast, inspectable, and avoids another opaque service. The retrieved passages are shown to the analyst below every answer.
- Source #2 is the one deliberate manual override. BSE repeatedly served an Angular HTML shell instead of the PDF; the attempt is logged in `cache/fetch_log.json`. I preserved the replacement text and flagged the status in the database rather than pretending the fetch succeeded.

## AI use

I used AI assistance while setting up the project structure and iterating on the cache/database pipeline. The two prompts kept in code are the ones that matter to the outcome:

1. **Source enrichment** (`src/ai/enrich_sources.py`): ask for a 2–3 sentence factual summary plus 2–5 lower-case topic tags in JSON. I explicitly frame filing/interview text as untrusted reference material and reject malformed JSON rather than storing it.
2. **Analyst answer** (`src/ai/ask.py`): provide only the retrieved excerpts, require each factual claim to use one of the supplied PDF-page or video-timestamp labels, and require the exact fallback sentence when the evidence is insufficient.

I accepted AI-generated summaries only as a discovery layer. The app still keeps the original source link and passage-level evidence visible. I rejected the tempting shortcut of asking a model a question without retrieval because that would make the answer harder to audit and easier to hallucinate.

## What I would improve with more time

- Add a retrieval evaluation set with expected citations for 10–15 analyst questions.
- Add semantic retrieval alongside lexical ranking, then compare both against that evaluation set rather than assuming embeddings are better.
- Add a source-detail drawer showing the full extracted page/transcript around each cited chunk.
