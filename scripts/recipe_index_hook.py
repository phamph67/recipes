"""MkDocs hook: build the A–Z listing on docs/recipes.md.

Registered via `hooks:` in mkdocs.yml. Tags are optional and a category answers only one
question, so without a complete list a recipe that nobody thought to tag is reachable only by
search. This page is the backstop: every recipe, alphabetically, whatever it is tagged.

Generated rather than hand-maintained for the same reason as the category listings — adding a
recipe file stays the only step needed to publish it.
"""

import re
from pathlib import PurePosixPath

SKIP_STEMS = {"index", "tags", "recipes"}

TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)


def _title_of(file):
    try:
        with open(file.abs_src_path, encoding="utf-8") as handle:
            head = handle.read(2048)
    except OSError:
        head = ""

    if head.startswith("---"):
        _, _, rest = head.partition("---")
        frontmatter, _, _ = rest.partition("---")
        match = TITLE_RE.search(frontmatter)
        if match:
            return match.group(1)

    return PurePosixPath(file.src_uri).stem.replace("-", " ").title()


def _sort_key(title):
    """Sort ignoring case and leading articles, so "The Best Bread" files under B."""
    key = title.lower()
    for article in ("the ", "a ", "an "):
        if key.startswith(article):
            key = key[len(article):]
            break
    return key


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "recipes.md":
        return markdown

    recipes = [
        f
        for f in files
        if f.src_uri.endswith(".md")
        and len(PurePosixPath(f.src_uri).parts) == 2
        and PurePosixPath(f.src_uri).stem not in SKIP_STEMS
    ]

    if not recipes:
        return f"{markdown.rstrip()}\n\n*No recipes yet.*\n"

    entries = sorted(
        (
            (_title_of(f), PurePosixPath(f.src_uri).parts[0], f.src_uri)
            for f in recipes
        ),
        key=lambda e: _sort_key(e[0]),
    )

    # Group under a letter heading so the page stays scannable as it grows, and so each
    # letter gets a table-of-contents entry.
    out = []
    letter = None
    for title, category, uri in entries:
        initial = _sort_key(title)[:1].upper() or "#"
        if initial != letter:
            letter = initial
            out.append(f"\n## {letter}\n")
        out.append(f"- [{title}]({uri}) <small>· {category}</small>")

    return f"{markdown.rstrip()}\n\n{chr(10).join(out)}\n"
