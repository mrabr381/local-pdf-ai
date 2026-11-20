"""Extract text from a PDF, page by page (pypdf)."""

from __future__ import annotations

import os

from pypdf import PdfReader


class PdfReadError(ValueError):
    """Raised when a PDF cannot be read or has no extractable text."""


def extract_pages(path: str) -> list[dict]:
    """Return [{'page': 1-based number, 'text': str}, ...] for a PDF.

    Raises PdfReadError on a missing/unreadable file or a PDF with no
    extractable text at all (e.g. a scanned image-only PDF).
    """
    if not os.path.isfile(path):
        raise PdfReadError(f"file not found: {path}")
    try:
        reader = PdfReader(path)
    except Exception as exc:  # corrupt / encrypted / not a PDF
        raise PdfReadError(f"could not read PDF {path!r}: {exc}") from exc

    pages: list[dict] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append({"page": i, "text": text.strip()})

    if not any(p["text"] for p in pages):
        raise PdfReadError(
            f"no extractable text in {path!r} — it may be a scanned "
            "image-only PDF (OCR is not supported yet)"
        )
    return pages
