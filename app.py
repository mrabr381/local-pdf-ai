"""Streamlit web app: upload PDFs, ask questions, see page citations.

Run:  streamlit run app.py

No API key, no upload to any server — the PDF is processed in memory
on the machine running the app. The default TF-IDF backend needs no
model download. Ollama (optional) can be enabled in the sidebar for
generative answers when it is running locally.
"""

from __future__ import annotations

import io
import os
import tempfile

import streamlit as st

from localpdfai.answer import answer
from localpdfai.chunking import chunk_pages
from localpdfai.index import Index
from localpdfai.pdfio import PdfReadError, extract_pages


@st.cache_resource(show_spinner=False)
def _build_index(pdf_bytes: bytes, filename: str, backend: str) -> Index:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name
    try:
        pages = extract_pages(tmp_path)
        chunks = chunk_pages(pages)
        from localpdfai.embeddings import make_embedder

        embedder = make_embedder(backend)
        embedder.fit([c["text"] for c in chunks])
        matrix = embedder.embed([c["text"] for c in chunks])
        return Index(chunks, matrix, embedder, backend, filename)
    finally:
        os.unlink(tmp_path)


st.set_page_config(page_title="Local PDF AI", page_icon="📄")
st.title("📄 Local PDF AI")
st.caption("Ask questions about your PDFs — 100% on your machine. No upload, no account, no key.")

uploaded = st.file_uploader("Choose a PDF", type=["pdf"])
backend = st.sidebar.selectbox(
    "Embedding backend",
    ["tfidf", "st"],
    help="tfidf: instant, no download. st: sentence-transformers, needs torch + a model download.",
)
llm_mode = st.sidebar.selectbox(
    "Answer mode",
    ["extractive", "auto", "ollama"],
    help="extractive quotes the document. auto tries local Ollama first, then falls back.",
)
top_k = st.sidebar.slider("Passages to retrieve", 1, 5, 3)

if uploaded is not None:
    try:
        index = _build_index(uploaded.getvalue(), uploaded.name, backend)
    except (PdfReadError, ImportError, ValueError) as exc:
        st.error(str(exc))
        st.stop()
    pages = sorted({c["page"] for c in index.chunks})
    st.success(f"Indexed **{uploaded.name}** — {len(pages)} pages, {len(index.chunks)} chunks.")
    question = st.text_input("Ask a question about this PDF")
    if question:
        results = index.search(question, top_k=top_k)
        if not results or results[0]["score"] <= 0:
            st.warning("No relevant passage found — try different words.")
        else:
            try:
                text, mode_used = answer(question, results, mode=llm_mode)
            except ConnectionError as exc:
                st.error(str(exc))
                st.stop()
            st.markdown(f"**Answer ({mode_used}):**")
            st.write(text)
            st.subheader("Passages used")
            for result in results:
                chunk = result["chunk"]
                with st.expander(f"Page {chunk['page']} — relevance {result['score']:.2f}"):
                    st.write(chunk["text"])
else:
    st.info(
        "Upload a PDF to start. Try the sample: run `python scripts/make_sample.py` "
        "and upload `sample_data/sample.pdf` — a 4-page tomato-growing guide."
    )
