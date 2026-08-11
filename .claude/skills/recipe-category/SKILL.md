---
name: recipe-category
description: Add or remove a recipe category, keeping the directory, its index.md, the home-page card, and the rules text in AGENTS.md consistent. Use when the user asks to add, remove, or rename a category — never as a convenience while filing a recipe.
---

# Adding or removing a category

A category is four things that must agree: a directory under `docs/`, its `index.md`, a card in
`docs/index.md`, and the canonical list in `AGENTS.md`. Change one and the site is quietly
wrong — the nav and the home page disagree, and **`mkdocs build --strict` passes anyway**,
because nothing here is a broken link. That silence is why this is a skill.

## Before you touch anything

**Categories answer *when do you eat this?*** — one per recipe, no overlap. They are not for
technique, cuisine, ingredient, or dietary fit; those are tags, which cut across categories and
can be worn several at a time.

So the bar for a new category is high, and the honest answer is usually a tag:

- A technique is never a category. `baking` was a category here and was removed for exactly
  this reason — plenty of things are baked without being a course. It is the worked example;
  do not reintroduce it.
- A cuisine is never a category. That is what `chinese`, `korean`, `vietnamese` are for.
- If a recipe could plausibly sit in the proposed category *and* an existing one, the proposal
  is a tag.

**Say this to the user before creating anything**, with the tag alternative named. If they
confirm, proceed — it is their book.

Renaming is the expensive one: the published URL is `<category>/<recipe>/`, there is no
redirect plugin, and every recipe in the directory changes address. Say so before starting.

## Adding

1. `docs/<category>/index.md` — frontmatter with `title`, an H1 matching it, and one line
   saying what belongs there and, where it is not obvious, what does not. Match the voice of the
   existing category pages; they are short on purpose.
2. A card in `docs/index.md`, in the existing alphabetical order, with a Material icon that
   already exists in the icon set.
3. The canonical list in `AGENTS.md` → "Layout", and the same list in
   `recipe-promote/SKILL.md` step 3.
4. `handoff.md`, if it still carries a category list.

The directory needs no `.gitkeep` — its `index.md` keeps it.

## Removing

Same four places, in reverse, plus one question first:

1. **Check the directory is empty of recipes** — `ls docs/<category>/`. If it holds anything
   besides `index.md`, stop and ask where those recipes should go. Never relocate someone's
   recipes as a side effect of a category change; moving a recipe changes its URL.
2. Delete the directory.
3. Remove the card from `docs/index.md`.
4. Update the canonical list in `AGENTS.md` and `recipe-promote/SKILL.md`, and `handoff.md`.

**Record a removal as deliberate.** Write a line in `AGENTS.md` saying the category was removed
and why, in the user's own reasoning. Without it the next agent reads the gap as an oversight
and helpfully recreates it. A removed category is a decision, and decisions need to survive in
the rules rather than only in a commit message.

## Afterwards

Run `.venv/bin/mkdocs build --strict`, then confirm by reading the built output, since the
build cannot catch this class of mistake:

```bash
python3 -c "
import re
h=open('site/index.html',encoding='utf-8').read()
print(sorted(set(re.findall(r'<a href=\"([a-z-]+)/\"', h))))
"
ls docs/
```

The two lists must match, minus `tags`. Then report what changed and **ask before committing**.
