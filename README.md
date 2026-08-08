# Recipes

A personal recipe book, published with [MkDocs](https://www.mkdocs.org/) +
[Material](https://squidfunk.github.io/mkdocs-material/) at
**<https://phamph67.github.io/recipes/>**.

Recipes are plain Markdown in `docs/<category>/`, one file per recipe, with YAML frontmatter
for the title and tags. The category directory says *when you eat it*; tags cover cuisine,
technique, and dietary notes and cut across categories.

Categories: `baking` · `breakfast` · `desserts` · `drinks` · `mains` · `prep` · `sides`

## Local preview

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve          # http://127.0.0.1:8000
.venv/bin/mkdocs build --strict # what CI runs
```

Pushing to `main` builds and deploys the site via GitHub Actions.

## PDFs

Every recipe has a standalone PDF, for handing a single recipe to someone. They live in
`recipe_pdfs/<category>/` and are linked from the top of each recipe page on the site.

```bash
# one-time: Chromium's system libraries (needs sudo)
.venv/bin/python -m playwright install --with-deps chromium chromium-headless-shell

.venv/bin/mkdocs build
.venv/bin/python scripts/build_pdfs.py            # all recipes
.venv/bin/python scripts/build_pdfs.py --only sushi-rice
```

The script prints the *built* pages, so PDFs match the site's styling. Regenerate and commit
the PDF whenever you change a recipe — CI refreshes the published copies but not the ones in
the repo.

## Working with an AI agent

[`AGENTS.md`](AGENTS.md) holds the house format and working rules, and is read by Claude Code,
Codex, Cursor, and Copilot alike.
