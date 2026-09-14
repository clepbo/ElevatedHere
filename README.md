# ElevatedHere — Partner Organisation (PO) Module

Design documentation for the Partner Organisation workspace: the surface an employer, NGO,
government body or community organisation uses to sponsor wellbeing services for the people it
serves, and to see what that sponsorship achieved.

> **This repository documents design, not code.** The source of truth for the interface is the
> Figma file; this repo records the model, decisions and conventions so the design survives
> hand-off and so the next person does not have to reverse-engineer it from screens.

---

## 1. What the module is for

The PO layer is not an administrative workspace that happens to list people. Its purpose is an
**impact intelligence layer**: the organisation funds services, and the module answers *what did
that money buy* — in adoption, in outcomes, and in return on social investment — without ever
exposing what an individual said in a session.

Three commitments follow from that, and they constrain every screen:

1. **The organisation sees the what and the how much, never the what was said.**
2. **Every debit is attributed** — to a beneficiary, a Project or Programme, and a provider — at
   the moment it is created. Attribution is what makes cost-per-outcome possible at all.
3. **Aggregates are suppressed below a minimum cohort size** (5) so no individual is identifiable
   by subtraction.

## 2. Vocabulary

Terminology is deliberate and consistent across the module — the UI was renamed to match.

| Term | Meaning |
|---|---|
| **Beneficiary (EU)** | The sponsored end user receiving services. *Never* "member" or "user". |
| **Partner Organisation (PO)** | The sponsoring tenant — employer, NGO, government, community. |
| **Service Provider (SP)** | Therapist, coach, lawyer or clinic delivering a service. |
| **Programme** | A reporting and outcome-target construct spanning Projects and cohorts. Holds the funding envelope. |
| **Project** | An operational unit with its own budget pool, providers and enrolled beneficiaries. |
| **Cohort / Segment** | A group of beneficiaries sharing a trait — department, geography, funder, employer, vulnerability segment. |
| **Allowance** | A per-beneficiary spending cap, drawn from a Project or Programme budget. |
| **Budget pool** | Money allocated to a Project or cohort, drawn down as services are used. |

## 3. Roles

Five roles, each with its own screen set. The reduced sets are intentional scoping, not gaps.

| Role | Persona | Sees |
|---|---|---|
| **Owner** | Jackson Obi | Everything. Funds the wallet, approves budget increases, configures the privacy dial. |
| **Admin-Manager** | Bola Ade | Operational parity with Owner, minus tenant-level and billing-mode control. |
| **Finance-Billing** | Ada Umeh | Wallet, budgets, invoices, transactions, reconciliation. Cost without outcome detail. |
| **Project-Manager** | Tunde Fashola | One Project's workspace. Requests budget rather than funding it. |
| **Analyst-Viewer** | Zainab Bello | Read-only aggregate reporting. No named beneficiary data. |

Where a role sees less, the interface says *why* — a lock icon and a one-line reason, never a
silently missing panel.

## 4. Information architecture

```
Overview
Beneficiaries ──── Directory · Engagement
Cohorts & Segments
Providers ──────── Direct SP Panel · Marketplace
Programs & Projects ─ Programs · Projects
Financials ─────── Overview · Wallet & Funding · Allowances & Budgets · Invoices & Seats · Transactions
Reports & ROI ──── L1 Operational · L2 Engagement · L3 Outcome · L4 Impact & ROI
Settings ───────── Org Profile & Type · Team & Roles · Privacy & Consent · Audit Log
```

Screens are named `PO — Section · Subsection (Role)`, with state suffixes `— Empty`,
`— No Results`, `— Failed`. The convention is load-bearing: ordering, nav highlighting and
role propagation all match on it.

## 5. The money model

```
PO tops up wallet ──▶ allocated to Programme envelope
                          └─▶ Project budget pool ──▶ beneficiary allowance
                                    │
       beneficiary books a service ─┴─▶ ESCROW ──▶ delivery confirmed ──▶ SP payout
                                                                   └─▶ EH platform fee
```

Every naira in the wallet sits in exactly one of five states, and they reconcile on screen:

**Available** + **Allocated to project budgets** + **Allocated to allowances** + **Committed (in
escrow)** + **Reserved for seats** = **Wallet balance**

Decisions worth knowing:

- **Reserved for seats is carved out of the balance**, not held separately.
- **Seats and platform fees settle automatically from available wallet funds** on the due date,
  with a card fallback. Service spend never appears on an invoice — it draws from Project budgets
  as it happens.
- **Fees are charged on top** of a top-up so the full amount reaches the wallet (processing fee,
  VAT on the fee, electronic transfer levy shown separately before confirmation).
- **KYC tiers (CBN three-tier)** cap wallet balance and transaction size; the UI blocks and
  explains rather than failing at the gateway.
- **Changing org currency does not convert funds.** A second balance opens in the new currency;
  conversion is an explicit, rate-stamped action.
- **Withdrawals** go only to the verified organisation account, with a 24-hour hold above a
  threshold — an AML control that cannot be skipped.

## 6. Privacy and consent model

Three tiers govern everything the organisation can see:

| Tier | Examples | Visibility |
|---|---|---|
| **Always private** | Session content, notes, recordings, case evidence, diagnoses | Never, regardless of who pays |
| **Operational** | Enrolment, spend, utilisation, active status | Consent-gated, governed by the Privacy Dial |
| **Aggregate** | Outcome trends, satisfaction, provider performance | Always safe, subject to minimum cohort size |

The **Privacy Dial** (Owner-only, overridable per Project) moves between *privacy-first* and
*case-management*, and shows the consequence before it is moved — including that widening it
requires re-consent from already-enrolled beneficiaries. Always-private data is **structurally
absent**, never shown as a locked row.

## 7. Reporting ladder

| Level | Answers | Contains |
|---|---|---|
| **L1 Operational** | What exists? | Beneficiaries, providers, projects, budgets; programme economics |
| **L2 Engagement** | Are they using it? | Activation, utilisation, retention, re-engagement; conversion funnel |
| **L3 Outcome** | Did it help? | Wellbeing, satisfaction, resolution, completion |
| **L4 Impact & ROI** | Was it worth it? | Cost per outcome, programme ROI, funding efficiency, social return |

**Programme economics** (cross-cutting): cost per beneficiary, per session, per case, per outcome;
programme utilisation; budget efficiency; provider efficiency. Each is spend divided by a stated
denominator, and **the denominator is always shown** — a cost-per-outcome figure means nothing
without knowing what counted as an outcome.

## 8. Module at a glance

153 screens across five roles.

| Role | Screens |
|---|---|
| Owner | 74 |
| Admin-Manager | 55 |
| Finance-Billing | 12 |
| Analyst-Viewer | 8 |
| Project-Manager | 4 |

See [`docs/screen-inventory.md`](docs/screen-inventory.md) for the full list,
[`docs/design-system.md`](docs/design-system.md) for tokens and components, and
[`docs/decisions.md`](docs/decisions.md) for the decision log.

## 9. Open items

- Multi-currency is modelled for display and conversion; multi-currency *settlement* is not built.
- L2–L4 reporting shows real populated figures with a phase note where full breakdowns are still
  to come.
- Provider photography uses placeholders pending an image source.
- Notification preferences and the activation checklist exist as concepts, not built screens.
