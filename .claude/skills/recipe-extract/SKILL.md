---
name: recipe-extract
description: Extract a recipe from a published or third-party source into this book's house format, keeping only ingredients, quantities, procedure, and practical notes while dropping the surrounding narrative. Use whenever the user pastes, links, or points at a recipe that did not originate with them — a website, blog, cookbook scan, magazine clipping, or video description.
---

# Extracting a recipe from a published source

This recipe book is **practical, not literary**. When a recipe comes from somewhere other
than the user's own kitchen, take the cooking and leave the storytelling.

There are two reasons, and both point the same way:

1. **The user wants it that way.** The book is a working reference. Nobody standing at a
   stove wants three paragraphs about a trip to Tuscany above the ingredient list.
2. **Copyright.** Ingredient lists and procedural steps are uncopyrightable statements of
   fact and process. The *expressive prose* around them — headnotes, personal essays,
   distinctive descriptive writing, photographs — is protected. Reproducing the former is
   fine; copying the latter into this repo is not.

## When this applies

Apply the stripping rules when the source is published or otherwise not the user's own.
Signals, in rough order of reliability:

- The user says so ("from Serious Eats", "this is off a blog", "from my Ottolenghi book").
- Input is a saved web page, a cookbook or magazine scan, or a video description.
- The text carries the fingerprints of published food writing: a first-person headnote before
  the ingredients, SEO throat-clearing ("you're going to love this…"), section headers like
  *Why this recipe works*, *Equipment I recommend*, *Storage tips*, *FAQ*, a jump-to-recipe
  link, star ratings, comment threads, affiliate or product plugs, or a byline and date.

**When it is the user's own or family recipe, do not apply this** — their asides are the
point. Keep them. See the ingredient-origin note style in `docs/prep/sushi-rice.md`.

If you genuinely cannot tell whose recipe it is, ask. Do not guess.

## Keep

- **Ingredients and quantities**, exactly as given. Convert to metric weights per the house
  format, but never change what the recipe actually calls for.
- **Procedure** — every step, in order, including temperatures, times, and pan sizes.
- **Practical notes** that change the outcome: substitutions, make-ahead and storage advice,
  doneness cues, what a range of amount or time actually does, common failure modes.
- **Why-this-ingredient background**, if it is genuinely informative (a cultivar, a fat's
  smoke point, why bread flour here) — but rewritten in your own words and moved into Notes.

## Drop

- Headnotes, personal anecdotes, travel and family stories belonging to the author.
- Marketing prose, SEO padding, and anything addressed to a blog audience rather than a cook.
- Equipment plugs, affiliate mentions, brand endorsements.
- Nutrition tables, ratings, comment excerpts, social calls to action.
- Photographs and captions.

## How to write the output

Reproduce facts, not phrasing. Ingredient lines and step instructions are functional and stay
close to the original by necessity — "Bake 15–17 minutes at 325 °F" has few other phrasings.
Anything beyond that, write fresh in the book's plain register. If a sentence is memorable
because of *how* it is written, that is the signal to rewrite or cut it.

Then follow `AGENTS.md` for everything else: frontmatter with `title` and `tags`, the H1, the
italic yield/time line, ingredient tables per component, numbered steps, `**Notes**` last.

Attribution goes in the **first Notes bullet** — before technique or substitution notes — not
in frontmatter. There is no `source:` key in this book. Two forms:

- **Hyperlinked** for a web source:
  `Adapted from [Serious Eats, "Sous Vide Steak"](https://…).`
- **Bolded** when it cannot be linked — book, clipping, scan, person:
  `Adapted from **Joy of Cooking**, 1997 edition.`

Recipes in this book are **family or in-house by default**, so the presence of that bullet is
what marks a recipe as someone else's. Never write a note saying a recipe *is* family or
in-house — the absence of an attribution line already says it.

## The rule that overrides everything

**Never invent culinary content.** If the source omits an oven temperature, a quantity, or a
yield, leave it out and tell the user what is missing. Do not fill the gap with a plausible
number. This matters most when the input is a handwritten scan or a non-English document
where a misread `1½` and `1¾` look alike — flag anything you are unsure you read correctly
rather than committing it silently to the book.
