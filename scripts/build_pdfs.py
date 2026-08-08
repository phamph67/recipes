#!/usr/bin/env python3
"""Render one PDF per recipe from the built MkDocs site.

Chromium prints the *built* pages, so the PDFs carry the Material theme and match what
the site looks like. This replaces printing raw Markdown by hand from a VS Code extension.

Output goes to two places:

  recipe_pdfs/<category>/<recipe>.pdf   committed, so a single recipe can be handed to
                                        someone straight from the GitHub repo
  site/pdf/<category>/<recipe>.pdf      served alongside the site, which is what the
                                        "Download PDF" link on each page points at

Usage:
    .venv/bin/mkdocs build
    .venv/bin/python scripts/build_pdfs.py [--only sushi-rice]
"""

from __future__ import annotations

import argparse
import http.server
import shutil
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOCS = ROOT / "docs"
PDF_REPO_DIR = ROOT / "recipe_pdfs"
PDF_SITE_DIR = SITE / "pdf"

# Pages that are navigation rather than recipes; they get no PDF.
SKIP_STEMS = {"index", "tags"}


def recipe_pages() -> list[tuple[str, str]]:
    """Return (url_path, relative_output_path) for every recipe page."""
    pages = []
    for md in sorted(DOCS.glob("*/*.md")):
        if md.stem in SKIP_STEMS:
            continue
        rel = md.relative_to(DOCS).with_suffix("")
        pages.append((f"{rel.as_posix()}/", f"{rel.as_posix()}.pdf"))
    return pages


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def log_message(self, *args):  # noqa: D102 - silence per-request logging
        pass


def serve() -> tuple[socketserver.TCPServer, int]:
    """Serve the built site locally.

    Printing over http:// rather than file:// matters: Material's absolute asset paths
    and the search index do not resolve under file://, so the PDFs come out unstyled.
    """
    httpd = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="render just the recipe whose filename stem matches")
    args = parser.parse_args()

    if not (SITE / "index.html").exists():
        print("site/ not found — run `mkdocs build` first.", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "playwright is not installed. Run:\n"
            "  .venv/bin/pip install -r requirements.txt\n"
            "  .venv/bin/python -m playwright install --with-deps chromium",
            file=sys.stderr,
        )
        return 1

    pages = recipe_pages()
    if args.only:
        pages = [p for p in pages if Path(p[1]).stem == args.only]
        if not pages:
            print(f"no recipe matching {args.only!r}", file=sys.stderr)
            return 1

    httpd, port = serve()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            for url_path, out_rel in pages:
                page.goto(f"http://127.0.0.1:{port}/{url_path}", wait_until="networkidle")
                for out_dir in (PDF_REPO_DIR, PDF_SITE_DIR):
                    out = out_dir / out_rel
                    out.parent.mkdir(parents=True, exist_ok=True)
                page.pdf(
                    path=str(PDF_REPO_DIR / out_rel),
                    format="A4",
                    print_background=True,
                    margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"},
                )
                shutil.copy2(PDF_REPO_DIR / out_rel, PDF_SITE_DIR / out_rel)
                print(f"  {out_rel}")
            browser.close()
    finally:
        httpd.shutdown()

    print(f"{len(pages)} PDF(s) written to {PDF_REPO_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
