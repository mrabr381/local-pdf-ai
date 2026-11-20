"""In-process vector index: chunks + embeddings, cosine search, JSON save/load."""

from __future__ import annotations

import json
import os

import numpy as np

from .chunking import chunk_pages
from .embeddings import make_embedder
from .pdfio import PdfReadError, extract_pages


class Index:
    def __init__(self, chunks: list[dict], matrix: np.ndarray, embedder, backend: str, source: str):
        self.chunks = chunks
        self.matrix = matrix
        self.embedder = embedder
        self.backend = backend
        self.source = source

    # -- construction -------------------------------------------------
    @classmethod
    def build(cls, pdf_path: str, backend: str = "tfidf") -> "Index":
        pages = extract_pages(pdf_path)
        chunks = chunk_pages(pages)
        if not chunks:
            raise PdfReadError(f"no chunks could be built from {pdf_path!r}")
        embedder = make_embedder(backend)
        embedder.fit([c["text"] for c in chunks])
        matrix = embedder.embed([c["text"] for c in chunks])
        return cls(chunks, matrix, embedder, backend, os.path.abspath(pdf_path))

    # -- search --------------------------------------------------------
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not query.strip():
            raise ValueError("question must not be empty")
        query_vec = self.embedder.embed([query])[0]
        scores = self.matrix @ query_vec  # cosine: rows are normalised
        order = np.argsort(-scores, kind="stable")  # stable: ties keep chunk order
        results = []
        for idx in order[:top_k]:
            results.append(
                {
                    "chunk": self.chunks[int(idx)],
                    "score": float(scores[int(idx)]),
                }
            )
        return results

    # -- persistence ---------------------------------------------------
    def save(self, path: str) -> None:
        data = {
            "backend": self.backend,
            "source": self.source,
            "chunks": self.chunks,
            "matrix": self.matrix.tolist(),
        }
        if self.backend == "tfidf":
            data["vocab"] = self.embedder.vocab
            data["idf"] = self.embedder.idf.tolist()
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)

    @classmethod
    def load(cls, path: str) -> "Index":
        if not os.path.isfile(path):
            raise FileNotFoundError(f"index file not found: {path}")
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        embedder = make_embedder(data["backend"])
        if data["backend"] == "tfidf":
            embedder.vocab = {k: int(v) for k, v in data["vocab"].items()}
            embedder.idf = np.array(data["idf"], dtype=np.float64)
        matrix = np.array(data["matrix"], dtype=np.float64)
        return cls(data["chunks"], matrix, embedder, data["backend"], data["source"])
