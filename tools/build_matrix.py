# -*- coding: utf-8 -*-
"""Resolve QA items to live Figma node links and emit matrix.json + the markdown table."""
import json, re, sys, io, os, collections

FILE_KEY = "1gK0GIsSnf3Efu2yXXpbrR"
FILE_NAME = "ElevatedHere_SP_App"
ROLES = ("Owner", "Admin-Manager", "Finance-Billing", "Project Manager", "Analyst-Viewer")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qa_items as Q


def norm(s):
    """ASCII-fold, drop separators, collapse whitespace. Makes em-dash/middot names comparable."""
    s = "".join(c if ord(c) < 128 else " " for c in s)
    s = s.replace("-", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def strip_role(name):
    return re.sub(r"\s*\((?:%s)\)" % "|".join(re.escape(r) for r in ROLES), " ", name)


def link(node_id):
    return "https://www.figma.com/design/%s/%s?node-id=%s" % (
        FILE_KEY, FILE_NAME, node_id.replace(":", "-"))


def load_screens(path):
    rows = json.load(open(path))
    index = collections.defaultdict(list)
    for node_id, name, x, y, w, h in rows:
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
    missing = []
    items = []
    for iid, src, req, change, screens in Q.ITEMS:
        items.append({"id": iid, "source": src, "requirement": req,
                      "change": change, "screens": resolve(index, screens, missing)})
    decisions = [{"id": d[0], "title": d[1], "text": d[2],
                  "screens": resolve(index, d[3], missing)} for d in Q.DECISIONS]
    openq = [{"id": o[0], "title": o[1], "text": o[2], "status": o[3]} for o in Q.OPEN]

    if missing:
        print("UNRESOLVED SCREEN NAMES (%d):" % len(missing))
        for m in sorted(set(missing)):
            print("   ", m)

    linked = sum(len(i["screens"]) for i in items)
    frames = sum(len(s["variants"]) for i in items for s in i["screens"])
    data = {"file": {"key": FILE_KEY, "name": FILE_NAME,
                     "url": "https://www.figma.com/design/%s/%s?node-id=800001-227" % (FILE_KEY, FILE_NAME)},
            "items": items, "decisions": decisions, "open": openq,
            "stats": {"items": len(items), "screenRefs": linked, "frameLinks": frames,
                      "decisions": len(decisions), "open": len(openq)}}
    json.dump(data, io.open(os.path.join(out_dir, "qa-matrix.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("items %d / screen refs %d / frame links %d" % (len(items), linked, frames))
    return data


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
