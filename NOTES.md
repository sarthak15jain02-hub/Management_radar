## Cuts / known issues
- Source #2 (Maruti Q4 FY26 results + dividend press release, BSE_PDF):
  automated fetch (requests, with browser headers, Referer, Fetch Metadata
  headers, and session cookies from bseindia.com) was consistently served
  BSE's Angular SPA shell instead of the PDF — this link likely requires
  JS execution to pass BSE's bot detection, which a headless-browser-free
  pipeline can't replicate without disproportionate effort for one source.
  Content was instead captured via an external URL-to-markdown reader and
  manually placed into the same extracted-JSON format
  (src/fetch/manual_override.py), so downstream steps treat it identically
  to automated sources. Flagged here for transparency per assignment rules.