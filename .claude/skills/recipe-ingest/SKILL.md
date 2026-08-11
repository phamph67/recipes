---
name: recipe-ingest
description: Orchestrate the recipe ingestion pipeline — enumerate source files in input_recipes/raw/, dispatch one isolated subagent per file to parse it, and file each source into processed/ or failed/. Use when the user asks to ingest, parse, or process the recipes they have dropped in input_recipes/raw/, or to run the ingestion pipeline.
---

# Orchestrating recipe ingestion

Turn everything sitting in `input_recipes/raw/` into staged Markdown proposals in
`input_recipes/markdown/`, one subagent per source file.

**You are a dispatcher, not a cook.** Do not read recipe content yourself. Reading two sources
into one context is exactly the failure this design exists to prevent — amounts and techniques
from one recipe bleeding into another. Your context holds file names and status, nothing more.

## Before dispatching

1. **Enumerate the queue.** List `input_recipes/raw/`, ignoring `.gitkeep` and dotfiles. If it
   is empty, say so and stop.
2. **Collect the tag vocabulary** — subagents have no repo context and must be given it:

   ```bash
   awk '/^tags:/{t=1;next} /^[a-zA-Z_-]+:/{t=0} t&&/^ *- /{sub(/^ *- /,"");print}' \
     $(find docs -name '*.md') | sort -u
   ```

   Pass the **whole faceted vocabulary from `AGENTS.md` → "Tag vocabulary"**, not just the tags
   currently in use — the in-use list is short, and a subagent given only it will coin
   near-duplicates of values the book has already standardised on. Values are enforced by
   `tags_allowed`, so an invented one fails the build later; tell subagents to flag rather than
   coin, and to write neither `course/` (derived from the directory) nor `effort/` (the user's
   alone).

3. **Classify each file by how it must be read**, from its extension and, for PDFs, whether it
   has a text layer. Probe for embedded fonts rather than reaching for `pdftotext` — poppler is
   not installed everywhere, and a missing binary silently reports "no text" for *every* PDF,
   which sends digital PDFs to the expensive tier for the rest of time:

   ```bash
   python3 -c "
   import re,sys
   d=open(sys.argv[1],'rb').read()
   print('scan' if not re.search(rb'/Font', d) else 'digital')
   " <file>
   ```

   A PDF with no `/Font` object has nothing to extract and is a scan. If you do reach for a
   command-line tool, check it exists first (`command -v pdftotext`) and treat its absence as
   "cannot tell" rather than as an answer.

   - **Text-ish** — `.txt`, `.md`, `.html`, `.docx`, digital PDF → Sonnet-class subagent.
   - **Scan or image** — image files, PDFs with no text layer → **Opus-class, vision-capable**
     subagent. This is the one place the uniform model tier deliberately breaks: a text-only
     agent handed a scan produces invented content rather than an error.

   If you cannot tell, treat it as a scan. The cost of over-provisioning is money; the cost of
   under-provisioning is a wrong recipe.

## Dispatch

One subagent per file, in parallel where the harness allows. In Claude Code, dispatch the
**`recipe-parser`** agent (`.claude/agents/recipe-parser.md`), which is already scoped and
tool-limited for this. Override its model per the classification in step 3: leave it at its
default `sonnet` for text-ish files, pass `model: opus` for scans and images.

Each prompt contains **only**:

- The single absolute source file path — never a directory, never a second file.
- An instruction to use the **`recipe-parse`** skill and follow it exactly.
- The tag vocabulary from step 2.
- Whether the user asked for multi-language output (default: English only).
- If the source is Vietnamese, a pointer to `references/vietnamese.md` — the shorthand there
  is where quantity errors come from.

Do not summarize the source, pre-extract anything, or tell the subagent what you think the
recipe is. It reads the file; you do not.

## After each subagent returns

Judge success only by whether at least one well-formed recipe file was written to
`input_recipes/markdown/`. Verify the file exists — do not take the report on faith. Then:

- **Success** → `git mv`-free plain `mv` of the source into `input_recipes/processed/`,
  verbatim and unrenamed. `processed/` is a dump, not a structured archive. Moving (never
  copying, never deleting) is what keeps `raw/` an accurate queue of outstanding work.
- **Failure** — unreadable scan, not actually a recipe, subagent errored → move the source to
  `input_recipes/failed/` and write a sibling `<filename>.why.txt` giving the reason in a line
  or two. Leaving it in `raw/` would re-run it on every future invocation.

Move the source only *after* its parse resolves. A crash mid-run must leave the queue accurate.

## Report

A short summary table: source file → recipes emitted (or failure reason), plus a combined list
of what subagents flagged for review. Then tell the user the proposals are in
`input_recipes/markdown/` and awaiting their review.

**Collect and surface unrecognized shorthand.** Subagents cannot reach the user; you are the
only route. Gather every `### Unrecognized shorthand` item the subagents reported, deduplicate
across files, and put them to the user as a short numbered list — literal text, where it
appeared, the subagent's hypothesis. Ask which readings are correct.

Then act on the answer: add confirmed readings to the relevant reference file under
`.claude/skills/recipe-parse/references/`, marked as user-confirmed, and correct the affected
staged files in `markdown/`. Leave anything unconfirmed unexpanded and flagged. This is how
the references improve — a shorthand confirmed once is never guessed at again.

## Where you stop

**Never promote anything into `docs/<category>/`.** Not as a convenience, not when the output
looks obviously correct, not when the whole batch parsed cleanly. Files in `markdown/` are
proposals until a human reads them, and promotion happens only when the user names a file and
asks for it.

Do not commit or push. Do not regenerate PDFs. Both are separate steps the user drives.

## Promotion, when the user does ask

A separate, user-driven step with its own skill: **`recipe-promote`**, per file, by name.
Do not inline its steps here or run them as part of an ingest.
