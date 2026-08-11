"""MkDocs hook: list a category's recipes on its landing page.

Registered via `hooks:` in mkdocs.yml. Category pages (docs/<category>/index.md) carry only
a heading and a one-line description, so without this they are a dead end — the recipes are
reachable from the sidebar but not from the page itself, and the page has no headings, which
leaves Material's table of contents empty.

Generating the list at build time rather than hand-maintaining it keeps the promise made in
mkdocs.yml: adding a recipe file is the only step needed to publish it.
"""

import re
from pathlib import PurePosixPath

SKIP_STEMS = {"index", "tags"}

# Frontmatter `title:`, with optional surrounding quotes.
TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)


def _title_of(file):
    """Read a recipe's frontmatter title straight from its source.

    Deliberately not `file.page.title` — page titles are not populated for every page at the
    point on_page_markdown runs for *this* page, so a sibling's title may still be None.
    """
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

    # Fall back to the filename: almond-cookies -> Almond Cookies
    return PurePosixPath(file.src_uri).stem.replace("-", " ").title()


def on_page_markdown(markdown, page, config, files):
    src = PurePosixPath(page.file.src_uri)

    # Only category landing pages: docs/<category>/index.md
    if len(src.parts) != 2 or src.stem != "index":
        return markdown

    category = src.parts[0]

    siblings = [
        f
        for f in files
        if f.src_uri.endswith(".md")
        and PurePosixPath(f.src_uri).parts[:1] == (category,)
        and len(PurePosixPath(f.src_uri).parts) == 2
        and PurePosixPath(f.src_uri).stem not in SKIP_STEMS
    ]

    # An empty category renders as-is; a "Recipes" heading over nothing reads as a bug.
    if not siblings:
        return markdown

    entries = sorted(
        (_title_of(f), PurePosixPath(f.src_uri).name) for f in siblings
    )
    listing = "\n".join(f"- [{title}]({name})" for title, name in entries)

    count = len(entries)
    heading = f"## Recipes\n\n{listing}\n"
    if count > 1:
        heading = f"## Recipes ({count})\n\n{listing}\n"

    return f"{markdown.rstrip()}\n\n{heading}"
