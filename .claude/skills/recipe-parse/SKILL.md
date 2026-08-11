---
name: recipe-parse
description: Parse one source file from input_recipes/raw/ into one or more house-format Markdown recipes staged in input_recipes/markdown/ for human review. Use when converting a dropped source file — text, HTML, Word/Docs export, digital PDF, or a scan — as part of the ingestion pipeline. Handles file input and staging output; defers to recipe-extract for what to keep and drop from a published source.
---

# Parsing one source file into a staged recipe

You have been given **exactly one** source file path. Read it, extract every recipe it
contains, and write each one as house-format Markdown into `input_recipes/markdown/`.

That is the whole job. You are deliberately scoped to a single file so that amounts,
techniques, and phrasing from unrelated recipes cannot bleed into this one. Do not read other
files in `raw/`, and do not consider what other recipes might exist.

## What this skill does not own

Two things live elsewhere. Read them rather than working from memory, and do not restate their
rules in your output:

- **What to keep and what to drop from a published source** — headnotes, SEO padding,
  equipment plugs, ratings, the copyright reasoning — is owned by the **`recipe-extract`**
  skill (`.claude/skills/recipe-extract/SKILL.md`). Apply it whenever the source is published
  or otherwise not the user's own. Its signals for telling the difference apply here too, with
  one addition: a file dropped in `raw/` is more likely than a chat paste to be a scan of a
  family recipe card. If you cannot tell whose recipe it is, do not guess — flag it (below)
  and let the reviewer decide.
- **The house format** — frontmatter keys, the H1 and italic yield/time line, ingredient
  tables, step numbering, units, dashes and fractions — is owned by **`AGENTS.md`**
  ("Recipe file format"). Follow it exactly.

If those two documents and this one ever disagree, they win.

## The rule that overrides everything

**Never invent culinary content.** No ingredient, amount, time, temperature, or yield that the
source does not supply and that cannot be derived from what is written. Where a house-format
field is unavailable, omit the field and record the gap — an absent `yield:` is correct; a
plausible guess is a ruined dinner.

This bites hardest on scans and non-English sources, where `1½` and `1¾` look alike. Flag
anything you are not confident you read correctly rather than committing it silently.

## Reading the input

| Format | How to read it |
|---|---|
| `.txt`, `.md` | Read directly. |
| `.html` | Strip navigation, headers, sidebars, and comment threads first. Almost certainly a published source — `recipe-extract` applies. |
| `.docx`, Google Docs export | Convert to text first: `pandoc -t plain <file>`, or an equivalent extractor. |
| PDF with a digital text layer | Extract the text (`pdftotext -layout` preserves column structure, which matters for ingredient tables). |
| PDF or image scan of handwriting | Read the pages as **images**, not text. See below. |

**Scans and handwriting.** Do not attempt these with a text extractor — a `pdftotext` run over
a scan returns empty or garbage, and garbage silently becomes invented content. Rasterize the
pages (`pdftoppm -r 200 -png`) and read the images directly. If you cannot see images, stop and
report the file as failed rather than guessing; the orchestrator routes scans to a
vision-capable agent for this reason.

## Language

Input may be mixed-language — expect English, French, and Vietnamese, usually at the level of
ingredient names and short imperative instructions rather than continuous prose.

An unfamiliar word is far more likely to be a real word in another language than an OCR error
or a typo. **Do not "correct" it.** Translate it if you are confident (`beurre` → butter,
`đường` → sugar); flag it if you are not. Preserve a dish name in its original language in the
title where that is what the dish is called.

**Read the matching language reference before parsing**, when there is one:

- `references/vietnamese.md` — measurements are abbreviated aggressively (`mcf`, `mc`, `cf`)
  and diacritics are frequently dropped, which reads as OCR noise but is not.
- `references/french.md` — the France/Québec vocabulary split, the `thermostat` oven scale,
  and Canadian cream sold by fat percentage.

**Establish the source language before expanding any abbreviation.** The shorthands collide:
`tc` is a Vietnamese tablespoon, `ct` a French teaspoon, and `cc`/`cf` sit close enough to
misfire. Getting a spoon abbreviation wrong is a 3× quantity error, so identify the language
first and use only that reference.

Both files are incomplete by design — escalate what they do not cover rather than guessing.

**Output is English by default.** If and only if the user asked for multi-language output, put
the English version first, then a horizontal rule (`---`), then each additional language.

## Flagging uncertainty

The reviewer should be able to find every soft spot without re-reading the source. Mark each
one inline, at the point it occurs, with an HTML comment:

```markdown
| Flour | 250 g |
| Sugar | 1½ cups |<!-- REVIEW: could be 1¾ — handwriting ambiguous -->
```

Flag, at minimum:

- Illegible or ambiguous handwriting, quoting your best reading and the alternative.
- Amounts you converted rather than read (volume → weight, °F ↔ °C), naming the conversion.
- Steps whose order or object is unclear in the source.
- A missing house-format field, so the gap is visible: `<!-- REVIEW: source gives no yield -->`.
- Uncertainty about whether the source is the user's own or published, since that changes
  whether `recipe-extract`'s stripping rules should have applied.

Also close each file with a `## Review notes` section summarizing what needs checking and
anything you dropped. Both the section and the inline comments are stripped at promotion; they
must never reach `docs/`.

## Escalating an unrecognized parse

The language references are **known to be incomplete**. When you hit something that looks like
a *convention* rather than a one-off — an abbreviation, unit, or shorthand that recurs, or that
clearly means something specific you cannot confirm — do not settle it yourself, and do not
quietly pick the likeliest reading.

Instead:

1. Leave the source text **unexpanded** in the output, with a `<!-- REVIEW: … -->` giving your
   best hypothesis and why you are unsure.
2. Add a **`### Unrecognized shorthand`** subsection under `## Review notes`, listing each one
   as: the literal text, where it appeared, your hypothesis, and your confidence.
3. Report it prominently in your final message. The orchestrator collects these across all
   files and puts them to the user.

The user decides. If they confirm a reading, it gets added to the relevant reference file and
every future parse benefits; if they do not, nothing was silently wrong in the meantime. One
question asked once is cheap — a wrong expansion repeated across a batch is not.

Escalate rather than guess when: an abbreviation is not in the reference; a unit is ambiguous
between two real readings; a number could be read two ways; you cannot tell whether a line is
an ingredient or an instruction. Do **not** escalate ordinary illegibility or a missing
field — those are just `REVIEW` flags.

## Writing the output

- One file per recipe, named `kebab-case.md` after the dish, written to
  `input_recipes/markdown/`. A single source may contain several recipes — emit one file each.
  If a name would collide with a file already there, suffix it (`-2`) and note it.
- **Tags** are faceted — every tag is `facet/value` (`cuisine/vietnamese`, `technique/frying`).
  Draw **only** from the vocabulary passed into your prompt: it is enforced by `tags_allowed`,
  so an invented value fails the build rather than quietly appearing. If a recipe needs a value
  that is not on the list, use nothing and flag it in Review notes — coining is the user's call
  via the `recipe-tag` skill. At least one tag; no facet is individually required.
- **Never write a `course/` tag.** It is derived from the recipe's directory at build time, and
  you do not choose the directory anyway.
- **Never write an `effort/` tag.** Only the user rates difficulty, and it cannot be inferred
  from a recipe file. Treat this like inventing culinary content: do not guess.
- **`diet/` only when the recipe qualifies as written** — no assumed substitutions. A wrong
  dietary tag can hurt someone, and a missing one means unclassified, not "does not qualify".
- **Category: do not choose one.** Picking a directory requires seeing the whole site, which
  you cannot. Category is decided at promotion.
- **Do not convert units.** Record amounts as the source wrote them. A weight may carry a
  metric equivalent alongside it (`3 lb (1.36 kg)`); a volume may not be silently rewritten as
  millilitres, and a packed or minced volume may never become a weight — that needs a density
  the source did not give. `AGENTS.md` → "House style for amounts" is authoritative.
- **Attribution** goes in the **first Notes bullet**, hyperlinked for a web source
  (`Adapted from [Allrecipes, "…"](https://…).`) and **bolded** when it cannot be linked
  (`Adapted from **Joy of Cooking**, 1997 edition.`). There is no `source:` frontmatter key.
  Recipes are family or in-house by default: if the source is the user's own or a family card,
  write no attribution at all — do not add a note saying it is a family recipe.
- Write LF line endings.

## Where you stop

Producing files in `input_recipes/markdown/` **is the end of the task.**

Never move, copy, or promote anything into `docs/<category>/`. Never edit an existing recipe.
Never move the source file yourself — the orchestrator does that once you report success.
Files you write are proposals; a human reads them before any of it is real.

Report back: the recipes you wrote, what you flagged, and anything you could not read.
