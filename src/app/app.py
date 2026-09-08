import json
import sqlite3
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.extend([str(ROOT / "src" / "ai")])
from ask import answer  # noqa: E402
from retrieve import source_label  # noqa: E402

DB_PATH = ROOT / "data" / "mgmt_radar.db"

st.set_page_config(page_title="Management Radar", page_icon="◉", layout="wide")
st.markdown("""<style>
    .stApp { background: #f7f8fa; color: #101b3d; }
    h1, h2, h3 { color: #0d1b42; }
    .eyebrow { color: #d71920; font-weight: 700; letter-spacing: .12em; font-size: .75rem; }
    .source-card { background: white; border-left: 4px solid #d71920; border-radius: 8px;
                    padding: 1rem 1.1rem; margin: .7rem 0; box-shadow: 0 1px 4px #0d1b4214; }
    .meta { color: #57627c; font-size: .85rem; }
</style>""", unsafe_allow_html=True)


def db_rows(sql, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def timestamp(value):
    seconds = int(value)
    return f"{seconds // 60}:{seconds % 60:02d}"


if not DB_PATH.exists():
    st.error("Database not found. Run the three Step 2 commands in the README first.")
    st.stop()

companies = db_rows("SELECT id, name, ticker FROM companies ORDER BY name")
if not companies:
    st.error("No sources loaded yet. Follow the README setup commands.")
    st.stop()

st.markdown("<div class='eyebrow'>HDFC AMC · AI & DIGITAL GROUP</div>", unsafe_allow_html=True)
st.title("Management Radar")
st.caption("Public disclosures and management interviews, with the evidence kept visible.")

company = st.selectbox("Company", companies, format_func=lambda row: f"{row['name']} ({row['ticker']})")
sources = db_rows("""SELECT s.*, t.summary, t.topic_tags
                     FROM sources s LEFT JOIN tags t ON t.source_id = s.id
                     WHERE s.company_id = ?
                     ORDER BY COALESCE(s.published_date, '') DESC""", (company["id"],))

left, right = st.columns([1.25, 1])
with left:
    st.subheader("Source timeline")
    if not sources:
        st.info("No sources for this company yet.")
    for source in sources:
        kind = "Exchange filing" if source["type"] == "pdf" else "Management interview"
        tags = ", ".join(json.loads(source["topic_tags"])) if source["topic_tags"] else "AI summary pending"
        summary = source["summary"] or "Run AI enrichment to generate a summary."
        st.markdown(f"""<div class='source-card'><b>{source['title']}</b><br>
        <span class='meta'>{source['published_date'] or 'Date unavailable'} · {kind}</span><p>{summary}</p>
        <span class='meta'>Tags: {tags}</span><br><a href='{source['url']}' target='_blank'>Open original source ↗</a></div>""", unsafe_allow_html=True)

with right:
    st.subheader("Ask the sources")
    st.caption("Answers are limited to retrieved passages. A citation is always shown underneath.")
    question = st.text_area("Question", placeholder="What did management say about AI growth?", height=100)
    if st.button("Find answer", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Write a question first.")
        else:
            with st.spinner("Checking the relevant filings and interview excerpts…"):
                try:
                    response, evidence = answer(question, company["id"])
                    st.session_state["response"] = response
                    st.session_state["evidence"] = evidence
                except Exception as exc:
                    st.error(f"The AI request failed: {exc}")
    if st.session_state.get("response"):
        st.markdown(st.session_state["response"])
        evidence = st.session_state.get("evidence", [])
        if evidence:
            st.markdown("**Retrieved evidence**")
            for row in evidence:
                location = source_label(row)
                st.markdown(f"- [{location} · {row['title']}]({row['url']})")
