# ElevatedHere

Marketing site and design documentation for **ElevatedHere** — Africa's AI-powered, multi-language,
multi-channel, multi-currency social impact and wellness aggregator.

> **Empowering Lives, Anytime, Anywhere.**

Certified professionals across seven dimensions of wellbeing — mental health, legal & human rights,
career & business, personal development, financial literacy, social & relational and physical
— serving individuals (B2C), corporations (B2B) and government/NGOs (B2G). A session can
be paid for by the person, an employer, a programme, or an insurer.

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
docs/new-brand-prompt.md    Reusable prompt for rebuilding this template for another brand
```

No build step, no dependencies. Open `index.html` directly, or serve the folder.

## Publishing to GitHub Pages

The site sits at the repository root, so no workflow is needed:

1. **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main`, folder **`/ (root)`** → Save

It goes live at `https://clepbo.github.io/ElevatedHere/` within a minute or two. `.nojekyll` is
included so Jekyll does not interfere with the asset folder.

## Layout

The shell tracks the viewport rather than locking to a fixed column: it fills the window up to
**1720px**, past which a text line stops being comfortable to read. The outer margin
(`clamp(24px,3.4vw,96px)`), the inner gutter (`clamp(18px,3vw,72px)`), the body size and the
display sizes all scale with the screen, so the proportions hold from a 390px phone to an
ultrawide. Verified at 400 / 820 / 1180 / 1400 / 1900 / 2500 with no horizontal overflow on any
page.

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

Scroll is smoothed with a per-frame lerp (alpha 0.08 at 60fps), and entrance animations are
**scrubbed** rather than toggled — progress is a continuous function of scroll position, so
scrolling back up reverses everything for free. Counters reset and re-run.

There is no loading screen. A full-screen intro competes with image decode for the main thread on
exactly the frames it needs to be smooth, so the hero carries the entrance instead: three headline
lines rising 80ms apart, then the supporting rows.

- Twin hero photo columns scrolling in opposite directions, pausing on hover
- Word-by-word statement reveal
- Words parting to admit a photo card
- Offset benefit rows sliding in from the side
- Arrow ticker, orbiting service icons, counters, animated progress bars
- Testimonial carousel, magnetic buttons, scroll progress bar

All of it is disabled under `prefers-reduced-motion`.

## Before this goes public

1. **Pricing figures are still placeholders.** Structurally right, commercially made up. The
   on-page warning banner has been removed at the owner's request, so nothing on the site flags
   this any more — replace the numbers before the page goes near a customer.
2. **Testimonials are illustrative**, written to be plausible. Replace or remove.
3. **Photography is in place** — 17 commissioned images in `assets/img/`, optimised to WebP
   (676KB for the set). [`docs/image-brief.md`](docs/image-brief.md) holds the prompts behind them.
4. **Statistics** come from the design data, not audited figures. Confirm before claiming publicly.
5. **Seven dimensions, not eight.** Spiritual wellness is listed in the PRD but is not offered;
   the site covers the other seven. The PRD should be corrected to match.
6. **Several PRD areas are not on the site yet:** peer-support community, events, the AI wellness
   buddy and AI matching, CE courses, the insurance claims flow, the investor/courses page, and
   language/currency switching beyond the strings in the footer.
5. Links marked `href="#"` — About, Careers, Contact, legal pages — need real destinations.
