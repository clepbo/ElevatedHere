# Design system

Tokens and component conventions used across the PO module. Values are the ones actually in the
Figma file — match them exactly when adding screens.

## Colour

| Token | Hex | Use |
|---|---|---|
| Green (primary) | `#098e2d` | Primary actions, active nav, positive deltas, chart primary |
| Dark text | `#17181c` | Headings, values |
| Grey text | `#8a8f8a` | Labels, helper text, axis labels |
| Border | `#e5e7e5` | Panel and table borders |
| Panel background | `#ffffff` | All cards |
| Tile background | `#fafafa` | Stat tiles, table header rows |
| Chip background | `#f7f7f7` | Secondary buttons, inputs |

**Status palette** — used for pills, alerts and chart accents:

| State | Background | Foreground |
|---|---|---|
| Active / Healthy / positive | `#e7f6ec` | `#098e2d` |
| Pending / Watch / caution | `#fef3c7` | `#b45309` |
| Failed / At risk / negative | `#fee2e2` | `#b91c1c` |
| Processing / informational | `#dbeafe` | `#1d4ed8` |
| Offboarded / neutral | `#f3f4f6` | `#6b7280` |
| Refunded | `#ede9fe` | `#7c3aed` |

**Chart sequence** (composition charts, in order): `#098e2d`, `#34b366`, `#0f969d`, `#2868e0`,
`#733dd0`, `#e96729`, `#dd3571`, `#b45309`. Neutral remainder: `#c9ccc9`.

**Avatar palette**: teal `#0f969d`, orange `#e96729`, blue `#2868e0`, purple `#733dd0`,
green `#0ba55d`, pink `#dd3571`.

## Type

Inter throughout — Regular, Medium, Semi Bold.

| Role | Size | Weight |
|---|---|---|
| Screen title | 20 | Semi Bold |
| Panel title | 16 | Semi Bold |
| KPI value | 22 | Semi Bold |
| Stat tile value | 18 | Semi Bold |
| Body / table cell | 13 | Regular / Medium |
| Field value | 14 | Semi Bold |
| Helper, axis, sub-label | 11–12 | Regular |
| Table column header | 10–11 | Semi Bold, grey |

## Layout

- Screen 1440 wide. Sidebar + Main; Main holds Topbar + Content.
- **Content width 1144**, panel padding 24, so inner content width is **1096**.
- Panel: white, 1px border, radius 12, vertical auto-layout, gap 16–20.
- Table row: px 16–24, py 13–16, 1px bottom border; header row background `#fafafa`.
- Screens target 1,000–1,500px tall. Past ~2,000px, split the screen.

## Components

**KPI card** — icon chip (38×38, radius 10, tinted background) + label + value + delta pill
(`↑ +12.5%`) + comparison basis. Every KPI carries a delta; a number without a trend is not a KPI.

**Stat tile** — compact label / value / sub, `#fafafa` background. Use where five or more metrics
sit in one row and deltas would crowd.

**Status pill** — radius 999, px 10, py 4, 11–12px medium text, from the status palette.

**Buttons** — primary: green fill, white semibold 13. Secondary: white or `#f7f7f7` fill, border,
dark text. Destructive: white fill, `#f3b8b8` border, `#b91c1c` text.

**Note strip** — tinted row with icon + one or two sentences. Green for explanation, amber for
caution, red for failure. This is where the *insight* goes, not a description of the widget.

**Progress row** — avatar chip + name/sub + bar + value + trend chip. Must contain an `<Icon>`
(see the renderer note in the skill) — the trend chip provides it.

**Segmented toggle** — pill group in a `#f3f4f3` track; the active option is a white pill with a
border. Used for view switching (Beneficiaries ⇄ Providers; Budgets / Allowances / Planning).

## Charts

Built as real Figma vectors, not images, so they stay editable.

- **Donut**: ellipse `arcData` with `innerRadius` 0.64 (0.72 for a single-value ring), angles
  starting at `-π/2`, small gap between segments. Total in the centre, breakdown in a legend beside
  it with values.
- **Line / area**: `createVector()` + `vectorPaths`; smoothed cubic path, 2.5px stroke, area fill
  as a vertical gradient from 22% to 0% opacity. Gridlines `#f0f1f0`, axis labels 10px `#a8aca8`.
  One annotated marker — dot with white ring plus a dark tooltip naming the value and why it matters.
- **Bar**: radius 6, `#8fd0a3` with the current period in `#098e2d`.
- **Funnel**: trapezoid vectors stepping down in the green sequence; pair with a table giving
  count, % of previous, and drop-off.

**Rules**: never two incomparable scales on one axis; always state the denominator; show the
unflattering number.

## Copy

Keep scope, period, denominator, policy, consequence. Cut anything that narrates the interface.

| Cut | Keep |
|---|---|
| "Switch between who is being served and who is delivering" | "Aggregate only · minimum cohort size of 5" |
| "What kind of file you need" | "Of 312 assessable beneficiaries" |
| "Narrow the ledger, then group it the way you report on it" | "Exhausts 2 Oct at this rate" |

Insight notes should name what the data shows and what to do about it — "The biggest single loss
is consent, not activation — 56 invited beneficiaries never consented."
