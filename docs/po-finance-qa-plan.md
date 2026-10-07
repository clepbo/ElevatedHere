# PO Finance QA — reading, reconciliation and build plan

Sources: `PO - Finance QA.pdf` (81pp, Finance section pp.37–81, ~90 design tasks across six tables)
and `PO - Final Concept Note.pdf` (16pp). This document reconciles them, states the model the
designs must obey, and sequences the work.

---

## 1. The model, reconciled

The QA raises a **data-model contradiction** (QA item 6): Program detail shows a combined budget,
while Create Program says programs do not hold budget. The updated Concept Note (p.3) resolves it,
and this is the version the designs must follow:

| Object | Financial role | Means |
|---|---|---|
| **Program** | financial **ceiling / allocation envelope** | strategic intervention — the WHY. Holds an envelope, not a spendable balance |
| **Project** | **executable budget** | where the intervention is executed — the WHERE/HOW. Money is committed and spent here |
| **Cohort** | **optional allocation** within a project or program | the population served — the WHO |
| **Transaction** | **actual money movement** | the only object that moves money |

So a Program *does* show a figure — but it is an envelope and must be labelled as one. It is not a
wallet, it is not spendable, and it must never be summed alongside Project budgets as if it were an
independent balance. This is exactly the "no overlapping figures presented as independent balances"
acceptance criterion in QA Table 1 (Fix Balance Reconciliation).

**Full chain:** Organization → Program → Project → Cohort → Beneficiary/Provider → Service Delivery
→ Outcomes → Financial/Impact Reporting.

**Both operating shapes stay supported.** A small PO runs flat — Direct SP Panel, directly
sponsored EUs, org-wide budget — with no Projects at all. Projects are optional sub-workspaces. Any
IA that forces a Project breaks the flat model.

---

## 2. IA restructure — Programs as parent

The PO's instruction: **Projects and Cohorts become sub-tabs under Programs.** A Program can exist
independently; Projects and Cohorts exist under a Program.

```
Programs                                    ← parent nav item
├── Programs      (tab, default)            ← strategic interventions
├── Projects      (tab)                     ← executable units, each under a Program
└── Cohorts       (tab)                     ← populations, scoped to a Program or Project
```

Decisions this forces, and how to handle each:

- **A Program must be creatable on its own**, with no Project required. Keep Create Program
  standalone.
- **Projects and Cohorts are scoped.** Each must display its parent Program on the row and on the
  detail header. Creating one from its tab requires picking a Program first.
- **Flat organisations still need a home.** When a PO runs flat, the Projects tab should not be a
  dead end — show an empty state explaining that Projects are optional, with the org-wide budget as
  the alternative route.
- **Microcopy on the parent** (QA item 2): "Plan interventions, fund projects and track outcomes."
- **Program detail should lead with strategy, not storage** (QA items 4–5): objective, outcome
  target, timeline, cohorts, projects, envelope — in that order. A Project leads with objective,
  geography, timeline, cohort, providers, budget and outcomes.

---

## 3. Finance IA — the spine

From Concept Note §11. The QA's six tables map onto it almost exactly, which is the strongest signal
that this is the structure to build against.

```
FINANCIALS
├── Overview                        ← NEW. Does not exist today (QA Table 1, first task)
├── Funding
│   ├── Wallet
│   ├── Funding Sources
│   ├── Auto-reload
│   └── Escrow
├── Budgets & Allowances
│   ├── Budget Pools
│   ├── Member Allowances
│   └── Approvals
├── Billing
│   ├── Invoices
│   ├── Seats & Plans
│   └── Payment Terms
├── Transactions
│   ├── Ledger
│   ├── Reconciliation
│   ├── Refunds
│   └── Payouts
└── Financial Reports & Dashboards
    ├── Spend
    ├── Budget Performance
    ├── Program Economics
    └── ROI
```

---

## 4. The six QA tables → build order

Sequenced so each stage unblocks the next, and so the structural work lands before the decorative.

### Stage 1 — Balance model and Finance Overview *(Table 1, pp.37–46)*

The foundation. Nothing downstream reconciles until this does.

- **Finance Overview** landing page before Wallet & Funding: available, committed, allocated,
  actual spend, pending settlements, invoices due, alerts, reporting-period selector.
- **Six distinct balances, each its own card with a definition:** Available, Allocated, Committed,
  Reserved, Spent, Pending Settlement.
- **Documented reconciliation** between wallet balance, project budgets, allowances, seats, escrow,
  provider payables and pending transactions. No figure may appear twice as an independent balance.
- **Balance calculation breakdown** — click a card, see the credits, debits, holds and allocations
  behind it.
- **Escrow visibility** and **Pending Settlement** as separate, explicit states.
- **Standardised transaction statuses:** Pending, Processing, Completed, Failed, Reversed,
  Refunded, Disputed, Reconciliation Required.
- **Financial audit trail:** actor, action, timestamp, record, reason, reference, before/after.
- **Approval workflow + Approval Inbox.**
- **Wallet & Funding redesign**, top-up flow, funding sources (+ attribution categories: Grant,
  Donor, Corporate, Government, Internal), failed top-up UX, payment recovery, success actions,
  auto-reload, funding alerts, funding history.

> The failed-top-up requirement is subtle and worth calling out: **separate the payment provider's
> reported status from ElevatedHere's interpretation.** Distinct states for decline, timeout,
> pending confirmation and confirmed failure — never tell someone a payment failed while the outcome
> is still unknown.

### Stage 2 — Budgets, allowances, approvals *(Table 2, pp.46–54)*

- Budget cards: cap, committed, spent, remaining, forecast, period, status.
- **Budget health** — Healthy / Watch / At Risk / Exhausted, from utilisation *and* remaining *and*
  burn rate, not one percentage.
- **Budget states** — Draft → Pending Approval → Active → Near Limit → Exhausted → Closed.
- Create Budget Pool with funding source, programme/project, period, owner, eligible categories,
  approval requirements, and the wallet impact shown before submission.
- **Funding restrictions** (programme, project, region, service, cohort) — restricted funds must
  never present as unrestricted capacity.
- Budget detail, approval flow, Request More Budget.
- **Three distinct actions, never conflated:** Request Additional Funds · Reallocate Existing Funds
  · Change Approved Budget Cap.
- Budget change history, alerts, burn rate, spend forecast, runway, cost centre.
- Project spend drill-down: Project → Budget → Spend → Provider → Engagement.
- Beneficiary funding view (privacy-safe identifiers), allowance management, allowance exceptions,
  member/cohort allocation, budget closure.

### Stage 3 — Invoices, seats, transactions, accounting *(Table 3, pp.55–64)*

- Separate **Invoices** from **Subscriptions & Seats** conceptually.
- Invoice list, detail, actions, and a full status lifecycle (Draft, Issued, Pending Payment,
  Partially Paid, Paid, Overdue, Disputed, Cancelled, Credited/Adjusted).
- Payment terms visibility — without implying credit terms are universal.
- Credit note / adjustment flow.
- Seat management and assignment, subscription lifecycle, enterprise commercial CTA.
- Transaction list and detail drawer with full fee breakdown.
- **Financial ledger** distinct from transaction history; **chart of accounts** if EH is the
  accounting system of record.
- **Reconciliation workspace:** gateway → wallet ledger → escrow → payouts, with exceptions
  (missing, duplicate, amount mismatch, timing, unresolved settlement).
- Refunds and reversals, payout visibility, configurable fee/tax breakdown.
- **FX architecture** — transaction / settlement / reporting currency, rate, rate timestamp,
  converted amount, FX fees. Values in different currencies must never sit side by side as
  comparable.
- Export centre, export permissions and history.

### Stage 4 — Reports, programme economics, ROI *(Table 4, pp.64–71)*

- Financial reports catalogue.
- **Two-way link between Finance and Impact:** "View Impact of This Spend" from budgets, projects
  and transactions; "View Investment Behind This Outcome" from reports. Carry the programme and
  period across.
- Programme economics: spend by programme, project, provider, service, period; budget vs actual.
- Cost per Beneficiary · per Active Beneficiary · per Session/Service · per Outcome — each with its
  denominator, period, inclusions and exclusions stated on screen.
- Funding performance, Programme ROI, Social Return, Funder Reporting.
- Geographic finance, budget-year model (FY/Q1–Q4), procurement references (PO number, grant code,
  contract reference), historical comparison.
- Financial health alerts, report definitions and data freshness.

### Stage 5 — Enterprise readiness, roles, states *(Table 5, pp.72–79)*

- PO onboarding: explore before completing everything, guided checklist, verification status and
  recovery. **Funding and activation stay gated behind KYB** — that gate is not negotiable.
- Lead with intent, not roles. Delay non-essential friction. First-value journey. Sales-assisted
  route.
- Explain billing models before selection, with unavailable options clearly labelled.
- **Role-based finance navigation** for Owner, Admin/Manager, Project Manager, Finance/Billing,
  Analyst/Viewer, per Concept Note §3.
- Permission-based actions: View, Create, Edit, Submit, Approve, Export, Administer — with
  permission-denied states that explain the route without leaking protected information.
- **Privacy:** no clinical notes, session content or case evidence in any finance view, ever.
  Aggregate reporting respects the minimum cohort size.
- External provider payments: **Paid Through ElevatedHere** vs **Recorded Externally**, never
  blended.
- Empty, loading and error states. Accessibility — status never by colour alone.
- Standardised finance components.

### Stage 6 — Handoff and acceptance *(Table 6, pp.79–81)*

Finance sitemap · end-to-end flows · screen-state inventory · financial consistency review ·
permissions and privacy review.

---

## 5. Cross-cutting rules

These apply to every screen and are the ones most likely to be violated by accident:

1. **No figure appears twice as an independent balance.** The reconciliation defined in Stage 1
   governs every later screen.
2. **Every metric shows its denominator**, period, inclusions and exclusions. This is stated
   separately for cost per beneficiary, per active beneficiary, per session and per outcome.
3. **Never present an estimate as a fact.** Forecast, runway and ROI appear only where the data
   supports them, labelled as estimates with their assumptions visible.
4. **Status is never colour alone.**
5. **Restricted funds never read as spendable capacity.**
6. **Private content never reaches a finance view**, regardless of who paid.
7. **Actions appear only when valid** for the record's status and the user's permission.

---

## 5A. Ripple — what else these changes touch

Neither change is contained. Both the IA restructure and the balance model propagate, and a
half-applied change is worse than none: it produces screens that disagree with each other. Every
item below has to move with the change, not after it.

### From the IA restructure (Projects and Cohorts under Programs)

| Surface | Adjustment |
|---|---|
| Left nav / sidebar, every PO screen | One parent **Programs**; Projects and Cohorts stop being top-level destinations |
| Breadcrumbs | Every Project and Cohort screen gains `Programs › <Program> › <Project>`; Cohort shows its Program and, where scoped, its Project |
| Project list and detail | Parent Program on every row and in the detail header; Program becomes a filter |
| Cohort list and detail | Same, plus which Project where applicable |
| Create flows | Create Project and Create Cohort require a Program first; Create Program stays standalone |
| Dashboard / Overview | Any "Projects" or "Cohorts" tile links into the Programs parent, not a removed route |
| Reports & ROI filters | Programme becomes the primary filter, Project the secondary — the hierarchy must match |
| Finance budget pools | A pool bound to a Project must name its Program too; grouping by Program becomes available |
| Members / Beneficiaries | Cohort references carry the Program |
| Search and deep links | Any saved or in-design link to a top-level Projects/Cohorts route needs repointing |
| Role scoping | Project Manager scope is "one Project **within a Program**"; Program Manager is distinct |
| Empty states | Flat organisations need a Projects empty state that explains Projects are optional |

### From the balance model (six distinct balances, Program as envelope)

| Surface | Adjustment |
|---|---|
| Every screen showing a money figure | Must say *which* balance it is — Available, Allocated, Committed, Reserved, Spent, Pending Settlement |
| PO Overview / dashboard KPIs | Re-derive against the reconciliation; remove any figure that double-counts |
| Program detail | Figure relabelled as an **envelope/ceiling**, visibly not a spendable balance, never summed with Project budgets as a peer |
| Project detail | Executable budget, with committed and reserved split out from spent |
| Wallet | Available funds stop implying "all of this is spendable" where allocations and holds exist |
| Allowances | Consumption reconciles to the budget it draws from |
| Invoices and seats | Amounts owed must not read as wallet movements |
| Transactions and ledger | Status vocabulary standardised to the same eight states everywhere |
| Reports | Spend figures reconcile to the same definitions, with denominators stated |
| Existing sample data | Every number re-checked so connected screens agree — this was already a repeat defect on this file |

### Working rule

When a change lands on a screen, check the same concept everywhere else it appears **before moving
on**. A sweep at the end misses the quiet ones — a stat tile, a filter label, a breadcrumb — and
those are exactly where inconsistency gets noticed.

---

## 6. Decisions needed before parts of this can be designed

The QA itself defers these — it repeatedly says "where supported", "if in Phase 1", "confirm with
the product owner". Designing them blind guarantees rework.

| # | Decision | Blocks |
|---|---|---|
| 1 | **Phase 1 billing modes.** Concept Note recommends wallet → invoicing → seats. Which ship in Phase 1? | Invoices, Seats, Payment Terms, billing-model comparison |
| 2 | **Payment integration for Phase 1** (Paystack / Stripe / bank transfer / crypto) | Funding source types, top-up flow, failure states, recovery |
| 3 | **Approval thresholds** — what value triggers approval, and who approves | Approval workflow, Approval Inbox, budget increase |
| 4 | **Budget health thresholds** for Healthy / Watch / At Risk / Exhausted | Budget cards, alerts |
| 5 | **ROI definition** — what counts as a return, how valued, which costs and outcomes included | Programme ROI, Social Return |
| 6 | **Is EH the accounting system of record?** | Chart of accounts, ledger — large scope swing |
| 7 | **Minimum cohort size `k`** for aggregate reporting (Concept Note suggests k ≥ 5) | Every aggregate report |
| 8 | **Partially-paid invoices and credit notes** — in Phase 1 or not | Invoice lifecycle |
| 9 | **Multi-currency now or later.** QA says in scope; confirm which currencies settle | FX architecture, geographic finance |
| 10 | **Confirm the Program-as-envelope reading** in §1 above | Program detail, all budget roll-ups |

My proposal: design 1–2 and 10 first since they gate the most, assume the Concept Note's phasing
(wallet first) for everything else, and mark seats/invoicing screens as Phase 2 rather than omitting
them.

---

## 7. Implementation log

Figma file `1gK0GIsSnf3Efu2yXXpbrR`, page **Partner-Organizations**. 189 frames.

### Decisions taken (were §6 open questions)

| # | Decision | Rationale |
|---|---|---|
| 1 | **Phase 1 = prepaid wallet.** Invoicing and seats designed, marked Phase 2 | Concept Note §6: the wallet, escrow and virtual-account rails already exist |
| 2 | **Paystack + bank transfer**, Stripe for international | Both in the PRD stack; Paystack is the Africa-first default |
| 3 | **EH is the accounting system of record** | QA p.61 states the intent, so the ledger and chart of accounts get designed properly |
| 4 | **k = 5** for aggregate reporting | Matches the "cohorts of five or more" already used across this file |

### IA restructure — complete

- `Nav-CohortsSegments` removed from the sidebar on **128** frames; `Nav-ProgramsProjects` → `Nav-Programs`, relabelled **Programs** on **136**.
- Active state transferred on the **14** frames where Cohorts was the selected item.
- **Analyst/Viewer** nav had Cohorts but no Programs entry — converted rather than removed, so analysts keep a route.
- Cohorts tab added to the 4 existing tab rows; full three-tab row added to the 5 Cohorts screens.
- **29** topbar titles corrected; **9** frames renamed to `PO — Programs · …`.
- Flat-organisation empty state built for the Projects tab — Projects stay optional.

### Finance — built

**Stage 1**
- Six-balance model on all three Overview screens. **Reserved and Pending Settlement did not previously exist.** Reconciliation stated on screen: `Position = Available + Allocated + Committed + Reserved + Pending = ₦19,490,000 funded; Spent is a 30-day flow and is not part of the position.`
- **Balance Breakdown · Available** — an 11-line waterfall from opening cash through credits, debits and earmarks, tying to the Overview's Money movement panel and position tiles.
- **Escrow register** — held / awaiting delivery / release blocked / released, with release condition and expected release per engagement. Sums to the ₦940,000 Reserved balance.
- **Financial audit trail** — actor, action, record, before → after, reference, across budgets, rules, approvals and adjustments.
- Transaction statuses: the three missing ones (Reversed, Disputed, Reconciliation Required) added, and a **STATUS column added to the Admin-Manager and Finance-Billing tables, which had none**.
- **Top-up outcome-unknown state** — the case the QA warns about, where the gateway has not returned a result. Separates the provider's reported status from EH's interpretation; primary action is Check status, not Retry.
- Approvals list gained programme and urgency.
- Drill-down links added to the Overview position panel.

**Stage 2**
- **Budget lifecycle STATE** added as a column distinct from HEALTH — Draft, Pending approval, Active, Near limit, Exhausted, Closed — with two rows added to show the pre-active stages. "Closed" was previously sitting in the FORECAST column, conflating state with forecast.
- **Three distinct budget actions** — Request additional funds / Reallocate existing funds / Change approved cap — each stating its effect on Available before submission.

**Stage 3**
- Invoice table gained **PAID** and **OUTSTANDING** columns and the fuller lifecycle: Paid, Pending payment, Partially paid, Disputed, Overdue, Draft. Only Paid and Due existed before.
- **Financial Reports** tab added to all 21 Finance screens, with a report catalogue screen built behind it so the tab is not a dead end.

### Defects found and fixed in passing

- Programs screen read *"outcome targets, no budget of their own"* directly under a "Budget committed ₦18.7M" KPI — the contradiction QA item 6 raises.
- A second instance of the same class on the Overview: a Q3 budget bar against a wallet position with nothing saying they are different axes.
- Duplicate "Overview" tab on `Financials · Transactions (Admin-Manager)`.
- Five screens highlighting the wrong sidebar item, including all three Finance Overviews highlighting Overview.

### Verified

- Nav active state: **138 screens correct, 0 real mismatches** (the 11 flagged are heuristic false positives — role suffixes such as "Finance-Billing" matching `/Financ/`).
- Every new screen screenshotted and read back; clone artefacts corrected (stale avatars, inherited failure copy, wrong semantic colours).

### Left open deliberately

- **Adjust Allowance Cap** (×3) highlights Beneficiaries and **Adjust Cohort Budget** (×2) highlights Programs. Both are plausibly entered from there, so this is a product decision rather than a defect.
- Sample data across connected Finance screens still needs a full consistency pass now the balance model has changed.
- Not yet built: funding restrictions display, budget change history, allowance exception workflow, reconciliation exceptions detail, FX architecture, cost-per-outcome methodology panels, empty/loading/error state sets, and the Stage 6 handoff artifacts.

### Completed after the first pass

**Stage 2 finished** — funding restrictions panel (dimension, restricted to, set by, effect, type,
with the rule that restricted grant money never counts toward Available); budget change history
(when, actor, what changed, from → to, reference, status); and an **allowance exception register**
with 14 active exceptions across individuals and cohorts, each with scope, change, reason,
effective date and lapse behaviour.

**Stage 3 finished** — reconciliation and FX audited and found sound. Convert Currency had a real
arithmetic bug: converting ₦1,520,000 *out* of NGN showed the NGN balance **rising** to
₦16,720,000. Corrected to ₦6,720,000, with a rate timestamp and a reporting-currency rule added.

**Stage 4 finished** — **Cost per active beneficiary** added alongside cost per beneficiary, which
the QA explicitly requires to be distinguished (₦59,950 against 213 active, versus ₦34,700 against
368 enrolled). Methodology note rewritten to say the two must never be compared.

**Stage 5 finished** — **PO — Financials · State Set**: 12 designed states covering six empty
states (no funding sources, no budget pools, no transactions, no invoices, no reports, nothing
awaiting approval) and six system states (loading, validation failure, session expiry, gateway
unreachable, permission denied, export failed). Each states what happened, what it means for the
money, and gives exactly one next action.

**Stage 6 finished** — `docs/po-finance-handoff.md` carries the Finance sitemap, eight end-to-end
flows, the screen-state inventory, the financial consistency review and the permissions/privacy
review.

### Sample-data consistency pass — complete

Governing identity now holds across every connected screen:

```
Available 8,240,000 + Allocated 8,400,000 + Committed 1,600,000
        + Reserved 940,000 + Pending 310,000 = 19,490,000
```

Three further contradictions were found and corrected during the pass:

1. **Wallet & Funding** split summed to ₦18,240,000 against a ₦19,490,000 position — it had no
   Reserved or Pending tile and folded escrow into Committed. Now seven tiles summing exactly to
   ₦19,490,000, with the footer arithmetic rewritten to match.
2. **Provider Payouts** reported ₦1,600,000 "still in escrow" for the same 38 engagements the Escrow
   register showed at ₦940,000 — it was labelling Committed as escrow.
3. **Convert Currency** balance-after bug described above.

Verified: 11 new frames, no overlaps; nav active state correct on 138 screens with no real
mismatches.

---

## 8. Programs / Projects / Cohorts QA (pp. 1-36)

The other half of the same document: ~60 tasks across P0/P1/P2. The reviewer's recommended budget
model on p.17 matches what was already built for Finance — Program = ceiling/envelope, Project =
executable budget, Cohort = optional allocation, Transaction = actual movement — so nothing had to
be reworked.

### P0 — all 14 complete

| Task | What was done |
|---|---|
| Resolve Program/Project model | Applied across every screen; Create Program no longer claims programmes hold no budget |
| One canonical data model | 4 programmes, spends summing to ₦12.78M against an ₦18.67M envelope, 90 verified outcomes |
| Fix inconsistent sample data | KPI said 3 active programmes, the table listed 2, the progress panel 3. Now 4 everywhere |
| Separate lifecycle vs health | LIFECYCLE and HEALTH are separate columns on projects; Program Detail shows "Behind plan" with the rule stated |
| Redesign Programs landing | Portfolio health strip → needs review → charts → table, as the reviewer sketched |
| Redesign Projects landing | Health, parent programme and lifecycle on every row; action-identifiable at a glance |
| Explanatory tab copy | Added to all 11 Programs/Projects/Cohorts frames |
| Fix misleading health state | **QA item 26**: "On pace" sat above 91% consumed, ₦0.21M left, 11 days to run. Now "At risk · near budget limit" on all four frames carrying it |
| Make warnings actionable | Observation → Evidence → Action, with Adjust budget / Cap enrolment / Review spend beside the warning |
| Engagement funnel interactive | Every stage drills in and names its drop-off; an action queue ranks the three recovery opportunities |
| Connect program → project | Linked projects carry allocation, spend and outcome contribution |
| Connect project → cohort | Project headers name programme and cohort; the view toggle gained Cohorts |
| Connect finance | "Open budget" on Program Detail |
| Connect Reports & ROI | "View Impact Report" and "Export M&E Report" |

### P1 — done

Outcome target as Baseline 62 → Current 69 → Target 74 with progress stated as 7 of 12 points
gained; measurement source named (WHO-5); programme owner and dates; Create Project gained a parent
programme field and a live allocation preview ("₦4.00M of the ₦12.37M envelope still unallocated");
charts carry period, definition and source; portfolio and project filters plus saved views; audit
visibility ("Recent changes") on Program and Project Detail; privacy tier indicators (Aggregate /
Operational / Consent required) on six detail screens; provider rows deepened to sessions, active
beneficiaries, capacity and spend; cohort rows deepened to enrolled, activated, utilisation,
outcomes and spend.

### P2 — done

Outcome contribution by project (42% / 31% / 27%); contextual expansion triggers on both landings,
written as the reviewer asked — behaviour-triggered, not "Upgrade Now": *"Q3 Wellness Access has 4
places left of 90"*, *"Three programmes now report separately"*.

### Not done

- Project dashboard is correct but not re-grouped under labelled **Outcome / Delivery / Finance**
  headings — the content is all present, the sectioning is not.
- Report configuration screen (period, programme, project, cohort, metric).
- Cohort comparison, provider contribution and portfolio allocation (Program → Projects → Cohorts)
  panels.
- Per-role permission states on these screens beyond the role variants that already exist.

Verified: 0 stale contradictions across the five restructured screens.
