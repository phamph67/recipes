# French recipe shorthand

Reference for parsing French-language sources. Less compressed than Vietnamese — French
recipes generally spell measurements out — but there are three specific traps: the
France/Québec vocabulary split, the `thermostat` oven scale, and Canadian cream sold by fat
percentage.

Same rule as everywhere: ⚠ rows are hypotheses to flag, not silent expansions. Anything not
listed here that looks like a convention should be **escalated** (see `SKILL.md`).

## Spoon measures

| Written | Expansion | → |
|---|---|---|
| `c. à s.`, `c. à soupe`, `cuil. à soupe`, `cs`, `CS` | cuillère à soupe | **tbsp** |
| `c. à c.`, `c. à café`, `cuil. à café`, `cc` | cuillère à café | **tsp** |
| `c. à t.`, `c. à thé`, `cuil. à thé`, `ct` | cuillère à thé — **Québec/Canada** | **tsp** |
| `c. à d.`, `cuillerée à dessert` | dessert spoon | ⚠ ~2 tsp; flag, uncommon |

`cuillère à café` (France) and `cuillère à thé` (Québec) are the same measure. A recipe using
`c. à thé` is Canadian, which is useful evidence for reading the rest of it.

**Note the collision with Vietnamese.** `cc` and `ct` here are French spoon measures; `cf` and
`tc` in a Vietnamese source are something else entirely. Establish the source language before
expanding any abbreviation.

## Volume and weight

- **France** is overwhelmingly metric by weight — `g`, `kg`, `ml`, `cl`, `l`. Note **`cl`**
  (centilitres): `20 cl` = 200 ml. It is standard in France and easy to misread as `ml`.
- **Québec/Canada** uses cups and spoons like the US: `tasse` = **250 ml** exactly (not the
  US 236 ml). `1/2 tasse`, `1 1/4 tasse`. Imperial `lb` and `oz` also appear.
- `pincée` pinch · `noix de beurre` knob of butter · `filet` a drizzle (`un filet d'huile`) ·
  `verre` glass ⚠ (unfixed size — flag, do not convert) · `bol` bowl ⚠ (same).
- `sachet` packet — `1 sachet de levure` is a real unit but ⚠ its gram weight differs between
  products and countries. Keep as "1 sachet" and flag rather than converting.
- `QS`, `q.s.` = *quantité suffisante*, "as much as needed".

## Oven temperature: the thermostat scale

French recipes often give the oven as `th. 6`, `thermostat 6`, or `Th.6` rather than degrees.
The scale is **thermostat × 30 = °C**:

| th. | °C | °F |
|---|---|---|
| 4 | 120 | 250 |
| 5 | 150 | 300 |
| 6 | 180 | 350 |
| 7 | 210 | 410 |
| 8 | 240 | 465 |

Convert to the house format's both-units form (`180 °C / 350 °F`) and flag the conversion:
`<!-- REVIEW: source gave "th. 6"; converted via thermostat × 30 -->`.

Also: `four préchauffé` preheated oven · `chaleur tournante` fan/convection ·
`à sec` dry pan · `au bain-marie` in a water bath.

## Vague amounts

Keep these as words, never as numbers:

`au goût`, `selon le goût` to taste · `à volonté` as much as you like · `un peu` a little ·
`quelques` a few · `à hauteur` enough to cover · `assaisonner` season · `rectifier
l'assaisonnement` adjust seasoning.

## France vs. Québec vocabulary

The split that actually changes what you buy:

| Québec | France | English |
|---|---|---|
| `bleuets` | `myrtilles` | blueberries |
| `canneberges` | `airelles` ⚠ | cranberries (not strictly the same berry) |
| `gruau` | `flocons d'avoine` | oatmeal / rolled oats |
| `blé d'Inde` | `maïs` | corn |
| `patates` | `pommes de terre` | potatoes |
| `fèves` | `haricots` | beans |
| `crème sure` | `crème aigre` | sour cream |
| `cassonade` | `cassonade` / `sucre roux` | brown sugar |
| `sirop d'érable` | — | maple syrup |
| `beurre d'arachide` | `beurre de cacahuète` | peanut butter |
| `pacanes` | `noix de pécan` | pecans |

**Canadian cream is sold by fat percentage**, and recipes name it that way — this is the
single most common Canadian-French parsing trap:

- `crème 35 %`, `crème à fouetter` → heavy / whipping cream
- `crème 15 %`, `crème à café` → light or table cream
- `crème 10 %` → half-and-half
- `lait 2 %`, `lait 3,25 %` → milk by fat content

Carry the percentage through to the ingredient table rather than flattening it to "cream" —
substituting 15 % for 35 % breaks anything that has to whip or hold.

**Decimal commas.** French writes `3,25 %` and `1,5 kg` with a comma. Do not read `1,5` as
1500. Convert to a decimal point in the output.

## Common ingredients

- **Baking:** `farine` flour (`farine T55` ⚠ French flour grade — keep the code, flag it) ·
  `sucre` sugar · `sucre glace` icing sugar · `sucre vanillé` vanilla sugar ·
  `levure chimique` **baking powder** · `levure de boulanger` **yeast** (not
  interchangeable — a frequent mistranslation) · `bicarbonate de soude` baking soda ·
  `oeufs` eggs · `beurre doux` unsalted butter · `beurre demi-sel` lightly salted butter
- **Dairy:** `crème fraîche` · `crème épaisse` thick cream · `crème liquide` pouring cream ·
  `lait entier` whole milk · `fromage blanc`
- **Aromatics:** `ail` garlic (`gousse d'ail` clove) · `oignon` · `échalote` shallot ·
  `persil` parsley · `thym` · `laurier` bay · `ciboulette` chives · `estragon` tarragon ·
  `bouquet garni`
- **Pantry:** `huile` oil · `huile d'olive` · `vinaigre` · `moutarde` · `sel` ·
  `poivre` · `fleur de sel` · `bouillon` stock

## Counting words

`gousse` clove · `brin` sprig · `botte` bunch · `feuille` leaf · `tranche` slice ·
`morceau` piece · `poignée` handful · `zeste` zest · `jus` juice.

## Technique verbs

`faire revenir` sauté until coloured · `saisir` sear · `mijoter` simmer · `réduire` reduce ·
`blanchir` blanch (or: beat eggs and sugar pale ⚠ — context decides) · `monter` whip to
volume · `incorporer` fold in · `pétrir` knead · `laisser reposer` rest · `égoutter` drain ·
`émincer` slice thinly · `hacher` chop · `napper` coat · `déglacer` deglaze ·
`à feu doux / moyen / vif` low / medium / high heat.

## Dish-name titles

Keep the French name where that is the dish — `Tarte Tatin`, `Pâté Chinois`, `Bœuf
Bourguignon` — with an English gloss in Notes if it is not self-explanatory. Tag `french`, or
`quebecois` where the dish is specifically Québécois.
