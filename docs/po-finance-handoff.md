# PO Finance — Phase 1 design handoff

Satisfies QA Table 6. Figma file `1gK0GIsSnf3Efu2yXXpbrR`, page **Partner-Organizations**.
51 Finance screens in the first pass; see 1a and 1b for what the second pass added.

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

### 1a. Added in the second QA pass

New screens: **Withdrawal Submitted** (after Withdraw to Bank), **Credit Note · Invoice Adjustment**
(from the invoice list), **Ledger** and **Chart of Accounts** (from Reports and Transactions), and
**Help & Support** (sidebar, every role). Help & Support holds the explanations that used to sit on
task screens: who approves what, budget states, allowances and exceptions, escrow, funding rules
and report definitions.

### 1b. Drawers, modals and toasts (Owner)

Every one is a frame on the canvas beside the screen that opens it. Indented items are reached from
the drawer above them. Role copies exist wherever another role can open the same action; an action
the role may not take opens **This needs an Owner** instead.

```
Overview ..................... Snooze
Financials · Overview ........ Committed Funds · Pending Settlement
Escrow ....................... Release Schedule · Escrow Engagement
Wallet & Funding ............. Add Funding Source · Manage Funding Source → Remove Funding Source
                               Grant Restrictions · Copied
Top Up Wallet ................ Authorise Payment (→ Wallet Funded, or "Bank not responding?" → Outcome Unknown)
Wallet Funded ................ Download Started
Top Up — Failed .............. Bank Transfer Details · Contact Support
Top Up — Outcome Unknown ..... Saved (notify me)
Auto-reload Rules ............ Edit Auto-reload → Authorise Change · Pause Auto-reload · Disable Auto-reload
Withdraw to Bank ............. Withdrawal Destination · Confirm Withdrawal (→ Withdrawal Submitted)
Convert Currency ............. Confirm Conversion
Verify Identity · KYC ........ Upload Document · Verification Submitted
Manage Budget Pool ........... Add Funds · Reallocate Funds · Change Cap · Close Budget Pool · Procurement References
Pool Created ................. Edit Restrictions
Allowances ................... Edit Allowance Defaults
Allowance Exceptions ......... Add Exception · Exception Detail · Bulk Changes
Budget Planning .............. Set Programme Budget · Allocate Budget · Plan Next FY · Change FY Start
Approvals .................... Request Top-up · Request Refund · Request Billing Mode
                               Approve Request → Approved · Decline Request → Declined · Ask For Detail
Invoices & Seats ............. Switch To Manual · Fallback Method · Change Seats · Assign Seats → Seats Assigned
                               Release Seats · Enterprise Billing
Invoice Detail ............... Pay Invoice → Invoice Paid · Share Invoice
Dispute Invoice .............. Choose Reason · Dispute Submitted
Credit Note .................. Credit Note Issued
Transaction Detail ........... Dispute Transaction · Sessions
Refund or Reverse ............ Refund Complete
Provider Payouts ............. Payout Schedule · Record External Payment
Reconciliation ............... Import Statement · Run Reconciliation → Reconciliation Complete · Reconciliation Exception
Chart of Accounts ............ Account Detail
Cost Centres ................. Add Cost Centre · Add Country
Every screen ................. Search · Display Currency · Account Menu · Period · Export
```

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

**Decided** (see `po-finance-qa-plan.md` §10, overturnable but no longer blocking):

- **Approval thresholds** — banded by value *or* share of pool, whichever is higher. Owner above
  ₦2,000,000 or 20%; dual Owner approval above ₦10,000,000; any cap, billing or restricted-fund
  change is Owner at any value. 2 business days, then escalation.
- **Partially-paid invoices and credit notes** — both in Phase 1. A credit note always references
  its original invoice and reduces the outstanding balance rather than erasing the record.
- **ROI** — Phase 1 reports return in **outcomes, not naira**. A verified outcome is a rise of at
  least one minimal important difference (8 points) on the seven-dimension index, with both
  baseline and endpoint present. Monetised ROI is designed and **withheld** until the organisation
  supplies absence and attrition baselines; the screen states this rather than showing a zero.
- **Sample data** — the reconciled figures are the canonical design dataset v1. Internally
  consistent at every level, not the organisation's real data. Replacing the values is expected;
  the relationships must hold.
