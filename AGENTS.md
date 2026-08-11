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
| `scripts/category_index_hook.py` | MkDocs hook listing a category's recipes on its `index.md`. |
| `input_recipes/` | Ingestion staging: `raw/`, `processed/`, `markdown/`, `failed/`. Local only — contents are gitignored and unreachable from the built site. |

Canonical categories: `breakfast`, `desserts`, `drinks`, `mains`, `prep`, `sides`.
Adding a new category means creating the directory **and** its `index.md`, plus a card in
`docs/index.md` — do all three or the nav and home page disagree. Removing one means the same
three in reverse. Prefer a new tag over a new category; categories are for *when you eat it*,
and there should stay few enough to scan.

**There is deliberately no `baking` category.** It was removed: a technique is not a *when*,
and plenty of things are baked without being a course. `baking` is a tag, which is the better
tool anyway — it cuts across categories and finds bread, cookies, and a baked main in one
place. Do not reintroduce it, and treat it as the worked example when weighing any future
category that names a technique rather than a meal.

## Category vs. tag

This is the distinction that keeps the site navigable, so apply it consistently:

- **Category (the directory)** answers *when do you eat this?* — one per recipe, no overlap.
- **Tags** answer *what is it made of, how is it made, whose cuisine is it, who can eat it?* —
  as many as apply, and they cut across categories.

So almond cookies live in `desserts/` and are tagged `baking` and `chinese`, not filed under
`baking/`. Sushi rice lives in `prep/` because it is a component, not a dish.

### Tag vocabulary

Tags are **faceted**: every tag is `facet/value`. The facet says what kind of statement the
tag makes, which is what keeps the browse pages coherent as the book grows — `vietnamese` on
its own is ambiguous, `cuisine/vietnamese` is not.

Values are lowercase, unaccented, and hyphenated where they need a space, because they become
URL slugs. The vocabulary below is **enforced**: `tags_allowed` in `mkdocs.yml` fails
`mkdocs build --strict` on anything not listed. Adding a value is therefore a deliberate act —
use the `recipe-tag` skill, which updates the vocabulary and the allow list together.

**No single tag is required, but every recipe should carry at least one.** Completeness is
guaranteed by `docs/recipes.md`, the generated A–Z listing of everything in the book, not by
forcing every facet onto every recipe.

**`course/`** — *when do you eat this?* **Derived from the directory, never hand-written.**
`scripts/course_tag_hook.py` injects it, so the tag and the file location cannot disagree.
`breakfast` · `desserts` · `drinks` · `mains` · `prep` · `sides`

**`cuisine/`** — where it is from. One, occasionally two for genuine fusion.
`american` · `british` · `canadian` · `chinese` · `filipino` · `french` · `german` · `greek` ·
`indian` · `italian` · `japanese` · `korean` · `mexican` · `middle-eastern` · `spanish` ·
`thai` · `vietnamese`

**`technique/`** — how it is cooked. Gerunds. Several may apply; tag the ones that decide
whether you can make it tonight, not every verb in the method.
`baking` · `boiling` · `braising` · `deep-frying` · `fermenting` · `frying` · `grilling` ·
`pickling` · `roasting` · `sauteing` · `simmering` · `smoking` · `sous-vide` · `steaming` ·
`stir-frying` · `no-cook`

**`main/`** — the main ingredient, as in what you would shop for. One or two, never five.
`almond` · `beans` · `beef` · `cheese` · `chicken` · `chocolate` · `duck` · `egg` · `fish` ·
`fruit` · `lamb` · `noodles` · `peanut` · `pork` · `potato` · `rice` · `sesame` · `shellfish` ·
`tofu` · `vegetable` · `walnut`

**`form/`** — what kind of thing it is. Answers "I want to bake bread", which neither `course/`
nor `main/` can.
`bread` · `cake` · `cookies` · `dumplings` · `pastry` · `salad` · `sauce` · `soup` · `staple` ·
`stew`

**`profile/`** — how it tastes, including the Cantonese hot/cooling axis. Several may apply.
`sweet` · `savoury` · `spicy` · `tangy` · `heaty` · `cooling`

`heaty` (熱氣, *yeet-hay*) and `cooling` (涼, *leung*) are the food-energetics axis, not
temperature and not spice — `profile/spicy` is a separate statement and the two often co-occur.

**`diet/`** — **the one facet where a wrong tag can hurt someone.** Only when the recipe
qualifies *as written*; never "vegan if you swap the butter". Absence means unclassified, never
"does not qualify" — do not read a missing tag as a negative, and do not add one to a recipe
you have not checked line by line.
`vegan` · `vegetarian` · `pescatarian` · `gluten-free` · `dairy-free` · `nut-free` ·
`egg-free` · `low-carb` · `halal` · `kosher`

**`season/`** — only where the recipe is genuinely seasonal.
`spring` · `summer` · `autumn` · `winter`

**`effort/`** — how hard it is. `easy` · `medium` · `hard`

> **Only the user assigns `effort/`.** It is a judgement about their own kitchen and their own
> skill, and there is no way to infer it from a recipe file. **Never add, change, or guess an
> `effort/` tag** — treat this exactly like "never invent culinary content". A recipe with no
> `effort/` tag is unrated, which is not the same as easy.

Deferred to later issues, deliberately not in the vocabulary: `time/` (bucketed times cannot
answer "under an hour" without OR-ing several tags — needs a real query mechanism first),
`status/` (untested recipes stay in `input_recipes/markdown/` instead), and `from/` (source
attribution stays a Notes line).

To see what is actually in use — the naive `grep -rh '^  - '` also catches `hide:` entries,
so read the `tags:` block specifically:

```bash
awk '/^tags:/{t=1;next} /^[a-zA-Z_-]+:/{t=0} t&&/^ *- /{sub(/^ *- /,"");print}' \
  $(find docs -name '*.md') | sort -u
```

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
---
```

There is no `source:` field. This is not a referenced cookbook, so attribution is prose in
**Notes**, never frontmatter.

**Recipes are family or in-house by default.** Unless a recipe says otherwise, it is the
user's own — discovered, inherited, or tuned over time. Do not add a note saying so; the
absence of one *is* the statement. Never label a recipe as family or in-house yourself, and
never label one as third-party on a hunch — if you cannot tell whose recipe it is, ask.

When a recipe does come from somewhere else, that goes in the **first Notes bullet**, before
anything about technique or substitutions, in one of two forms:

- **Hyperlinked** when the source is a web page:
  `Adapted from [Allrecipes, "Korean BBQ Short Ribs (Gal-Bi)"](https://…).`
- **Bolded** when it cannot be linked — a book, a magazine clipping, a scan, a person:
  `Adapted from **Joy of Cooking**, 1997 edition.` · `From **Bà Ngoại's card**, undated.`

The point of putting it first is that a reader deciding whether the asides are trustworthy
family knowledge or someone else's house style should not have to read to the bottom to find
out. In-house asides may be preserved as written; a third-party recipe's prose may not (see
"Recipes from published sources").

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
- **Do not convert what the source wrote.** This rule is about how *new* recipes are written,
  not a licence to restate an existing one. Record amounts as the source gives them. A weight
  may carry a metric equivalent alongside it (`3 lb (1.36 kg)`) because that is a fact about the
  same quantity; a volume may not be silently turned into millilitres, and a volume of something
  packed or minced may never become a weight at all — that needs a density the source never
  supplied, and inventing one is inventing culinary content. When in doubt, leave it as written
  and say what you left alone.
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
- **Never promote a staged recipe on your own.** Nothing moves from `input_recipes/markdown/`
  into `docs/<category>/` unless the user asks for that file by name. See below.
- When the user pastes a recipe from elsewhere, convert it to the house format above and file
  it — but carry over only what the source actually says, and list anything you had to leave
  blank.
- After adding or renaming a recipe, run the build and confirm it is clean (see below). A
  rename changes the published URL; there is no redirect plugin configured.
- Line endings are normalized to **LF** by `.gitattributes`. Some older files in the working
  copy are still CRLF and are renormalized when next modified; `sed -i` patterns anchored with
  `$` fail silently on those, so use the editing tools rather than stream edits.

## Recipes from published sources

This book is practical, not literary. When a recipe comes from somewhere other than the
user's own kitchen — a website, blog, cookbook scan, magazine clipping, video — take only the
**ingredients and quantities, the procedure, and notes that change the outcome**. Drop the
headnote, the personal story, the SEO padding, equipment plugs, ratings, and nutrition
tables. Genuinely useful background may be rewritten in your own words and placed in Notes.

Two reasons, pointing the same way: the user wants a working reference rather than a
cookbook, and while ingredient lists and procedures are uncopyrightable statements of fact,
the expressive prose around them is not — so reproduce facts, not phrasing.

This does **not** apply to the user's own and family recipes, where the asides are the point
(see the cultivar note in `docs/prep/sushi-rice.md`) — and those are the default, so a recipe
with no stated source is one you leave whole. If you cannot tell whose recipe it is, ask.

Attribution goes in the **first Notes bullet**, hyperlinked for a web source and bolded for
one that cannot be linked. The exact forms are in "Recipe file format" above; that section is
authoritative and this one just points at it.

Claude Code has this as the `recipe-extract` skill in `.claude/skills/`, with fuller detection
signals and keep/drop lists; other tools should follow the summary above.

## Recipe ingestion

Bulk conversion of source files — scans, exports, saved pages — runs through a local staging
pipeline rather than being typed straight into `docs/`. It is an LLM workflow, not application
code, and nothing about it is part of the deployed site or of CI.

```
input_recipes/
├── raw/          # drop zone: sources awaiting parsing
├── processed/    # sources whose parse succeeded, moved here verbatim
├── failed/       # sources that could not be parsed, with a .why.txt beside each
└── markdown/     # output: one .md per recipe, awaiting human review
```

The user drops files in `raw/`. An orchestrator enumerates them and dispatches **one subagent
per source file** — the isolation is the whole point, since one agent parsing a dozen recipes
bleeds amounts and techniques between them. Each subagent parses its one file and writes one
or more house-format proposals into `markdown/`; a single document may hold several recipes.
The source then moves to `processed/`, or to `failed/` if the parse did not produce a usable
recipe. Sources move only after their parse resolves, so `raw/` is always the accurate queue.

**Category is not chosen at parse time** — that needs whole-site context the subagent lacks.
Tags are, drawn from the existing vocabulary, which the orchestrator passes into the prompt.

### Hard rule: no auto-promotion

An agent must **never** move, copy, or otherwise promote a file from `markdown/` into
`docs/<category>/` unless the user explicitly asks for that file. Writing to `markdown/` is
where the parse task ends. Files there are proposals; a human reads them before any of it is
real. This sits alongside "ask before editing an existing recipe" and "never commit without
asking," and is not waived by output that looks obviously correct.

Promotion is a separate, user-driven step: strip the `<!-- REVIEW: … -->` markers and the
`## Review notes` section, pick a category, reuse existing tags, run `mkdocs build --strict`,
regenerate the PDF, then ask before committing.

Nothing under `input_recipes/` is committed — the directory skeleton is, its contents are
gitignored. Sources are routinely other people's copyrighted material and this repo is public,
and `markdown/` is transient by design.

Claude Code has this as four skills in `.claude/skills/`: `recipe-ingest` (the orchestrator),
`recipe-parse` (the per-file worker, which defers to `recipe-extract` for the published-source
keep/drop rules), `recipe-review` (working through what the parsers flagged, and writing
confirmed shorthand back into the language references), and `recipe-promote` (the user-driven
publish step). `recipe-parse` is written as plain instructions — file path in, Markdown out —
so another harness can drive it; only the dispatch step is Claude-Code-specific.

Between parsing and promotion sits **review**, and it is not optional. Parsers are built to
flag rather than guess, so the flags are the product; a proposal nobody has read is a record of
doubt, not a recipe.

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
