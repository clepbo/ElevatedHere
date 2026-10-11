# -*- coding: utf-8 -*-
"""Emit docs/po-qa-traceability.md from qa-matrix.json."""
import json, io, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(io.open(os.path.join(HERE, "qa-matrix.json"), encoding="utf-8"))

GROUPS = [
    ("Finance QA — Table 1: balance model and Finance Overview", "F1"),
    ("Finance QA — Table 2: budgets, allowances, approvals", "F2"),
    ("Finance QA — Table 3: invoices, seats, transactions, accounting", "F3"),
    ("Finance QA — Table 4: reports, programme economics, ROI", "F4"),
    ("Finance QA — Table 5: enterprise readiness, roles, states", "F5"),
    ("Finance QA — Table 6: handoff and acceptance", "F6"),
    ("Programs / Projects / Cohorts QA — P0", "P0"),
    ("Programs / Projects / Cohorts QA — P1", "P1"),
    ("Programs / Projects / Cohorts QA — P2", "P2"),
]

def role_of(name):
    for r in ("Owner", "Admin-Manager", "Finance-Billing", "Project Manager", "Analyst-Viewer"):
        if "(%s)" % r in name:
            return r
    return "Shared"

def links_for(screens):
    if not screens:
        return "_documentation deliverable — no screen_"
    parts = []
    for s in screens:
        vs = s["variants"]
        label = s["screen"].replace("PO - ", "").replace("PO-", "PO-")
        tags = " ".join("[%s](%s)" % (role_of(v["name"]), v["url"]) for v in vs)
        parts.append("**%s** %s" % (label, tags))
    return "<br>".join(parts)

out = []
w = out.append
w("# PO QA — traceability matrix")
w("")
w("Every item raised in the two QA documents, the decision taken, and a direct link to each Figma")
w("frame where it was resolved. Role labels after a screen name are links to that role's variant.")
w("")
w("Figma file: [%s](%s) · page **Partner-Organizations**." % (D["file"]["name"], D["file"]["url"]))
w("")
s = D["stats"]
w("**%d QA items** · %d screen references · **%d frame links** · %d decisions recorded · %d items awaiting your call."
  % (s["items"], s["screenRefs"], s["frameLinks"], s["decisions"], s["open"]))
w("")
w("> The generated source of this table is `tools/qa_items.py` plus `tools/build_matrix.py`; re-run")
w("> it against a fresh screen index if node IDs change.")
w("")
w("---")
w("")

by = collections.defaultdict(list)
for it in D["items"]:
    by[it["id"].split(".")[0]].append(it)

for title, key in GROUPS:
    rows = by.get(key, [])
    if not rows:
        continue
    w("## %s" % title)
    w("")
    w("| # | What the QA asked for | Decision and what changed | Where it lives |")
    w("|---|---|---|---|")
    for it in rows:
        w("| **%s** | %s | %s | %s |" % (it["id"], it["requirement"], it["change"], links_for(it["screens"])))
    w("")

w("---")
w("")
w("## Decisions recorded")
w("")
w("Four of these were open questions the product owner asked me to settle. All are overturnable —")
w("what could not stand was a screen built on an undefined term.")
w("")
w("| # | Decision | What was settled | Where it shows |")
w("|---|---|---|---|")
for d in D["decisions"]:
    w("| **%s** | %s | %s | %s |" % (d["id"], d["title"], d["text"], links_for(d["screens"])))
w("")
w("---")
w("")
w("## Still needs your call")
w("")
w("| # | Item | Detail | Status |")
w("|---|---|---|---|")
for o in D["open"]:
    w("| **%s** | %s | %s | %s |" % (o["id"], o["title"], o["text"], o["status"]))
w("")
w("---")
w("")
w("## Coverage note")
w("")
w("150 of the 176 screens on the page are referenced above. The 26 that are not were outside the")
w("scope of both QA documents — sign-up, sign-in, OTP, password reset, the beneficiary directory and")
w("engagement screens, add-beneficiary, the provider panel and marketplace, and provider-engaged.")
w("They were still changed by item **P0.15**, which rebuilt the side navigation on every frame that")
w("has one; the links on that row are representative rather than exhaustive.")
w("")

io.open(os.path.join(HERE, "..", "docs", "po-qa-traceability.md"), "w", encoding="utf-8").write("\n".join(out))
print("wrote docs/po-qa-traceability.md", len("\n".join(out)), "chars")
