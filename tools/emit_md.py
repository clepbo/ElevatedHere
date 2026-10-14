# -*- coding: utf-8 -*-
"""Emit docs/po-qa-traceability.md from qa-matrix.json, keeping the QA wording."""
import json, io, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(io.open(os.path.join(HERE, "qa-matrix.json"), encoding="utf-8"))
ROLE = {"Owner": "Owner", "Admin-Manager": "Admin", "Finance-Billing": "Finance",
        "Project Manager": "PM", "Analyst-Viewer": "Analyst", "Shared": "Shared"}


def role_of(name):
    for r in ("Owner", "Admin-Manager", "Finance-Billing", "Project Manager", "Analyst-Viewer"):
        if "(%s)" % r in name:
            return r
    return "Shared"


def links(screens):
    if not screens:
        return "_documentation deliverable_"
    out = []
    for s in screens:
        label = s["screen"][5:] if s["screen"].startswith("PO - ") else s["screen"]
        tags = " ".join("[%s](%s)" % (ROLE[role_of(v["name"])], v["url"]) for v in s["variants"])
        out.append("**%s** %s" % (label, tags))
    return "<br>".join(out)


def esc(s):
    return (s or "").replace("|", "\\|")


out = []
w = out.append
s = D["stats"]
w("# PO QA — traceability matrix")
w("")
w("Every item from the two QA documents, **in the document's own words and order**, with what was")
w("decided, what changed, and a direct link to each Figma frame where it was resolved. Role labels")
w("after a screen name link to that role's variant.")
w("")
w("Figma file: [%s](%s) · page **Partner-Organizations**." % (D["file"]["name"], D["file"]["url"]))
w("")
w("**%d QA items** · %d screen references · **%d frame links** · %d decisions · %d awaiting your call."
  % (s["items"], s["screenRefs"], s["frameLinks"], s["decisions"], s["open"]))
w("")
w("> Requirement text is extracted verbatim from `PO - Finance QA.pdf` by `tools/parse_qa_pdf.py`.")
w("> What changed and where it lives is in `tools/qa_map.py`. Neither restates the other.")
w("")
w("---")
w("")

by = collections.OrderedDict()
for it in D["items"]:
    by.setdefault(it["table"], []).append(it)

for table, rows in by.items():
    w("## %s" % table)
    w("")
    if rows[0]["group"] == "PROG":
        w("Columns as the QA document has them: the problem it raises, why it says it matters, and its")
        w("recommendation — then what was done.")
        w("")
        w("| # | Area / Screen | Brutal problem | Why it matters | Elite-level recommendation | What changed | Where it lives |")
        w("|---|---|---|---|---|---|---|")
        for it in rows:
            w("| **%s** | %s | %s | %s | %s | %s | %s |" % (
                it["id"], esc(it["ref"]), esc(it["requirement"]), esc(it.get("why", "")),
                esc(it.get("recommendation", "")), esc(it["change"]), links(it["screens"])))
    elif rows[0]["group"] == "PO":
        w("| # | What was asked | What changed | Where it lives |")
        w("|---|---|---|---|")
        for it in rows:
            w("| **%s** | %s | %s | %s |" % (it["id"], esc(it["requirement"]),
                                             esc(it["change"]), links(it["screens"])))
    else:
        w("| Design Task | Exact Design Work Required | Acceptance Criteria / UX Outcome | What changed | Where it lives |")
        w("|---|---|---|---|---|")
        for it in rows:
            w("| **%s** | %s | %s | %s | %s |" % (
                esc(it["ref"]), esc(it["requirement"]), esc(it.get("accept", "")),
                esc(it["change"]), links(it["screens"])))
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
    w("| **%s** | %s | %s | %s |" % (d["id"], esc(d["title"]), esc(d["text"]), links(d["screens"])))
w("")
w("## Still needs your call")
w("")
w("| # | Item | Detail | Status |")
w("|---|---|---|---|")
for o in D["open"]:
    w("| **%s** | %s | %s | %s |" % (o["id"], esc(o["title"]), esc(o["text"]), o["status"]))
w("")
w("---")
w("")
w("## Notes on the source")
w("")
w("- The review table is numbered **1–58** in the PDF, but **3, 33, 54 and 55 do not exist**:")
w("  the numbering skips them, and row 3 contains only a repeated table header. 54 real items.")
w("- Items **57 and 56 appear in that order** in the document; the order here matches the document.")
w("- Two rows (**26** and **58**) sit on pages whose column grid cannot be recovered automatically")
w("  and were transcribed by hand from the PDF text; this is marked in `parse_qa_pdf.py`.")
w("- The two **PO** rows are the product owner's instructions from this engagement, which are not")
w("  numbered in the QA document.")

io.open(os.path.join(HERE, "..", "docs", "po-qa-traceability.md"), "w", encoding="utf-8").write("\n".join(out))
print("wrote docs/po-qa-traceability.md", len("\n".join(out)), "chars")
