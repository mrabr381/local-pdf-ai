"""Split page text into overlapping chunks that keep their page number."""

from __future__ import annotations

import re

MAX_CHUNK_CHARS = 600
OVERLAP_CHARS = 100

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def _sentences(text: str) -> list[str]:
    parts = [s.strip() for s in _SENTENCE_END.split(text) if s.strip()]
    # A very long "sentence" (e.g. a wall of text with no punctuation)
    # is hard-split so no chunk ever grows unbounded.
    out: list[str] = []
    for part in parts:
        while len(part) > MAX_CHUNK_CHARS:
            cut = part.rfind(" ", 0, MAX_CHUNK_CHARS)
            cut = cut if cut > 100 else MAX_CHUNK_CHARS
            out.append(part[:cut].strip())
            part = part[cut:].strip()
        if part:
            out.append(part)
    return out


def chunk_pages(pages: list[dict]) -> list[dict]:
    """Turn [{'page': n, 'text': ...}] into chunks.

    Each chunk is {'id': int, 'page': int, 'text': str}. Chunks never
    cross a page boundary, so every citation points at exactly one page.
    """
    chunks: list[dict] = []
    for page in pages:
        sentences = _sentences(" ".join(page["text"].split()))
        current = ""
        for sentence in sentences:
            candidate = f"{current} {sentence}".strip() if current else sentence
            if len(candidate) > MAX_CHUNK_CHARS and current:
                chunks.append(
                    {"id": len(chunks), "page": page["page"], "text": current}
                )
                # Overlap: carry the tail of the finished chunk forward.
                current = current[-OVERLAP_CHARS:] + " " + sentence
                current = current.strip()
                if len(current) > MAX_CHUNK_CHARS:
                    chunks.append(
                        {"id": len(chunks), "page": page["page"], "text": current}
                    )
                    current = ""
            else:
                current = candidate
        if current:
            chunks.append({"id": len(chunks), "page": page["page"], "text": current})
    return chunks
