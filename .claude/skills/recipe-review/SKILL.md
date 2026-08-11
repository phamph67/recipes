---
name: recipe-review
description: Turn the staged proposals in input_recipes/markdown/ into a numbered question sheet the user can answer away from their desk, then apply the answers — writing confirmed shorthand into the language references and correcting the affected files. Use after an ingest run, or whenever the user asks what needs checking, what is blocking promotion, or to review the staged recipes.
---

# Reviewing staged proposals

An ingest run ends in a pile of proposals nobody has read. This skill turns that pile into a
short list of questions, collects the answers, and feeds them back into the files and the
language references.

**This is the step where the pipeline pays off or doesn't.** Parsers are deliberately built to
flag rather than guess, which means the flags are the product. Left unread they are just a
record of doubt.

## What this skill is not

It does **not** promote anything. Promotion is `recipe-promote`, per file, by name, and only
when the user asks for that file. Answering a question about a recipe is not asking for it to
be published.

## Step 1 — harvest

Read every `.md` in `input_recipes/markdown/`. Unlike `recipe-ingest`, you *are* meant to read
recipe content here — the contamination risk that justified isolation during parsing is gone,
because nothing is being written from a source any more.

Collect from each file:

- every `<!-- REVIEW: … -->` marker, with the ingredient or step it sits on
- the `## Review notes` section
- any `### Unrecognized shorthand` entries, verbatim
- structural gaps: no procedure, no yield, no oven temperature

## Step 2 — group by kind of doubt, not by file

This is the whole trick. A per-file walkthrough is unanswerable — the user is asked to
context-switch thirty times. The same questions grouped by *kind* can be answered in one sitting,
and identical doubts across files collapse into one question:

| Group | What it holds |
|---|---|
| **Shorthand** | Unexpanded abbreviations. Highest leverage: one answer fixes every file using it. |
| **Missing units** | The number is legible, the unit was never written. Pure recall for the user. |
| **Two readings** | Both plausible, materially different — `dầm` vs `dầu`, baking powder vs yeast. |
| **Identity** | What dish is this, what meat, which flour. |
| **Duplicates** | The same dish parsed several times with different ratios. Usually deletions. |
| **Source damage** | Cropped scans, illegible pencil. Not a question — a re-scan request. |

Order the groups by leverage: shorthand first, source damage last. Within a group, put the
items that change a quantity above the ones that change a name.

**Number every item across the whole sheet**, so the user can answer `3 = tbsp, 12 = yeast`.

## Step 3 — deliver it where they will read it

Ask how they want it if it is not obvious. A short run can go straight into the conversation.
A long one is better published as an artifact — the user is often away from the machine when
they have the answers, and a link opens on a phone where a file path does not.

**Never publish the sheet into the repository.** It quotes recipe content, `input_recipes/` is
gitignored precisely because that content is personal or third-party, and this repo is public.
Committing the review sheet leaks exactly what the gitignore protects.

State plainly what is *not* answerable — recipes with no procedure are not blocked on a
question, they are blocked on the user writing down a method they know by heart.

## Step 4 — apply the answers

Answers are worth little until they are written down in both places:

1. **The language reference** — `.claude/skills/recipe-parse/references/<language>.md`. Add the
   confirmed reading, marked as user-confirmed, with the form it appeared in. This is the
   mechanism that stops the same question being asked twice; skipping it wastes the answer.
2. **Every affected staged file** — expand the shorthand, fill the unit, resolve the reading,
   and remove the `<!-- REVIEW: … -->` marker that flagged it. A marker left behind will be
   stripped at promotion and the doubt will vanish silently.

Where an answer resolves a *duplicate*, delete the versions the user rejected rather than
leaving them to be re-reviewed next time.

**Anything the user did not answer stays flagged and unexpanded.** Silence is not confirmation.
Ask once, never guess twice.

## Step 5 — report

Say what was applied, what was written into which reference, what remains open, and which files
are now clean enough to be worth promoting. Do not promote them.
