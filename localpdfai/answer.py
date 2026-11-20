"""Answer a question from retrieved passages.

Two modes:

* ``extractive`` (default) — quotes the retrieved passages with page
  citations. No LLM, no network, always works. The answer is a quote,
  not a synthesis: it cannot invent facts, but it also cannot rephrase.
* ``ollama`` — sends the passages to a local Ollama model
  (http://localhost:11434) and returns a grounded summary with the same
  citations. ``auto`` tries Ollama and falls back to extractive when
  Ollama is not reachable.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
OLLAMA_TIMEOUT = 120


def _citation(chunk: dict) -> str:
    return f"[p. {chunk['page']}]"


def extractive_answer(results: list[dict]) -> str:
    lines = [
        "Based on the document, here are the most relevant passages:",
        "",
    ]
    for i, result in enumerate(results, start=1):
        chunk = result["chunk"]
        lines.append(f"{i}. {_citation(chunk)} (relevance {result['score']:.2f})")
        lines.append(f"   {chunk['text']}")
        lines.append("")
    lines.append(
        "This is an extractive answer: it quotes the document directly "
        "instead of rephrasing it, so nothing is invented."
    )
    return "\n".join(lines).strip()


def _ollama_answer(question: str, results: list[dict], model: str) -> str | None:
    context = "\n\n".join(
        f"{_citation(r['chunk'])} {r['chunk']['text']}" for r in results
    )
    prompt = (
        "Answer the question using ONLY the passages below. "
        "Quote the page citations like [p. 2] in your answer. "
        "If the passages do not contain the answer, say so.\n\n"
        f"Passages:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    payload = json.dumps(
        {"model": model, "prompt": prompt, "stream": False}
    ).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=OLLAMA_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    return (data.get("response") or "").strip() or None


def answer(question: str, results: list[dict], mode: str = "extractive",
           model: str = OLLAMA_MODEL) -> tuple[str, str]:
    """Return (answer_text, mode_used). mode: extractive | ollama | auto."""
    if mode == "extractive":
        return extractive_answer(results), "extractive"
    if mode == "ollama":
        text = _ollama_answer(question, results, model)
        if text is None:
            raise ConnectionError(
                "could not reach Ollama at http://localhost:11434 — "
                "is Ollama running (`ollama serve`) with a model pulled "
                f"(`ollama pull {model}`)? Use --llm auto to fall back "
                "to extractive answers instead."
            )
        return text, "ollama"
    if mode == "auto":
        text = _ollama_answer(question, results, model)
        if text is not None:
            return text, "ollama"
        return extractive_answer(results) + (
            "\n\n(Note: Ollama was not reachable, so this is the "
            "extractive fallback.)"
        ), "extractive (Ollama unavailable)"
    raise ValueError(f"unknown --llm mode {mode!r} (use extractive, ollama or auto)")
