# Management Radar — Intern Build Challenge

**HDFC AMC · AI & Digital Group · 2026–27**
**24 hours · solo · any language, any stack · AI-assisted coding encouraged**

---

## The business problem

Analysts track everything a company and its management say in public: official filings on the stock
exchange (results, expansions, resignations, big orders) and what the CEO and
CFO say in TV and YouTube interviews. That's dozens of PDFs and hours of
video per company, every quarter.

This assignment asks you to build a working prototype that does the first pass automatically.

**The one-line brief:** for the companies we give you, your system should
digest their exchange announcements *and* their management's video
interviews, then let an analyst ask questions like *"What has management
said about expansion plans?"* — with every answer backed by a quote from the
actual document or a timestamp in the actual video.

## What you get

- A list of **10 links for 2 NIFTY 50 companies — Maruti Suzuki and
  Infosys** (attached CSV): for each company, 3–4 official announcement
  PDFs from the BSE website and 1–2 YouTube interviews of their management
  (all with captions available). You do not need to hunt for sources —
  your code just needs to process the items on this list.
- Use any LLM you like — free tiers are perfectly fine. We judge how you
  design with AI, not how big your model is. For YouTube, any transcript
  tool is allowed (e.g. `youtube-transcript-api`, `yt-dlp`).

## The build — four pieces, in order

**1. Fetch & read** *(must have)*
Download the PDFs and pull the transcripts of the YouTube videos, keeping
the timestamps. Cache everything locally so a re-run doesn't fetch twice.
Handle a bad link or a missing transcript without crashing.

**2. Store** *(must have)*
Put everything in a real database (SQLite is fine): the companies, the
documents and videos with their details, the text pieces you'll search over
(with page or timestamp), and the tags your AI produces. A folder of JSON
files does not count. Be ready to explain every table — your schema is one
of the first things we read.

**3. Understand & answer** *(must have)*
Use an LLM to give every announcement and interview a plain-language summary
and topic tags (results, expansion, management change, new orders, risks…).
Then build a chat that answers questions like *"What did management promise
about margins?"* by first retrieving the relevant passages from your
database, then answering **with citations** — the exact PDF, or the video
with a timestamp. When the sources don't contain the answer, it should say
so — we will ask questions designed to tempt it into making things up.

**4. Show** *(must have)*
One clean page: pick a company, see its announcements and interviews as a
timeline with tags and summaries, plus the chat box. Style it in HDFC AMC
colours — red, deep navy, clean white. Look and feel counts: spacing,
readable type, and what the page shows while loading or when something fails.

## Rules

- **Use AI, openly.** Build this with AI assistants — Claude, ChatGPT,
  Copilot, Cursor, anything. Using AI well is a skill we are hiring for.
  The rule is transparency: keep a short `NOTES.md` with the prompts that
  mattered most, plus what you accepted, rejected, or fixed.
- **Keep a diary with Git.** Run `git init` in your project folder the moment
  you start, and commit every time something works — small, honest saves with
  real messages. We read this diary to see how you think. Whether you submit
  through GitHub or as a zip, the full Git history must come with your work.
  If you use GitHub, **keep the repository private while you build** — code
  visible before the deadline invites copying, and identical work fails
  everyone involved.
- **Keep secrets out.** Your LLM key lives in an environment variable or a
  `.env` file that is never committed. A key found inside the code or the Git
  history costs marks. Bonus thought: PDFs and transcripts are outside text
  going into your AI — what stops a malicious document from hijacking your
  prompts?
- **Finish something.** A thin system that works end-to-end beats a thick one
  that almost works. If you must cut a corner, cut it deliberately and write
  one line in `NOTES.md` saying what you cut and why. That is engineering
  judgment, and we score it.

## Timeline

-  3.30pm .** You receive this brief, the 10 links,
  and a 15-minute group Q&A call. The clock starts.
- **Hours 0–24 — build.** Work wherever you like, on your own machine.
  Commit as you go.
- **Hour 24 — submit, 10:00 AM next day.** Your submission must contain:
  1. your project folder with the `.git` diary inside,
  2. the populated database file (plus your cached PDFs/transcripts —
     but never the raw video files),
  3. a README that gets us running in five minutes,
  4. `NOTES.md` (decisions + best prompts),
  5. a 3-minute screen recording of the working system (if it is too big
     to include, an unlisted YouTube or Google Drive link in the README
     is fine).

  **Hand it in via GitHub — that is the route we expect:** push
  everything to a repository, then make it public, and email the
  repository link to Chetan by replying to the kickoff email. Commits
  and pushes after 10:00 AM are ignored — the Git timestamps tell us
  everything.

  **Only if you truly cannot use GitHub:** email your project as zip
  files, by replying to the kickoff email (max 5 MB per mail — split a
  bigger project into separate zip parts across several mails; exclude
  `node_modules`/`venv`; **include the hidden `.git` folder**).
- **We will reach out pretty fast to shortlisted candidates (30 min, screen
  shared).** Five minutes of live demo, we may ask you to make one small
  change on the spot — using your AI tools, thinking aloud — and to explain
  your schema and design choices. This is how we know the work is yours.

## Scoring (100 points)

| What we score | What good looks like | Points |
|---|---|---|
| Working outcome | Runs end-to-end from our machine using your README and cached data; the recording matches reality. | 30 |
| AI & answer quality | Sensible tags and summaries; chat answers grounded in retrieved text with document citations and video timestamps; graceful "I don't know." | 20 |
| Database design | A schema you can defend; clean separation of companies, sources, text pieces, and AI outputs. | 15 |
| Front end | HDFC AMC colours, clean hierarchy, honest loading and error states. | 15 |
| Code quality & Git diary | Readable structure, honest commit history, a README that works, a thoughtful `NOTES.md`. | 10 |
| Security basics | No secrets in code or history; inputs handled with care; untrusted-content risk at least considered. | 10 |

There is no pass mark published in advance. We rank, we discuss, and hunger
and curiosity break ties — a candidate who shipped less but understood more
can beat a candidate who shipped more on autopilot.

## Stretch goals — only if the core is done

- Break the AI work into separate steps — one that classifies, one that
  extracts claims, one that summarises — instead of one giant prompt.
- A "promise tracker": pull out concrete forward-looking statements by
  management ("we will add capacity by Q3") and list them in one place.
- A simple management consistency view: does what they say in interviews
  match what they file with the exchange?
- A "fetch latest" button that pulls new announcements for a company
  straight from the BSE website, not just our list.

Stretch goals earn no fixed points — they earn conversation in the viva,
which is worth more.

---

*This exercise uses publicly available disclosures. Your submission is
evaluated for hiring. Questions? Ask when we do the 15 min call.*
