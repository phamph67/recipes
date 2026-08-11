"""MkDocs hook: derive each recipe's `course/` tag from its directory.

Registered via `hooks:` in mkdocs.yml. A recipe in docs/desserts/ is course/desserts —
always, with no way for the two to disagree. Deriving it is the whole point: a hand-typed
`course/desserts` on a file sitting in desserts/ is a second source of truth that goes stale
the moment the file moves, and nothing in the build would notice.

Recipes therefore never carry a course/ tag in their frontmatter. If one does, it is a
mistake, and it is dropped here in favour of the directory.
"""

from pathlib import PurePosixPath

SKIP_STEMS = {"index", "tags", "recipes"}

PREFIX = "course/"


def on_page_markdown(markdown, page, config, files):
    src = PurePosixPath(page.file.src_uri)

    # Recipes are docs/<category>/<recipe>.md; anything else is a nav page.
    if len(src.parts) != 2 or src.stem in SKIP_STEMS:
        return markdown

    course = f"{PREFIX}{src.parts[0]}"

    tags = page.meta.get("tags") or []
    # Drop any hand-written course/ tag; the directory is authoritative.
    tags = [t for t in tags if not str(t).startswith(PREFIX)]
    tags.append(course)
    page.meta["tags"] = tags

    return markdown
