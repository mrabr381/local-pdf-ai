"""Q&A citation tests for local-pdf-ai.

The fixture is the tiny offline tomato guide (scripts/make_sample.py
regenerates sample_data/sample.pdf — the PDF itself is binary and
gitignored, so the test rebuilds it when it is missing, exactly as a
fresh clone would). Every expected page + relevance score below was
measured by running the real indexer, not assumed.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from localpdfai.answer import extractive_answer
from localpdfai.chunking import chunk_pages
from localpdfai.index import Index

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PDF = ROOT / "sample_data" / "sample.pdf"

# question -> (expected top-1 page, expected relevance, answer phrase)
EXPECTED_QA = {
    "What soil pH do tomatoes need?": (2, 0.33, "6.0 and 6.8"),
    "How much water do tomato plants need each week?": (2, 0.25, "1 to 2 inches) of water per week"),
    "How do I deal with tomato hornworms?": (3, 0.16, "soapy water"),
    "How long until tomatoes are ready to harvest?": (4, 0.31, "60 to 80 days"),
    "Should I store tomatoes in the fridge?": (4, 0.26, "Never store tomatoes in the fridge"),
    "How far apart should I space tomato plants?": (1, 0.25, "60 to 90 centimetres"),
}


@pytest.fixture(scope="module")
def index() -> Index:
    if not SAMPLE_PDF.is_file():
        subprocess.run(
            [sys.executable, "scripts/make_sample.py"],
            cwd=str(ROOT),
            check=True,
        )
    assert SAMPLE_PDF.is_file()
    return Index.build(str(SAMPLE_PDF))


def test_sample_pdf_indexes_to_seven_chunks(index):
    assert len(index.chunks) == 7
    assert sorted({c["page"] for c in index.chunks}) == [1, 2, 3, 4]


def test_ph_question_top1_is_page_2_at_0_33(index):
    top = index.search("What soil pH do tomatoes need?", top_k=1)[0]
    assert top["chunk"]["page"] == 2
    assert round(top["score"], 2) == 0.33
    assert "6.0 and 6.8" in top["chunk"]["text"]


def test_all_six_fixture_questions_top1_correct(index):
    """Top-1 citation correct on 6/6 — the number the README quotes."""
    for question, (page, relevance, phrase) in EXPECTED_QA.items():
        top = index.search(question, top_k=1)[0]
        assert top["chunk"]["page"] == page, question
        assert round(top["score"], 2) == relevance, question
        assert phrase in top["chunk"]["text"], question


def test_extractive_answer_cites_the_page(index):
    results = index.search("What soil pH do tomatoes need?", top_k=3)
    text = extractive_answer(results)
    assert "[p. 2]" in text
    assert "6.0 and 6.8" in text
    assert "nothing is invented" in text


def test_same_question_twice_is_identical(index):
    first = index.search("How long until tomatoes are ready to harvest?")
    second = index.search("How long until tomatoes are ready to harvest?")
    assert [(r["chunk"]["id"], round(r["score"], 6)) for r in first] == [
        (r["chunk"]["id"], round(r["score"], 6)) for r in second
    ]


def test_chunks_never_cross_a_page_boundary():
    pages = [
        {"page": 1, "text": "First page. " + "Tomatoes grow well. " * 40},
        {"page": 2, "text": "Second page. " + "Water them daily. " * 40},
    ]
    chunks = chunk_pages(pages)
    assert chunks, "expected at least one chunk per page"
    assert any(c["page"] == 1 for c in chunks)
    assert any(c["page"] == 2 for c in chunks)
    # No chunk mixes the two pages: page-1 chunks never contain a
    # page-2 sentence, and vice versa.
    for chunk in chunks:
        if chunk["page"] == 1:
            assert "Water them daily" not in chunk["text"]
        else:
            assert "Tomatoes grow well" not in chunk["text"]


def test_empty_question_raises(index):
    with pytest.raises(ValueError):
        index.search("   ")
