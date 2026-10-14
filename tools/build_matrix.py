# -*- coding: utf-8 -*-
"""Join the verbatim QA items to what was built, and resolve live Figma links.

    python build_matrix.py screens.json .

`qa-source.json` holds the QA document's own wording (see parse_qa_pdf.py).
`qa_map.py` holds what changed and where. Nothing restates a requirement.
"""
import json, re, sys, io, os, collections

FILE_KEY = "1gK0GIsSnf3Efu2yXXpbrR"
FILE_NAME = "ElevatedHere_SP_App"
ROLES = ("Owner", "Admin-Manager", "Finance-Billing", "Project Manager", "Analyst-Viewer")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qa_map as M


def norm(s):
    s = "".join(c if ord(c) < 128 else " " for c in s)
    return re.sub(r"\s+", " ", s.replace("-", " ")).strip().lower()


def strip_role(name):
    return re.sub(r"\s*\((?:%s)\)" % "|".join(re.escape(r) for r in ROLES), " ", name)


def link(node_id):
    return "https://www.figma.com/design/%s/%s?node-id=%s" % (
        FILE_KEY, FILE_NAME, node_id.replace(":", "-"))


def load_screens(path):
    index = collections.defaultdict(list)
    for node_id, name, x, y, w, h in json.load(io.open(path, encoding="utf-8")):
        index[norm(strip_role(name))].append({"id": node_id, "name": name, "url": link(node_id)})
    for k in index:
        index[k].sort(key=lambda s: s["name"])
    return index


def resolve(index, wanted, missing):
    out = []
    for w in wanted:
        hits = index.get(norm(w))
        if not hits:
            missing.append(w)
            continue
        out.append({"screen": w, "variants": hits})
    return out


def main(screens_path, out_dir):
    index = load_screens(screens_path)
    src = json.load(io.open(os.path.join(HERE, "qa-source.json"), encoding="utf-8"))
    missing, unmapped, items = [], [], []

    for n, title, req, change, screens in M.EXTRA:
        items.append({"id": n, "group": "PO", "table": title, "ref": "",
                      "requirement": req, "change": change,
                      "screens": resolve(index, screens, missing)})

    for r in src["programs"]:
        hit = M.PROGRAMS.get(r["n"])
        if not hit:
            unmapped.append("programs #%d" % r["n"])
        req = r["problem"]
        items.append({
            "id": str(r["n"]), "group": "PROG",
            "table": "Programs, Projects and Cohorts — review table",
            "ref": r["area"], "requirement": req,
            "good": r["good"], "why": r["why"], "recommendation": r["rec"],
            "change": hit[0] if hit else "",
            "screens": resolve(index, hit[1], missing) if hit else []})

    for table, rows in src["finance"].items():
        for r in rows:
            hit = M.FINANCE.get(r["task"])
            if not hit:
                unmapped.append(r["task"])
            items.append({
                "id": r["task"], "group": "FIN", "table": table, "ref": r["task"],
                "requirement": r["work"], "accept": r["accept"], "impact": r["impact"],
                "change": hit[0] if hit else "",
                "screens": resolve(index, hit[1], missing) if hit else []})

    decisions = [{"id": d[0], "title": d[1], "text": d[2],
                  "screens": resolve(index, d[3], missing)} for d in M.DECISIONS]
    openq = [{"id": o[0], "title": o[1], "text": o[2], "status": o[3]} for o in M.OPEN]

    if missing:
        print("UNRESOLVED SCREEN NAMES (%d):" % len(set(missing)))
        for m in sorted(set(missing)):
            print("   ", m)
    if unmapped:
        print("QA ITEMS WITH NO MAPPING (%d):" % len(unmapped))
        for u in unmapped:
            print("   ", u)

    frames = sum(len(s["variants"]) for i in items for s in i["screens"])
    data = {"file": {"key": FILE_KEY, "name": FILE_NAME,
                     "url": "https://www.figma.com/design/%s/%s?node-id=800001-227" % (FILE_KEY, FILE_NAME)},
            "items": items, "decisions": decisions, "open": openq,
            "stats": {"items": len(items),
                      "screenRefs": sum(len(i["screens"]) for i in items),
                      "frameLinks": frames, "decisions": len(decisions), "open": len(openq)}}
    json.dump(data, io.open(os.path.join(out_dir, "qa-matrix.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("items %d / screen refs %d / frame links %d"
          % (len(items), data["stats"]["screenRefs"], frames))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
