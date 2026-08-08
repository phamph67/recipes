# AGENTS.md

Guidance for any AI coding agent working in this repository (Claude Code, Codex, Cursor,
Copilot, Gemini CLI, …). This is the single source of truth; tool-specific files point here.

## What this repository is

A personal recipe book published as a static site with **MkDocs + Material**. There is no
application code — the deliverable is Markdown prose plus site config. Your job is to help
**format, index, and organize** recipes, not to invent them.

**Never invent culinary content.** Do not add ingredients, amounts, times, temperatures, or
yields that the user did not supply and that cannot be derived from what is already written.
If a recipe is missing something the house format wants, leave the field out and say what is
missing. A plausible-sounding guess in a recipe book is a ruined dinner.

## Layout

| Path | Purpose |
|---|---|
| `docs/<category>/*.md` | One file per recipe. The directory is its category. |
| `docs/<category>/index.md` | Category landing page; also the section page in the nav. |
| `docs/index.md` | Site home with the category grid. |
| `docs/tags.md` | Auto-generated tag listing (Material's `tags` plugin fills it in). |
| `mkdocs.yml` | Site config. Deliberately has **no `nav:`** — the sidebar is built from the directory tree, so adding a file is all that is needed. |
| `recipe_pdfs/<category>/*.pdf` | Per-recipe PDFs, generated and committed. See below. |
| `scripts/build_pdfs.py` | Renders one PDF per recipe from the built site. |
| `scripts/pdf_link_hook.py` | MkDocs hook adding the "Download PDF" link to recipe pages. |

Canonical categories: `baking`, `breakfast`, `desserts`, `drinks`, `mains`, `prep`, `sides`.
Adding a new category means creating the directory **and** its `index.md`, plus a card in
`docs/index.md` — do all three or the nav and home page disagree. Prefer a new tag over a new
category; categories are for *when you eat it*, and there should stay few enough to scan.

## Category vs. tag

This is the distinction that keeps the site navigable, so apply it consistently:

- **Category (the directory)** answers *when do you eat this?* — one per recipe, no overlap.
- **Tags** answer *what is it made of, how is it made, whose cuisine is it, who can eat it?* —
  as many as apply, and they cut across categories.

So almond cookies live in `desserts/` and are tagged `baking` and `chinese`, not filed under
`baking/`. Sushi rice lives in `prep/` because it is a component, not a dish.

Tag vocabulary in use: cuisine (`chinese`, `japanese`), technique (`baking`, `no-cook`),
form (`cookies`, `rice`, `staple`), dietary (`vegan`, `gluten-free`). Reuse an existing tag
before coining a new one — check with `grep -rh '^  - ' docs --include='*.md' | sort -u`.
Tags are lowercase and singular-ish; match what is already there.

## Recipe file format

Filenames are lowercase `kebab-case.md`, named for the dish (`almond-cookies.md`).

Frontmatter — `title` and `tags` are required, the rest only when actually known:

```yaml
---
title: Almond Cookies
tags:
  - chinese
  - dessert
  - baking
yield: 30–40 cookies
time:
  active: 30m
  total: 2h30m
source: Grandma's index card   # optional: where it came from
---
```

`title` drives the nav label; `tags` drive `docs/tags.md`. Note that Material's tags plugin
only reads `tags:` — a cuisine recorded anywhere else will not produce a browse page, which
is why cuisine is a tag rather than its own key.

Body structure, in this order:

1. `# Recipe Name` — the only H1, matching `title`.
2. An italic one-liner restating yield and time, so the rendered page shows it without the
   reader parsing frontmatter: `*Yield: 30–40 cookies · Active 30 min · Total 2½ h*`.
3. `## Ingredients` — a two-column table, `| Ingredient | Amount |`. When a recipe has
   separable components (dough vs. egg wash), give each a **bolded subheading** and its own
   table, and mark optional ones `*(optional)*`.
4. `## Procedure` (or `## Instructions`) — numbered steps, one action per step.
5. Optional `**Notes**` — substitutions, tolerances, and which steps are purely cosmetic.

House style for amounts:

- Metric by weight (g/ml) for anything where precision matters; tsp/tbsp for small quantities.
- Oven temperatures in **both** °F and °C (`325 °F / 165 °C`).
- Ranges express real latitude (`175–200 g`, `15–17 minutes`). Whenever a range appears, the
  Notes should say what each end of it does — a range without that explanation is incomplete.
- Use en dashes for ranges and `½`-style fractions, matching existing files.

Background asides about ingredient choice (why this rice cultivar, why unsalted butter) go
inline as a **bolded lead-in paragraph** near the relevant table — not in Notes.

## Working rules

- **Ask before editing an existing recipe.** New files you may create freely; a recipe the
  user has already cooked and tuned is theirs. Reformatting, retagging, or recategorizing an
  existing file needs a nod first. Fixing a broken link or typo does not.
- When the user pastes a recipe from elsewhere, convert it to the house format above and file
  it — but carry over only what the source actually says, and list anything you had to leave
  blank.
- After adding or renaming a recipe, run the build and confirm it is clean (see below). A
  rename changes the published URL; there is no redirect plugin configured.
- Existing Markdown files use **CRLF** line endings. `sed -i` patterns anchored with `$` will
  silently fail on them — use the editing tools rather than stream edits.

## Git rules

These are hard rules, not preferences:

- **Never commit or push without asking.** Stop, summarize what changed, and wait for an
  explicit go-ahead — every time, including when the user has approved a commit earlier in the
  same session. Approval covers one commit, not a standing licence.
- **No AI co-author trailers.** Do not add `Co-Authored-By: Claude`, `Generated with …`, or any
  equivalent attribution line to commits.
- **Keep commit messages simple.** A plain subject line saying what changed
  (`add sushi rice recipe`, `fix tag on almond cookies`). No conventional-commit prefixes, no
  ceremony. Add a short body only when the change needs explaining.
- **Summarize before asking.** The summary you present when requesting permission should be a
  real account of the changes — files touched and what each change does — not just the
  proposed subject line.
- **Branches, PRs, and merges are the user's.** On a non-`main` branch, do not open a pull
  request, merge, or otherwise advance the workflow. Do that only when the user explicitly
  asks you to run the PR or merge step.

## Commands

```bash
# One-time setup
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/mkdocs serve          # live preview at http://127.0.0.1:8000
.venv/bin/mkdocs build --strict # build to site/; --strict fails on broken links & bad nav
```

```bash
# Regenerate per-recipe PDFs (requires `mkdocs build` to have run first)
.venv/bin/python scripts/build_pdfs.py
.venv/bin/python scripts/build_pdfs.py --only sushi-rice   # just one
```

`--strict` is the check that matters — it is what CI runs, and it catches the two mistakes
that actually happen here: a link to a category page that does not exist, and a recipe file
whose frontmatter fails to parse.

## PDFs

Every recipe gets its own PDF so a single recipe can be handed to someone without sending
them the whole site. `scripts/build_pdfs.py` drives headless Chromium over the **built**
site, so the PDF carries the Material theme; `docs/stylesheets/extra.css` has the `@media
print` rules that strip the nav and keep ingredient tables from splitting across pages.

- Output lands in both `recipe_pdfs/<category>/<recipe>.pdf` (committed, so GitHub can serve
  a single file) and `site/pdf/…` (what the on-page download link points at).
- CI regenerates the `site/` copies on every deploy. The committed `recipe_pdfs/` copies are
  **not** updated by CI — after changing a recipe, run the script locally and include the
  refreshed PDF in the same commit, or the repo copy goes stale.
- Renaming a recipe orphans its old PDF; delete the stale file by hand.

Local runs need Chromium's system libraries once:
`.venv/bin/python -m playwright install --with-deps chromium chromium-headless-shell`
(needs sudo; CI does this itself).

## Publishing

`.github/workflows/deploy.yml` builds and deploys to GitHub Pages on every push to `main`
(<https://phamph67.github.io/recipes/>). Pages must be set to **Source: GitHub Actions** in
the repository settings for the first deploy to succeed.
