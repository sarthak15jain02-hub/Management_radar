PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    ticker TEXT NOT NULL UNIQUE
);

CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    source_no TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('pdf', 'youtube')),
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    published_date TEXT,
    cache_path TEXT,
    fetch_status TEXT NOT NULL CHECK (fetch_status IN ('ok', 'manual_override', 'failed')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    page_number INTEGER,
    timestamp_start REAL,
    timestamp_end REAL,
    chunk_order INTEGER NOT NULL,
    CHECK (page_number IS NOT NULL OR timestamp_start IS NOT NULL),
    UNIQUE (source_id, chunk_order)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL UNIQUE REFERENCES sources(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    topic_tags TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sources_company_date ON sources(company_id, published_date);
CREATE INDEX idx_chunks_source ON chunks(source_id);
