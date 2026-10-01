# ElevatedHere

Marketing site and design documentation for the ElevatedHere platform — sponsored wellbeing
infrastructure: funding, delivery and proof, with privacy held at the centre.

**Live site:** https://clepbo.github.io/ElevatedHere/ *(enable Pages — see below)*

---

## What is in here

```
index.html                  Home — the full motion showcase
partner-organisations.html  For sponsoring organisations
beneficiaries.html          For the people receiving care
providers.html              For therapists, coaches and lawyers
pricing.html                Tiers, platform fee, comparison table
faq.html                    Privacy / money / delivery questions

assets/styles.css           Design tokens + home-page sections
assets/components.css       Shared components for inner pages + responsive rules
assets/app.js               Motion engine
assets/logo-*.png           Brand marks (dark and light)
assets/img/*.webp           Photography (17 images)

docs/design-system.md       Tokens, type scale, components, chart construction, copy rules
docs/decisions.md           Product and design decisions, with reasoning
docs/screen-inventory.md    All 153 product screens by role
docs/image-brief.md         Prompts for the photography still to be produced
```

No build step, no dependencies. Open `index.html` directly, or serve the folder.

## Publishing to GitHub Pages

The site sits at the repository root, so no workflow is needed:

1. **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main`, folder **`/ (root)`** → Save

It goes live at `https://clepbo.github.io/ElevatedHere/` within a minute or two. `.nojekyll` is
included so Jekyll does not interfere with the asset folder.

## Design system

The site uses the platform's own tokens — no invented colours, and Inter throughout.

| Token | Value | Use |
|---|---|---|
| `--green` | `#098e2d` | Primary actions, highlights, positive deltas |
| `--green-900` | `#04250f` | Dark bands (a shade of the brand green, not a new hue) |
| `--ink` | `#17181c` | Headings and body |
| `--grey` | `#8a8f8a` | Secondary text |
| `--border` | `#e5e7e5` | Panel and table borders |
| `--tile` | `#fafafa` | Page ground and stat tiles |

Full reference in [`docs/design-system.md`](docs/design-system.md).

## Motion

Every entrance animation is **two-way** — it plays on the way down and reverses on the way back up.
Counters reset and re-run; the word-by-word highlight is scroll-linked in both directions.

- Preloader with a scrambling word, on every load (`?nopre` skips it)
- Twin hero photo columns scrolling in opposite directions, pausing on hover
- Word-by-word statement reveal
- Words parting to admit a photo card
- Offset benefit rows sliding in from the side
- Arrow ticker, orbiting service icons, counters, animated progress bars
- Testimonial carousel, magnetic buttons, scroll progress bar

All of it is disabled under `prefers-reduced-motion`.

## Before this goes public

1. **Pricing is invented.** Structurally right, commercially made up — a warning banner says so on
   the page. Replace the figures and remove the banner.
2. **Testimonials are illustrative**, written to be plausible. Replace or remove.
3. **Photography is in place** — 17 commissioned images in `assets/img/`, optimised to WebP
   (676KB for the set). [`docs/image-brief.md`](docs/image-brief.md) holds the prompts behind them.
4. **Statistics** come from the design data, not audited figures. Confirm before claiming publicly.
5. Links marked `href="#"` — About, Careers, Contact, legal pages — need real destinations.
