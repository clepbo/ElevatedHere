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
