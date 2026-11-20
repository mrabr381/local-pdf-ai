"""Document embeddings.

Two backends, one interface (`embed(texts) -> np.ndarray`, rows L2-normalised):

* ``tfidf`` (default) — small, pure-NumPy TF-IDF. No model download, no
  network, deterministic, fast. Good for keyword-heavy factual questions.
* ``st`` (opt-in) — sentence-transformers ``all-MiniLM-L6-v2``. Semantic
  matching, but needs torch (~2 GB install) and a one-time ~90 MB model
  download. Only used when ``--backend st`` is passed AND the package
  is installed; otherwise a clear error tells the user how to enable it.
"""

from __future__ import annotations

import math
import re

import numpy as np

_TOKEN = re.compile(r"[a-z0-9]+")

# Small English stopword list (kept short on purpose: the goal is to
# drop glue words, not to do linguistics).
STOPWORDS = frozenset(
    """
    a an the and or but if then else for of to in on at by with from as is are
    was were be been being it its this that these those there here what which
    who whom how when where why can could should would will shall may might
    do does did have has had not no yes you your he she we they them his her
    our their i me my we us our do does did is am are was were be been being
    """.split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in STOPWORDS]


class TfidfEmbedder:
    """Fit-once TF-IDF over the document's own chunks."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}
        self.idf: np.ndarray = np.zeros(0)

    def fit(self, texts: list[str]) -> None:
        df: dict[str, int] = {}
        for text in texts:
            for token in set(tokenize(text)):
                df[token] = df.get(token, 0) + 1
        self.vocab = {token: i for i, token in enumerate(sorted(df))}
        n = max(len(texts), 1)
        self.idf = np.array(
            [math.log((n + 1) / (df[token] + 1)) + 1.0 for token in sorted(df)],
            dtype=np.float64,
        )

    def embed(self, texts: list[str]) -> np.ndarray:
        rows = np.zeros((len(texts), len(self.vocab)), dtype=np.float64)
        for r, text in enumerate(texts):
            counts: dict[int, float] = {}
            for token in tokenize(text):
                idx = self.vocab.get(token)
                if idx is not None:
                    counts[idx] = counts.get(idx, 0.0) + 1.0
            for idx, count in counts.items():
                # log-scaled TF x IDF
                rows[r, idx] = (1.0 + math.log(count)) * self.idf[idx]
        norms = np.linalg.norm(rows, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return rows / norms


class SentenceTransformerEmbedder:
    """Optional semantic backend (sentence-transformers, lazy import)."""

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is not installed. Install it with "
                "`pip install sentence-transformers` (needs torch, ~2 GB) "
                "or use the default --backend tfidf."
            ) from exc
        self._model = SentenceTransformer(self.MODEL_NAME)

    def fit(self, texts: list[str]) -> None:  # noqa: ARG002 — no fitting needed
        return None

    def embed(self, texts: list[str]) -> np.ndarray:
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return np.asarray(vectors, dtype=np.float64)


def make_embedder(backend: str):
    """Return an embedder for 'tfidf' (default) or 'st'."""
    if backend == "tfidf":
        return TfidfEmbedder()
    if backend == "st":
        return SentenceTransformerEmbedder()
    raise ValueError(f"unknown backend {backend!r} (use 'tfidf' or 'st')")
