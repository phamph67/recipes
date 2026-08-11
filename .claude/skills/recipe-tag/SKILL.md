---
name: recipe-tag
description: Add, rename, or retire a value in the faceted tag vocabulary, keeping AGENTS.md and the tags_allowed list in mkdocs.yml in step. Use when the user asks for a new tag, when a recipe needs a value the vocabulary lacks, or when tidying near-duplicate tags.
---

# Changing the tag vocabulary

The vocabulary lives in two places that must agree: the prose list in `AGENTS.md` →
"Tag vocabulary", and `tags_allowed` in `mkdocs.yml`. The allow list is what actually enforces
it — a tag outside it fails `mkdocs build --strict` — so a value added to only one of the two
either breaks the build or silently escapes enforcement.

**Only the user adds vocabulary.** A parser or promoter that meets a value it needs must flag
it, not coin it. If you are here because a recipe wanted a tag that does not exist, the answer
is to ask, not to add.

## Before adding anything

Adding a near-synonym is the failure mode. It makes browse pages worse: two half-full pages
where there should be one useful one, and no way to tell which a recipe used.

1. **Read the existing facet** in `AGENTS.md`. Does a listed value already cover this?
   `bbq` is `technique/grilling`; `asian` is a specific `cuisine/`; `quick` is not a tag at all.
2. **Check the facet is right.** `form/` is what kind of thing it is, `main/` is what you would
   shop for, `technique/` is how it is cooked. A value in the wrong facet is worse than a
   missing one.
3. **Say what it excludes.** A good tag divides the book. If a proposed value would be true of
   nearly everything, or of exactly one recipe forever, say so before adding it.

Two facets are closed and are not extended here:

- **`course/`** is derived from the directory. Its values *are* the category directories, so
  changing them means adding or removing a category — that is `recipe-category`, not this skill.
- **`effort/`** is `easy` / `medium` / `hard` and is assigned by the user alone. Never add
  values, and never apply one to a recipe.

## Adding a value

1. Add it to the right facet in `AGENTS.md`, keeping the list alphabetical.
2. Add it to `tags_allowed` in `mkdocs.yml`, in the same facet block, alphabetically.
3. Run `.venv/bin/mkdocs build --strict`. Clean before you go on.
4. Report it, and **ask before committing**.

## Renaming a value

A rename changes a published browse-page URL, and there is no redirect plugin configured.
Say so before starting.

1. Update `AGENTS.md` and `tags_allowed` together.
2. Rewrite the tag in every recipe that carries it. Find them first:

   ```bash
   grep -rln 'facet/oldvalue' docs --include='*.md'
   ```

3. **This edits recipes the user has already tuned**, which normally needs a nod — a rename
   they explicitly asked for is that nod, but list the files you touched in your report.
4. Build strict, then ask before committing.

## Retiring a value

Remove it from both places *after* removing it from every recipe, in that order — dropping it
from `tags_allowed` first breaks the build for everyone until the recipes catch up.

## Checking the vocabulary against reality

The two lists drift silently, so verify rather than assume:

```bash
# every tag actually in use
awk '/^tags:/{t=1;next} /^[a-zA-Z_-]+:/{t=0} t&&/^ *- /{sub(/^ *- /,"");print}' \
  $(find docs -name '*.md') | sort -u

# every tag the build will accept
grep -A400 'tags_allowed:' mkdocs.yml | grep -oE '^\s+- \S+' | sed 's/^ *- //' | sort -u
```

Everything in the first list must appear in the second; the reverse is fine, since a vocabulary
value with no recipes yet is a plan, not an error.
