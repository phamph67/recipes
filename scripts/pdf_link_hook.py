"""MkDocs hook: put a "Download PDF" link on every recipe page.

Registered via `hooks:` in mkdocs.yml. The link is emitted as raw HTML rather than a
Markdown link on purpose — MkDocs' --strict link validation would flag a Markdown link to
a .pdf that does not exist until scripts/build_pdfs.py has run.
"""

from pathlib import PurePosixPath

SKIP_STEMS = {"index", "tags"}


def on_page_markdown(markdown, page, config, files):
    src = PurePosixPath(page.file.src_uri)

    # Recipes are docs/<category>/<recipe>.md; anything else is a nav page.
    if len(src.parts) != 2 or src.stem in SKIP_STEMS:
        return markdown

    depth = len(src.parts)  # <recipe>/ pages sit one directory deep once built
    prefix = "../" * depth
    href = f"{prefix}pdf/{src.with_suffix('.pdf').as_posix()}"

    # markdown="1" lets the Material icon shortcode render inside the raw HTML block
    # (md_in_html is enabled in mkdocs.yml).
    link = (
        f'<p class="recipe-pdf-link" markdown="1"><a href="{href}" download>'
        ":material-file-pdf-box: Download this recipe as a PDF</a></p>\n\n"
    )

    # Place it after the H1 so it sits under the title rather than above it.
    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: i + 1]) + "\n\n" + link + "\n".join(lines[i + 1 :])
    return link + markdown
