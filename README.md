# Recipes

The recipe book itself lives at **<https://phamph67.github.io/recipes/>** — that is where you
read and cook from. This README covers working *on* the repository: the agent skills, how to
run and test the site locally, and how it deploys.

House rules for content — the recipe file format, category vs. tag, what to strip from a
published source — live in [`AGENTS.md`](AGENTS.md), which every agent tool reads. Two of them
are worth stating here because they shape every recipe in the book:

- **Recipes are family or in-house by default.** A recipe with no stated source is one of
  yours. When a recipe *does* come from elsewhere, that is the first bullet under **Notes** —
  hyperlinked for a web source, **bolded** for a book, clipping, scan, or person.
- **Tags are faceted and enforced** — `cuisine/`, `technique/`, `main/`, `form/`, `profile/`,
  `diet/`, `season/`, `effort/`, plus `course/` derived from the directory. The vocabulary is
  in [`AGENTS.md`](AGENTS.md) and enforced by `tags_allowed`, so an invented tag fails the
  build. `effort/` is yours alone — agents never assign it.

## Agent skills

Seven workflows, in `.claude/skills/`. Claude Code picks them up automatically; other tools can
be pointed at the `SKILL.md` files directly.

| Skill | Use it when |
|---|---|
| `recipe-extract` | A recipe is pasted or linked from a published source — website, blog, cookbook scan, video. Decides what to keep and what to drop, and owns the copyright reasoning. |
| `recipe-ingest` | Bulk-converting the files sitting in `input_recipes/raw/`. Orchestrates the pipeline below. |
| `recipe-parse` | Parsing **one** source file into house format. Normally invoked by `recipe-ingest`, not by hand. Defers to `recipe-extract` for keep/drop. |
| `recipe-review` | Working through what the parsers flagged — groups the questions by kind, collects your answers, and writes confirmed shorthand back into the language references. |
| `recipe-promote` | Moving a reviewed proposal from `input_recipes/markdown/` into `docs/`. |
| `recipe-category` | Adding or removing a category, keeping the directory, home-page card, and rules text in step. |
| `recipe-tag` | Adding, renaming, or retiring a value in the faceted tag vocabulary, keeping `AGENTS.md` and the enforced `tags_allowed` list in step. |

The per-file worker runs as a defined subagent, `.claude/agents/recipe-parser.md` — scoped to
one file, tool-limited, `sonnet` by default with the orchestrator overriding to `opus` for
scans. That file is the Claude Code dispatch shim; the portable contract stays in
`recipe-parse/SKILL.md`, so another harness reimplements the shim and reuses the skill.

Language references for parsing live in `.claude/skills/recipe-parse/references/`:
`vietnamese.md` (measurement shorthand like `mcf`/`mc`/`cf`, missing diacritics, container
measures that must not be silently converted) and `french.md` (France vs. Québec vocabulary,
the `thermostat` oven scale, Canadian cream by fat percentage).

**These references are meant to grow.** When a parser meets a shorthand it cannot confirm, it
leaves the text unexpanded, flags it, and reports it — and the orchestrator asks you at the end
of the run. Confirmed readings get written into the reference file, so each one is only ever
asked once.

## Importing recipes

Two paths, depending on how many you have.

### One recipe, interactively

Paste it into the chat, or point the agent at a URL or file. It applies `recipe-extract` and
writes straight into `docs/<category>/`. Fine for a single recipe; it does not scale, and
several recipes in one session start bleeding into each other.

### A batch — the ingestion pipeline

```
input_recipes/
├── raw/          # 1. you drop source files here
├── processed/    # 3. sources that parsed successfully, moved here
├── failed/       #    sources that did not, each with a .why.txt
└── markdown/     # 2. proposals land here, awaiting your review
```

1. **Drop sources in `input_recipes/raw/`.** Any mix of `.txt`, `.md`, `.html`, `.docx`,
   PDFs, or image scans. No naming convention needed.
2. **Ask the agent to ingest them** ("ingest the recipes in raw", or invoke `recipe-ingest`).
   It dispatches one isolated subagent per file — that isolation is the point, since one agent
   reading a dozen recipes mixes up their amounts and techniques. Scans go to a vision-capable
   model; everything else to a cheaper tier. One document may produce several recipes.
3. **Read what lands in `markdown/`.** These are *proposals*, not recipes. Each one flags its
   soft spots inline as `<!-- REVIEW: … -->` and summarizes them in a `## Review notes`
   section — ambiguous handwriting, amounts that were converted rather than read, fields the
   source never gave. Check those against the original, which is now in `processed/`.
4. **Promote the ones you approve**, by name: "promote almond-cookies". The agent strips the
   review markers, picks a category, runs the strict build, and regenerates the PDF.

**The agent will never promote anything on its own.** Nothing reaches `docs/` without you
asking for that specific file, however clean the output looks. Nothing under `input_recipes/`
is ever committed — the directory skeleton is, the contents are gitignored, since sources are
usually other people's copyrighted material and this repo is public.

Anything that failed to parse is in `failed/` with a note saying why. Fix it and move it back
to `raw/` to retry, or convert it by hand.

## Running and testing locally

```bash
# one-time setup
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/mkdocs serve          # live preview at http://127.0.0.1:8000
.venv/bin/mkdocs build --strict # what CI runs — the check that matters
```

`--strict` is the test suite. There is no application code, so it is the only automated check,
and it catches the two mistakes that actually happen: a link to a category page that does not
exist, and frontmatter that fails to parse. Run it after adding or renaming any recipe.

A rename changes the published URL — there is no redirect plugin — and orphans the old PDF,
which has to be deleted by hand.

## PDFs

Every recipe gets a standalone PDF so one recipe can be handed to someone without sending the
whole site. `scripts/build_pdfs.py` drives headless Chromium over the *built* site, so PDFs
carry the site's styling.

```bash
# one-time: Chromium's system libraries (needs sudo)
.venv/bin/python -m playwright install --with-deps chromium chromium-headless-shell

.venv/bin/mkdocs build                                  # must run first
.venv/bin/python scripts/build_pdfs.py                  # all recipes
.venv/bin/python scripts/build_pdfs.py --only sushi-rice
```

Output goes to `recipe_pdfs/<category>/` (committed, so GitHub can serve a single file) and
`site/pdf/` (what the on-page download link points at). CI refreshes only the `site/` copies —
after changing a recipe, regenerate locally and include the PDF in the same commit, or the
repo copy goes stale.

## Deploying

`.github/workflows/deploy.yml` builds and deploys to GitHub Pages on **every push to `main`**.
There is no manual deploy step and no staging environment; merging is publishing.

Repository settings must have Pages set to **Source: GitHub Actions**. CI runs
`mkdocs build --strict` and installs Chromium itself; it does not touch `input_recipes/`.

Agents do not commit, push, merge, or open pull requests without being asked — see the Git
rules in [`AGENTS.md`](AGENTS.md).
