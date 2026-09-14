# Decision log

Product and design decisions made while building the PO module, with the reasoning. Recorded so
they can be challenged rather than rediscovered.

## Terminology

**"Beneficiary", not "member" or "user".** The concept note defines the sponsored end user as a
beneficiary; the UI now matches — nav, tables, screen names, body copy. *Team member* was
deliberately left alone: it means org staff, and collapsing the two terms would hide the
distinction the privacy model depends on. Department names like "People Ops" were also left.

The Beneficiaries section's first tab is **Directory**, not "Beneficiaries", to avoid a
"Beneficiaries › Beneficiaries" breadcrumb.

## Money

**Reserved-for-seats is carved out of the wallet balance, not additional.** The reconciliation is
shown on screen because the previous design implied two different totals.

**Invoices settle automatically from available wallet funds**, with a card fallback and a 3-day
retry. Service spend never appears on an invoice — it is drawn from Project budgets as it happens.
Stated explicitly because "how do dues get settled" was a live question.

**Fees are charged on top of a top-up**, so the full requested amount reaches the wallet. The
breakdown (processing fee, VAT on fee, electronic transfer levy) is shown before confirmation, with
the resulting balance.

**An Owner increases a budget pool directly from the wallet** — there is no one to ask. Project
Managers and Finance see the same screen with *Request More Budget*, which captures amount,
justification, urgency and funding source and routes to an Owner. The previous design showed
"Request More Budget" to the Owner, which was incoherent.

**Changing organisation currency does not convert existing funds.** A second balance opens; both
stay spendable; conversion is a separate explicit action with the rate and timestamp stamped onto
the transaction. The alternative — silent conversion at an unstated rate — is the kind of thing
that destroys trust in a wallet.

**Withdrawals** go only to an account in the organisation's registered name, with a 24-hour hold
above ₦5,000,000 and a source-of-funds check. Presented as an AML control that cannot be skipped,
not as a system limitation.

**KYC follows the CBN three-tier framework.** The interface blocks and explains at the point of
action rather than letting the gateway decline.

## Privacy

**Always-private data is structurally absent**, never rendered as a locked or greyed row. A locked
row advertises that the data exists and invites pressure to unlock it.

**Widening the Privacy Dial requires re-consent** from already-enrolled beneficiaries, and the
consequence is shown before the dial moves.

**Aggregates suppress below a cohort size of 5**, and exports apply the filter *before* the file is
generated, not after. The export screen says so.

## Reporting

**One canonical figure per metric across the module.** Cost per beneficiary and cost per outcome
were quoted differently on the L1 strip and on Financials Overview; reconciled to a single set.
Where a screen's own header disagreed with a newly added panel, the header was treated as the
source of truth — it predates the addition.

**Benchmarking is against the organisation's own history**, never against other organisations. No
external benchmark is implied, because we have no basis for one.

**Deltas show losses too.** Retention down 2 points is shown in red. A dashboard where every arrow
is green does not get believed.

**Denominators are always visible.** "Cost per outcome ₦142,000" appears with "90 verified
improvements". Without the denominator the metric is unfalsifiable.

## Structure

**Allowances & Budgets was split into three views** — Budgets / Allowances / Planning — behind a
segmented control. At 3,218px it was three unrelated jobs in one scroll: live pool management,
per-beneficiary policy, and annual envelope planning.

**Detail screens lost their header metric strips** once KPI rows were added below them; the same
figures appeared twice.

**Project and Cohort detail have a Beneficiaries ⇄ Service providers toggle**, each state a real
wired screen, because those pages answer two different questions about the same unit.

**Role variants are cloned from Owner with the sidebar swapped**, never rebuilt. Divergence between
roles then only happens on purpose.

## Copy

**Text that narrates the interface was removed.** A toggle labelled *Beneficiaries | Service
providers* does not need "Switch between who is being served and who is delivering" beneath it.
Roughly 80 such lines were cut. What stays: scope, period, denominator, policy, consequence — and
the insight notes under charts, which say what the data means and what to do.

## Open questions

- Multi-currency **settlement** (as opposed to display and conversion) is not designed.
- Cohort-level retention curves are modelled on aggregate data; per-cohort curves need a data
  source decision.
- Notification preferences and the activation checklist exist in the older reference file but were
  judged to be a different feature area, not settings.
