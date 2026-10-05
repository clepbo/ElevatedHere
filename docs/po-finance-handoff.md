# PO Finance — Phase 1 design handoff

Satisfies QA Table 6. Figma file `1gK0GIsSnf3Efu2yXXpbrR`, page **Partner-Organizations**.
51 Finance screens.

---

## 1. Finance sitemap

Navigation is one parent — **Financials** — with six tabs. Detail views are reached from their
parent and carry a "Back to …" link rather than adding tab clutter.

```
Financials
├── Overview                    ← landing: position, alerts, spend, money movement, economics
│     ├── Balance Breakdown · Available        (drill-down from any balance card)
│     ├── Escrow                                (drill-down from Reserved)
│     └── Audit Trail                           (drill-down from the position panel)
│
├── Wallet & Funding
│     ├── Top Up Wallet → Wallet Funded
│     │                 → Failed  (confirmed decline)
│     │                 → Outcome Unknown  (gateway gave no result)
│     ├── Withdraw to Bank
│     ├── Convert Currency
│     └── Auto-reload rules
│
├── Allowances & Budgets        ← tabs: Budgets · Allowances · Planning
│     ├── New Budget Pool
│     ├── Manage Budget Pool    (+ restrictions, + change history)
│     ├── Adjust Allowance Cap
│     ├── Adjust Cohort Budget
│     ├── Allowance Exceptions  (register)
│     ├── Request More Budget   (3 actions: add funds · reallocate · change cap)
│     └── Approvals             (inbox + decision detail)
│
├── Invoices & Seats
│     ├── Invoice Detail
│     └── Dispute Invoice
│
├── Transactions
│     ├── Transaction Detail
│     ├── Reconciliation        (+ exceptions)
│     ├── Provider Payouts
│     ├── Refund or Reverse
│     └── Cost Centres
│
└── Reports                     ← catalogue of six finance reports
      └── Export Report         (format · scope · privacy · delivery)
```

Role variants exist for Owner, Admin/Manager and Finance/Billing. Project Manager reaches budget
requests through Project Workspace; Analyst/Viewer sees aggregate reporting only.

---

## 2. End-to-end flows

Each has a defined start, success state and recovery route.

**Funding**
`Wallet & Funding → Top Up → amount → source → review fees and limits → authorise → confirm`
→ success: **Wallet Funded** with reference, updated balance, and Allocate / View transaction
→ failure: **Failed** (confirmed decline, with bank's words and our interpretation separated)
→ unknown: **Outcome Unknown** (no result yet; retry suppressed, Check status is primary)

**Allocation**
`Wallet → New Budget Pool → name, source, programme/project, amount, period, owner, restrictions
→ shows wallet impact before submission → Active`

**Allowance**
`Allowances → default cap → exception for an individual or cohort → reason, effective date, expiry,
authorisation → Exception register → lapses on end date unless renewed`

**Budget increase**
`Manage Budget Pool → choose one of three actions → amount, justification, urgency, source
→ Approvals inbox → Owner decision → audit entry → cap changes; money moves only on allocation`

**Invoice**
`Invoices → list filtered by status → Invoice Detail → Download / Pay / Dispute
→ Dispute Invoice → credit note or adjustment linked to the original`

**Transaction investigation**
`Transactions → filter → Transaction Detail (fee breakdown, timeline) → related invoice, budget or
original transaction → Audit Trail`

**Reconciliation**
`Transactions → Reconciliation → import gateway statement → run → matched / unmatched
→ exception detail → owner and resolution status`

**Reporting**
`Reports → catalogue → report with period and definitions → View impact of this spend → Reports &
ROI (programme and period carried across) → Export Report`

---

## 3. Screen-state inventory

Designed in **PO — Financials · State Set** (12 states) and applied per screen.

| Screen | Default | Empty | Loading | Error | Blocked | Success |
|---|---|---|---|---|---|---|
| Overview | ✔ | — | ✔ | — | ✔ | — |
| Wallet & Funding | ✔ | no funding sources | ✔ | gateway unreachable | ✔ | — |
| Top Up | ✔ | — | ✔ | declined · **outcome unknown** · amount exceeds Available | ✔ | Wallet Funded |
| Allowances & Budgets | ✔ | no budget pools | ✔ | — | ✔ | — |
| Manage Budget Pool | ✔ | — | ✔ | amount exceeds Available | ✔ | — |
| Allowance Exceptions | ✔ | no exceptions | ✔ | — | ✔ | — |
| Approvals | ✔ | nothing waiting | ✔ | — | ✔ | decision recorded |
| Invoices & Seats | ✔ | no invoices | ✔ | — | ✔ | — |
| Transactions | ✔ | no transactions | ✔ | — | ✔ | — |
| Reconciliation | ✔ | — | ✔ | unmatched items | ✔ | run complete |
| Reports | ✔ | no reports available | ✔ | export failed | ✔ | export delivered |

Session expiry applies to every screen and preserves the draft.

---

## 4. Financial consistency review

The sample data was re-derived so connected screens agree. The governing identity:

```
Available 8,240,000 + Allocated 8,400,000 + Committed 1,600,000
        + Reserved 940,000 + Pending settlement 310,000
        = 19,490,000  (cash on hand)
```

Verified ties:

| Figure | Appears on | Status |
|---|---|---|
| Position total ₦19,490,000 | Overview, Balance Breakdown, Wallet & Funding header | agree |
| Wallet tile sum | Wallet & Funding — 7 tiles | sums to **19,490,000** |
| Reserved ₦940,000 | Overview, Escrow, Provider Payouts | agree |
| Allocated ₦8,400,000 | Overview = project budgets 5.6M + allowances 2.3M + seats 0.5M | agree |
| Net movement +₦2,134,000 | Overview money movement, Balance Breakdown | agree |
| Released to providers ₦9,840,000 | Escrow, Provider Payouts, Balance Breakdown | agree |
| Q3 consumed ₦12.76M | Overview, Allowances & Budgets, Reconciliation | agree |

**Contradictions found and corrected during the pass**

1. Wallet & Funding split summed to ₦18,240,000 against a ₦19,490,000 position — it had no Reserved
   or Pending tile and folded escrow into Committed.
2. Provider Payouts showed ₦1,600,000 "still in escrow" for the same 38 engagements the Escrow
   register showed at ₦940,000 — it was reporting Committed under an escrow label.
3. Convert Currency showed the NGN balance **rising** to ₦16,720,000 after converting ₦1,520,000
   *out* of NGN. Correct figure ₦6,720,000.
4. Spent was presented as a sixth balance alongside five position balances; it is a period flow and
   is now labelled as one.
5. Programs detail claimed programmes hold "no budget of their own" directly beneath a committed-budget
   KPI.

---

## 5. Permissions and privacy review

**Role scope** (Concept Note §3), applied to the Finance navigation:

| Role | Finance nav | Can do | Cannot |
|---|---|---|---|
| Owner | full | fund, approve, change caps and billing mode, withdraw, refund | — |
| Admin / Manager | full minus treasury actions | budgets, allowances, programme spend | billing-critical changes |
| Finance / Billing | Overview, Wallet, Allowances & Budgets, Invoices, Transactions, Reports | funding, billing, invoices, payouts, spend reports | manage members, outcome detail |
| Project Manager | via Project Workspace | request budget within their project | anything outside their project |
| Analyst / Viewer | Overview, Reports | read-only aggregate reporting | any change, any named content |

**Privacy** — the governing rule is that a finance view shows *what and how much*, never *what was
said*:

- No clinical notes, session content, assessment answers, diagnoses or case evidence appears on any
  finance screen, regardless of who paid.
- Beneficiary funding views use privacy-safe identifiers and show allowance, consumption and
  remaining — never service content.
- Aggregate reporting applies the minimum cohort size **k = 5**; smaller groups render as
  "Below threshold" rather than a value.
- Export Report carries an explicit privacy scope step, and export activity is recorded.
- Restricted grant funding is shown as restricted and never counts toward Available.

**Still to confirm with the product owner**: approval thresholds by value, whether partially-paid
invoices and credit notes are in Phase 1, and the ROI definition — an ROI view should not ship
before what counts as a return is written down.
