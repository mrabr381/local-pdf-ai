# 📄 Local PDF AI

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![No API key required](https://img.shields.io/badge/API%20key-not%20required-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B.svg)
![100% local](https://img.shields.io/badge/100%25-local-22c55e.svg)

**Ask questions about your PDFs in plain English — and get answers with page citations. Everything runs on your machine: no upload, no account, no API key, no subscription.**

Drop in a contract, a manual, a research paper, a textbook — ask "what is the notice period?" or "how do I fix error 42?" and get the exact passage, with the page number, in seconds.

## Table of contents

- [Before / after](#before--after)
- [Verified Q&A (sample document)](#verified-qa-sample-document)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Web app](#web-app)
- [How it works](#how-it-works)
- [Optional: generative answers with Ollama](#optional-generative-answers-with-ollama)
- [Optional: semantic embeddings](#optional-semantic-embeddings)
- [Comparison with paid PDF-chat tools](#comparison-with-paid-pdf-chat-tools)
- [Honest limitations](#honest-limitations)
- [Project structure](#project-structure)
- [License](#license)

## Before / after

**Before — finding one fact in a 200-page PDF:**

```
Ctrl+F … "notice period" … 47 matches … scroll … scroll …
read three wrong sections … give up and ask a colleague
```

**After — one command:**

```
$ python -m localpdfai ask --pdf contract.pdf --q "what is the notice period?"

Answer (extractive):

1. [p. 12] (relevance 0.41)
   Either party may terminate this agreement by giving 30 days'
   written notice ...
```

## Verified Q&A (sample document)

The repo ships with a regenerable 4-page sample PDF — *The Beginner's Guide to Growing Tomatoes* (`python scripts/make_sample.py`). Every question below was run against it and hand-checked against the PDF text. Top-1 citation correct on **6/6**:

| Question | Top passage | Answer in the quote |
| --- | --- | --- |
| What soil pH do tomatoes need? | p. 2 (0.33) | pH between 6.0 and 6.8 |
| How much water do tomato plants need each week? | p. 2 (0.25) | 1 to 2 inches per week |
| How do I deal with tomato hornworms? | p. 3 (0.16) | Pick off by hand into soapy water |
| How long until tomatoes are ready to harvest? | p. 4 (0.31) | 60 to 80 days |
| Should I store tomatoes in the fridge? | p. 4 (0.26) | Never — flavour is destroyed, flesh turns mealy |
| How far apart should I space tomato plants? | p. 1 (0.25) | 60 to 90 cm (24 to 36 inches) |

Same question asked twice returns byte-identical output. Full transcripts: [`sample_output/qa_report.md`](sample_output/qa_report.md).

## Quickstart

```
git clone https://github.com/mrabr381/local-pdf-ai.git
cd local-pdf-ai
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Make the sample PDF and ask it something:
python scripts/make_sample.py
python -m localpdfai ask --pdf sample_data/sample.pdf --q "What soil pH do tomatoes need?"
```

## Usage

```
# Build a reusable index (fast after the first ask)
python -m localpdfai index --pdf contract.pdf
# → contract.localpdfai.json

# Ask questions (reuses the index when it exists)
python -m localpdfai ask --pdf contract.pdf --q "what is the notice period?"
python -m localpdfai ask --pdf manual.pdf --q "how do I reset the device?" --top-k 5

# Semantic embeddings instead of TF-IDF (needs sentence-transformers + torch)
python -m localpdfai ask --pdf paper.pdf --q "what did the study conclude?" --backend st

# Generative answer from a local Ollama model (optional, see below)
python -m localpdfai ask --pdf report.pdf --q "summarise the risks" --llm auto
```

Exit codes: `0` ok, `1` runtime error (missing file, no extractable text, empty question, Ollama unreachable in `--llm ollama` mode), `2` bad arguments. Errors are plain-English, no tracebacks.

## Web app

```
streamlit run app.py
```

Upload a PDF, ask questions in the chat box, expand any passage to see the full text with its page number. The PDF is processed in memory on your machine — nothing is uploaded anywhere.

**1-click deploy (repo owner):** [share.streamlit.io](https://share.streamlit.io) → Create app → repo `mrabr381/local-pdf-ai`, branch `main`, file `app.py` → Deploy. No key or secret needed.

## How it works

```
PDF ──▶ pypdf (text per page) ──▶ chunks (~600 chars, page kept)
        │
        ▼
  TF-IDF embeddings (NumPy, default) ──▶ cosine search, top-k passages
  or sentence-transformers (optional)
        │
        ▼
  extractive answer: quoted passages + [p. N] citations
  or Ollama (optional): grounded summary with the same citations
```

- **Chunking** never crosses a page boundary, so every citation points at exactly one page.
- **Retrieval** is deterministic: ties break by chunk order, so the same question always returns the same passages.
- **Index files** (`*.localpdfai.json`) are plain JSON and can be rebuilt any time.

## Optional: generative answers with Ollama

Extractive answers quote the document — accurate, but they don't summarise or rephrase. For a written answer, run [Ollama](https://ollama.com) locally:

```
ollama serve
ollama pull llama3.2
python -m localpdfai ask --pdf report.pdf --q "summarise the risks" --llm auto
```

`--llm auto` tries Ollama and falls back to the extractive answer (with a note) when Ollama isn't running. `--llm ollama` fails loudly instead of silently falling back. The model only ever sees the retrieved passages, never the whole document — and it is instructed to answer from those passages only, with page citations.

## Optional: semantic embeddings

The default TF-IDF backend matches on words — great for factual questions ("notice period", "pH 6.0"), weak on paraphrases ("how long before I can pick them?" vs "days to maturity"). For semantic matching:

```
pip install sentence-transformers   # pulls torch (~2 GB)
python -m localpdfai ask --pdf doc.pdf --q "..." --backend st
```

TF-IDF stays the default because it needs no download, no GPU, and no 2 GB install — and for most PDF Q&A the keyword signal is the one that matters.

## Comparison with paid PDF-chat tools

|  | Local PDF AI (this repo) | Paid PDF-chat tools |
| --- | --- | --- |
| Price | Free, open source (MIT) | Subscription, usually per month |
| Your documents uploaded to a server? | No — everything local | Yes, by design |
| Account / API key needed | No | Yes |
| Answers with page citations | Yes | Yes |
| Generative summaries | Yes, with local Ollama (optional) | Yes, cloud LLM |
| Works offline | Yes (after install) | No |
| Scanned image-only PDFs | No — OCR not supported yet | Some offer OCR |

## Honest limitations

- **Extractive answers are quotes, not synthesis.** Without Ollama, you get the exact passages — accurate, but the tool won't write you a polished summary. That is deliberate: it cannot invent facts.
- **TF-IDF is lexical, not semantic.** A question phrased very differently from the document may miss. Use `--backend st` for paraphrase-heavy questions.
- **No OCR.** Scanned image-only PDFs have no extractable text and are rejected with a clear error.
- **No JavaScript, no tables-as-data.** Text extraction follows the PDF's text layer; complex tables may come out as jumbled lines.
- **Ollama answers depend on your local model.** A small local model can still misread a passage — always check the cited page.
- **Large PDFs are slower on first index** — indexing is in-memory and single-threaded; a 500-page PDF takes a few minutes on first ask, then the saved index makes later asks instant.

## Project structure

```
local-pdf-ai/
├── app.py                  # Streamlit web app (repo root, deploy-ready)
├── localpdfai/
│   ├── pdfio.py            # PDF → text per page (pypdf)
│   ├── chunking.py         # pages → ~600-char chunks, page kept
│   ├── embeddings.py       # TF-IDF (default) + sentence-transformers (opt-in)
│   ├── index.py            # build / search / save / load index (JSON)
│   ├── answer.py           # extractive + Ollama answers
│   └── cli.py              # index / ask commands, exit codes 0/1/2
├── scripts/make_sample.py  # regenerates sample_data/sample.pdf (reportlab)
├── sample_data/            # sample.pdf (generated, gitignored)
└── sample_output/          # qa_report.md + index.html demo page
```

## License

MIT — see [LICENSE](LICENSE).
