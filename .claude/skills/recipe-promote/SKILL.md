---
name: recipe-promote
description: Promote a reviewed recipe proposal from input_recipes/markdown/ into docs/<category>/ — strip review markers, choose a category, verify the strict build, and regenerate the PDF. Use only when the user names a specific staged file and asks for it to be published or promoted.
---

# Promoting a staged recipe into the book

Move one reviewed proposal from `input_recipes/markdown/` into `docs/<category>/`.

## Before you start

**The user must have asked for this specific file.** Promotion is never a follow-on to
parsing, never a convenience because output looked correct, never a batch operation you infer
from "these all look good." If you are acting on your own judgment rather than a named
request, stop — the file stays where it is.

If the user names several files, confirm the list back before touching any of them.

## Steps

1. **Read the file, including its `## Review notes`.** If it flags something unresolved — an
   ambiguous amount, a missing yield, uncertainty about whose recipe it is — raise it now.
   The user may have promoted without reading the markers.

2. **Strip every review artifact.** All `<!-- REVIEW: … -->` comments and the entire
   `## Review notes` section. None of it may reach `docs/`. Grep the result to be sure:
   `grep -n 'REVIEW\|Review notes' <file>` should return nothing.

3. **Choose a category** — `breakfast`, `desserts`, `drinks`, `mains`, `prep`,
   `sides`. The question is *when do you eat this?*, not what it is made of or how. Almond
   cookies are `desserts/` tagged `baking`; there is no `baking/`. A component rather than a dish
   (sushi rice, a spice mix) is `prep/`. Ask if genuinely torn; prefer a new tag over a new
   category.

4. **Check the tags against the vocabulary** in `AGENTS.md` → "Tag vocabulary", which is the
   authority — a parser working without repo context routinely coins a synonym of a tag the
   book already has. Tags are faceted (`cuisine/korean`, not `korean`) and enforced by
   `tags_allowed`, so a wrong value fails the build. Two never come from you: `course/` is
   derived from the directory by a hook, and `effort/` is the user's alone — leave it absent
   rather than guessing. New values go through `recipe-tag`, not straight into the file.
   To see what is actually in use:

   ```bash
   awk '/^tags:/{t=1;next} /^[a-zA-Z_-]+:/{t=0} t&&/^ *- /{sub(/^ *- /,"");print}' \
     $(find docs -name '*.md') | sort -u
   ```

   Replace a coined tag with a standard one wherever a reasonable one fits. Flag any tag that
   is genuinely new to the user rather than quietly introducing it.

5. **Verify the frontmatter and body against `AGENTS.md`** — `title` and `tags` present, H1
   matching `title`, the italic yield/time line, ingredient table, numbered steps. Fix
   formatting drift; do not add culinary content that is missing.

6. **Move it**: `mv input_recipes/markdown/<name>.md docs/<category>/<name>.md`. Move, not
   copy — a lingering staged duplicate will be re-promoted later.

7. **Build**: `.venv/bin/mkdocs build --strict`. It must be clean before you go on.

8. **Regenerate the PDF**: `.venv/bin/python scripts/build_pdfs.py --only <name>`, and include
   the result. Skipping this leaves the committed `recipe_pdfs/` copy stale, since CI does not
   refresh it.

9. **Report and stop.** Summarize the category and tags you chose, anything you stripped, and
   the build result. **Do not commit** — ask, as always, and give a real account of the files
   touched.

## Notes

- The published URL is `<category>/<name>/`. Renaming later breaks it — there is no redirect
  plugin — so settle the filename now.
- If a file with that name already exists in the target category, stop and ask. Overwriting a
  recipe the user has cooked and tuned is exactly what the "ask before editing" rule protects.
- Leave the corresponding source in `processed/` where it is. It is the audit trail for what
  the recipe was derived from.
