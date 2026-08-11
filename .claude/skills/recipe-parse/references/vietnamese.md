# Vietnamese recipe shorthand

Reference for parsing Vietnamese-language sources. Vietnamese home recipes — especially
handwritten cards and forum posts — compress measurements heavily and often drop diacritics
entirely, which makes them look like OCR noise when they are not.

**Confidence is marked.** Rows marked ⚠ are plausible readings, not established conventions:
treat them as a hypothesis to flag with `<!-- REVIEW: … -->`, never as a silent expansion. A
wrong expansion of a spoon abbreviation changes a quantity by 3×, which is exactly the kind of
error this book's fidelity rule exists to prevent.

## Before anything else: how the text may be mangled

- **Missing diacritics are normal, not corruption.** `muong ca phe`, `nuoc mam`, `duong`,
  `hanh tim` are ordinary typed Vietnamese. Do not "correct" them and do not treat them as
  illegible. Restore the diacritics mentally, translate, and move on.
- **Mojibake** (`Ä'Æ°á»ng` for `đường`) means a UTF-8 file was read as Latin-1. If a file is
  mostly mojibake, re-read it with the correct encoding rather than guessing at words.
- **Telex/VNI artifacts** — `dduongf`, `nuowsc`, `ca2 phe6` — appear when someone typed with
  an input method that did not compose. Decode if the pattern is clear; flag if it is not.
- **No diacritics creates real ambiguity.** `ca phe` is both "coffee" and the "coffee spoon"
  of `muỗng cà phê`. `1 mcf duong` is a teaspoon of sugar; `ca phe` in an ingredient table may
  be actual coffee. Use position and context, and flag when unsure.

## Spoon measures

The two that matter most, since nearly every recipe uses them.

| Written | Expansion | → | Confidence |
|---|---|---|---|
| `muỗng cà phê`, `thìa cà phê` | coffee spoon | **tsp** | Established |
| `mcf`, `m.cf`, `mcp` | ↑ abbreviated | **tsp** | Established |
| `cf`, `c.phê`, `c.phe` | ↑ further abbreviated | **tsp** | Established (user-confirmed) |
| `tcf`, `t.cf` | `thìa cà phê`, northern phrasing | **tsp** | Established (user-confirmed) |
| `muỗng canh`, `thìa canh` | soup spoon | **tbsp** | Established |
| `mc`, `m canh`, `m.canh` | ↑ abbreviated | **tbsp** | Established (user-confirmed) |
| `tc`, `t.canh` | `thìa canh`, northern | **tbsp** | Established (user-confirmed) |
| `muỗng súp`, `ms` | soup spoon, same thing | **tbsp** | Established (user-confirmed) |
| `muỗng lớn` / `muỗng nhỏ` | big spoon / small spoon | **tbsp** / **tsp** | Confident |

**Capitalization carries no meaning.** `M` and `m` are not big and small spoon. Handwriting
makes case unreliable in the first place, so resolve the unit from the word or the recognized
abbreviation only, and flag it if neither is present.

`thìa` (northern) and `muỗng` (southern) are the same utensil. A recipe using `thìa`
throughout is likely northern, which is weak evidence for other northern vocabulary.

**Modifiers:** `vun` = heaped, `gạt` = levelled, `đầy` = full. `1 mcf vun` is a heaped
teaspoon — carry it into Notes rather than dropping it, since it matters for leaveners and
salt.

## Volume and container measures

These are the dangerous ones: they are real, widely used, and have no fixed size.

| Written | Meaning | Notes |
|---|---|---|
| `chén` (southern), `bát` (northern) | small rice bowl | Commonly ~200–250 ml, but genuinely varies. Do **not** convert to grams. |
| `ly`, `cốc` | glass / cup | Varies. `ly` is southern, `cốc` northern. |
| `lon sữa bò` | condensed-milk can | A real and very common unit in home recipes, ~380 ml. Often shortened to `lon`. |
| `lon` | can | Ambiguous alone — condensed-milk can, beer can, or rice-cooker cup. Flag it. |
| `chai` | bottle | Size unstated. |
| `gói` | packet | e.g. `1 gói men` = 1 packet yeast. |
| `nửa`, `phân nửa`, `1/2` | half | |

**Rule for all of these: keep the original unit and flag it.** `1 chén gạo` becomes
`| Rice | 1 chén (~200 ml) |` with `<!-- REVIEW: chén is a rice bowl, size varies -->`. Do not
silently convert a bowl to 250 g. This is the single most likely place to invent content.

## Counting words (classifiers)

Vietnamese counts most things with a classifier. These are units, not ingredients:

| Word | Counts | Example |
|---|---|---|
| `tép` | clove | `3 tép tỏi` = 3 garlic cloves |
| `củ` | bulb, tuber, root | `1 củ hành tím` = 1 shallot |
| `nhánh` | sprig, knob, stalk | `1 nhánh gừng` = a knob of ginger |
| `cây` | stalk | `2 cây sả` = 2 lemongrass stalks |
| `trái`, `quả` | fruit, whole item | southern / northern |
| `lát` | slice |  |
| `miếng` | piece |  |
| `bó` | bunch | `1 bó rau muống` |
| `nắm` | handful |  |
| `con` | whole animal | `1 con cá` = 1 fish |

## Vague amounts

Common, and they must stay vague — the temptation to pin a number is the failure mode.

| Written | Meaning |
|---|---|
| `chút`, `chút xíu`, `tí`, `xíu` | a little, a pinch |
| `vừa ăn` | to taste — `nêm vừa ăn` = "season to taste" |
| `vừa đủ` | just enough |
| `tùy khẩu vị` | according to taste |
| `xâm xấp` | just barely covering (of liquid) |
| `sền sệt` | thickened, syrupy |

Render these as words, never as numbers. "Salt, to taste" is correct; "2 g salt" is invented.

## Frequently abbreviated ingredients

Ingredient abbreviation is not standardized the way spoon abbreviation is, and no ingredient
shorthand is confirmed for this book yet. ⚠ **Never expand a single- or double-letter
ingredient abbreviation. Flag it and escalate** (see below) so it can be confirmed once and
added here.

Full names worth recognizing:

- **Sauces/seasoning:** `nước mắm` fish sauce · `nước tương`/`xì dầu` soy sauce ·
  `hạt nêm` seasoning granules · `bột ngọt`/`mì chính` MSG · `đường` sugar · `muối` salt ·
  `tiêu` pepper · `dầu ăn` cooking oil · `dầu hào` oyster sauce · `mắm tôm` shrimp paste
- **Starches:** `bột mì` wheat flour · `bột gạo` rice flour · `bột năng` tapioca starch ·
  `bột bắp` cornstarch · `bột nở` baking powder · `men` yeast
- **Aromatics:** `hành lá` scallion · `hành tím` shallot · `hành tây` onion · `tỏi` garlic ·
  `ớt` chili · `sả` lemongrass · `gừng` ginger · `riềng` galangal · `nghệ` turmeric
- **Herbs:** `ngò`/`rau mùi` cilantro · `ngò gai` culantro · `ngò om`/`rau ngổ` rice paddy
  herb · `húng quế` Thai basil · `tía tô` perilla · `lá dứa` pandan
- **Coconut/dairy:** `nước dừa` coconut water · `nước cốt dừa` coconut milk (**not**
  interchangeable) · `sữa đặc` condensed milk · `sữa tươi` fresh milk
- **Pork cuts:** `ba chỉ`/`ba rọi` pork belly · `nạc` lean · `nạc dăm` shoulder ·
  `sườn` ribs · `xương` bones · `giò` trotter

## Technique verbs

Useful because they carry cooking method the house format should preserve:

`ướp` marinate · `xào` stir-fry · `chiên`/`rán` deep- or pan-fry · `kho` braise in caramel
sauce · `rim` simmer down · `om` stew · `luộc` boil · `hấp` steam · `nướng` grill or roast ·
`hầm`/`ninh` simmer long · `trộn` toss · `đảo đều` stir evenly · `phi` fry aromatics until
fragrant · `nêm nếm` season · `để nguội` let cool · `sôi` boil (state)

Heat: `lửa nhỏ` low · `lửa vừa` medium · `lửa lớn`/`lửa to` high · `lửa liu riu` bare simmer.

## Dish-name titles

Keep the Vietnamese dish name as the `title` when that is what the dish is called — `Bò Kho`,
`Bánh Xèo`, `Thịt Kho Trứng` — rather than translating to a description. Add an English gloss
in Notes if the name is not self-explanatory. Tag `vietnamese`.

## What to do when unsure

Flag, do not resolve — and if the unknown is a shorthand or unit rather than a one-off
smudge, **escalate it** so this file can grow. See "Escalating an unrecognized parse" in
`SKILL.md`. This reference is expected to be incomplete; every real recipe is a chance to
confirm one more abbreviation with the user rather than guessing at it forever.

Quote the source text verbatim in the review comment so the reviewer can check it without
reopening the original:

```markdown
| Sugar | 2 tbsp |<!-- REVIEW: source reads "2 mc duong" — mc read as muỗng canh (tbsp); could be a personal shorthand -->
| Rice | 1 chén |<!-- REVIEW: chén = rice bowl, ~200–250 ml, size varies; not converted -->
```
