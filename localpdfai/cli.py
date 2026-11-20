"""Command line interface.

Usage:
    python -m localpdfai index --pdf doc.pdf [--out index.json] [--backend tfidf|st]
    python -m localpdfai ask --pdf doc.pdf --q "your question"
                        [--index index.json] [--top-k 3]
                        [--llm extractive|ollama|auto] [--backend tfidf|st]

Exit codes: 0 ok, 1 runtime error (missing file, no text, empty question,
Ollama unreachable in --llm ollama mode), 2 bad arguments.
"""

from __future__ import annotations

import argparse
import os
import sys

from .answer import answer
from .index import Index
from .pdfio import PdfReadError


def _default_index_path(pdf_path: str) -> str:
    base, _ = os.path.splitext(pdf_path)
    return base + ".localpdfai.json"


def _load_or_build(pdf_path: str, index_path: str | None, backend: str) -> Index:
    if index_path and os.path.isfile(index_path):
        index = Index.load(index_path)
        if os.path.abspath(index.source) != os.path.abspath(pdf_path):
            print(
                f"warning: index {index_path} was built for {index.source}, "
                f"not {pdf_path} — rebuilding",
                file=sys.stderr,
            )
        else:
            return index
    return Index.build(pdf_path, backend=backend)


def cmd_index(args: argparse.Namespace) -> int:
    try:
        index = Index.build(args.pdf, backend=args.backend)
    except (PdfReadError, ImportError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out = args.out or _default_index_path(args.pdf)
    index.save(out)
    pages = sorted({c["page"] for c in index.chunks})
    print(f"indexed {args.pdf}")
    print(f"  pages: {len(pages)}  chunks: {len(index.chunks)}  backend: {args.backend}")
    print(f"  index saved to {out}")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    if not args.q or not args.q.strip():
        print("error: question must not be empty", file=sys.stderr)
        return 1
    try:
        index = _load_or_build(args.pdf, args.index, args.backend)
    except (PdfReadError, ImportError, ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    results = index.search(args.q, top_k=args.top_k)
    if not results or results[0]["score"] <= 0:
        print("No relevant passage found in this document for that question.")
        print("Try different words, or check the PDF actually covers the topic.")
        return 0
    try:
        text, mode_used = answer(args.q, results, mode=args.llm)
    except ConnectionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Answer ({mode_used}):\n")
    print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="localpdfai",
        description="Ask questions about your PDFs — 100% local, no upload, no key.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="build a search index for a PDF")
    p_index.add_argument("--pdf", required=True, help="PDF file to index")
    p_index.add_argument("--out", help="where to save the index JSON")
    p_index.add_argument("--backend", default="tfidf", choices=["tfidf", "st"],
                         help="embedding backend (default: tfidf)")
    p_index.set_defaults(func=cmd_index)

    p_ask = sub.add_parser("ask", help="ask a question about a PDF")
    p_ask.add_argument("--pdf", required=True, help="PDF file to ask about")
    p_ask.add_argument("--q", required=True, help="question in plain English")
    p_ask.add_argument("--index", help="existing index JSON to reuse")
    p_ask.add_argument("--top-k", type=int, default=3,
                       help="passages to retrieve (default: 3)")
    p_ask.add_argument("--llm", default="extractive",
                       choices=["extractive", "ollama", "auto"],
                       help="answer mode (default: extractive)")
    p_ask.add_argument("--backend", default="tfidf", choices=["tfidf", "st"],
                       help="embedding backend (default: tfidf)")
    p_ask.set_defaults(func=cmd_ask)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
