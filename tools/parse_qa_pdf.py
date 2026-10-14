# -*- coding: utf-8 -*-
"""Parse the QA PDF's tables into structured rows, keeping the document's own wording.

Input: `pdftotext -table` output, which preserves column positions.

Method, per page: find the vertical gutters (column indexes blank on nearly every
*tabular* line), slice each line into cells, then start a new record on the
empty -> text transition in column 0. Cell text wraps over several lines, and the
PDF breaks words without hyphens, so fragments are re-fused on the way out.
"""
import io, re, sys, json, collections

# Header fragments, matched whole: the header row wraps, so each cell is one of
# these on its own. Anchored at both ends -- a bare "n" alternative would
# otherwise swallow every cell beginning with that letter.
_HEAD = ("#", "Area / Screen", "What is", "currently", "good", "Brutal problem",
         "Why it matters", "for PO / B2B2C /", "revenue", "Elite-level",
         "recommendatio", "n", "Design Task", "Exact Design Work", "Required",
         "Acceptance", "Criteria / UX", "Outcome", "Business /", "Product Impact",
         "currently good", "Area / Screen What is")
NOISE_EXACT = re.compile(r"^(%s)$" % "|".join(re.escape(h) for h in _HEAD), re.I)
NOISE_PREFIX = re.compile(r"^(Table \d|TABLE \d|PARTNER ORGs)", re.I)


def NOISE(s):
    return bool(NOISE_EXACT.match(s) or NOISE_PREFIX.match(s))


TABULAR = re.compile(r"\S {3,}\S")

# Fragments a soft wrap can strand at the start of the next line. Real two-letter
# words (to, of, in, is, on, by, as, at, it, ...) are deliberately absent.
SUFFIX = re.compile(r"^(ner|nts|gs|ng|nt|al|ed|es|er|le|ic|ly|ty|ve|ce|se|n|e|s|y|d|t)(\s|$)")


def gutters(lines, min_run=2, ratio=0.92):
    """Column indexes blank on >=ratio of tabular lines, in runs of >=min_run.

    Full-width prose has no gutters and would wash the signal out, so only lines
    that actually show column gaps are counted.
    """
    use = [l for l in lines if l.strip() and TABULAR.search(l)]
    if len(use) < 3:
        return []
    width = max(len(l) for l in use)
    blank = []
    for c in range(width):
        n = sum(1 for l in use if c >= len(l) or l[c] == " ")
        blank.append(n >= ratio * len(use))
    runs, start = [], None
    for c in range(width):
        if blank[c] and start is None:
            start = c
        elif not blank[c] and start is not None:
            if c - start >= min_run:
                runs.append((start, c))
            start = None
    if start is not None and width - start >= min_run:
        runs.append((start, width))
    return runs


def columns_from(lines, ncols, ratio=0.92):
    """Cut the page into ncols using the widest interior gutters."""
    tab = [l for l in lines if l.strip() and TABULAR.search(l)]
    width = max((len(l) for l in tab), default=0)
    runs = [r for r in gutters(lines, ratio=ratio) if r[0] > 0 and r[1] < width]
    if len(runs) < ncols - 1:
        return []
    runs.sort(key=lambda r: (r[1] - r[0]), reverse=True)
    cuts = sorted(int((a + b) / 2) for a, b in runs[: ncols - 1])
    return [0] + cuts + [10 ** 6]


def slice_page(lines, bounds):
    return [[l[bounds[i]:bounds[i + 1]].strip() for i in range(len(bounds) - 1)]
            for l in lines]


def page_cells(pages, ncols, adaptive=False):
    """Slice every page of one table on a single grid pooled from all its pages.

    A per-page grid goes wrong where one separator happens to be narrow on that
    page and a wider gap inside a cell wins instead; pooling every line of the
    table averages that out, because the column positions are fixed per table.

    `None` is pushed between pages so a record cannot start mid-way through one
    and swallow the first row of the next.
    """
    allLines = []
    for p in pages:
        allLines.extend(p.split("\n"))
    grid = columns_from(allLines, ncols)
    cells, last = [], grid
    for p in pages:
        lines = p.split("\n")
        if not [l for l in lines if l.strip()]:
            continue
        own = best_grid(lines, ncols) if adaptive else columns_from(lines, ncols)
        b = own or snap(grid, lines) or last
        if not b:
            continue
        last = b
        cells.extend(slice_page(lines, b))
        cells.append(None)
    return cells


def best_grid(lines, ncols):
    """Try several blankness thresholds and keep the grid that fills most cells.

    One threshold does not fit every page: a strict one misses a separator that
    a long cell bleeds into, a loose one invents separators inside a cell. The
    grid that puts text in the most columns is the one that matched the page.
    """
    best, score = None, -1
    for ratio in (0.97, 0.92, 0.86, 0.80):
        g = columns_from(lines, ncols, ratio)
        if not g:
            continue
        filled = sum(1 for row in slice_page(lines, g) for c in row if c)
        spread = len(set(i for row in slice_page(lines, g)
                         for i, c in enumerate(row) if c))
        s = spread * 1000 + filled          # cover every column first, then fill
        if s > score:
            best, score = g, s
    return best


def snap(grid, lines, tol=10):
    """Move each global cut to this page's own nearest gutter.

    Column positions shift a little from page to page. Choosing a page's cuts by
    width alone picks a wide gap inside a cell when a real separator is narrow;
    anchoring to the table's global grid and snapping locally avoids both.
    """
    if not grid:
        return None
    mids = [int((a + b) / 2) for a, b in gutters(lines)]
    if not mids:
        return None
    out = [0]
    for g in grid[1:-1]:
        near = [m for m in mids if abs(m - g) <= tol and m > out[-1]]
        out.append(min(near, key=lambda m: abs(m - g)) if near else g)
    out.append(10 ** 6)
    return out if all(out[i] < out[i + 1] for i in range(len(out) - 1)) else None


def join_frags(frags):
    """Join wrapped fragments, re-fusing words the PDF split without a hyphen."""
    out = ""
    for f in frags:
        m = SUFFIX.match(f)
        if out and m and out[-1:].islower() and len(out.split()[-1]) >= 5:
            out += m.group(1)                       # "Reconciliatio" + "n Workspace"
            rest = f[m.end(1):].strip()
            if rest:
                out += " " + rest
        else:
            out = (out + " " + f) if out else f
    return re.sub(r"\s+", " ", out).strip()


NUMBERED_START = re.compile(r"^\d{1,3}")


def assemble(cellrows, numbered=False):
    """A record starts on the empty -> text transition in column 0.

    In the numbered review table an item number is never wrapped, so a leading
    number always starts a row even when the line above also had column 0 text.
    """
    recs, cur, prev0 = [], None, False
    for cells in cellrows:
        if cells is None:                           # page boundary
            prev0 = False
            continue
        if not any(cells):
            continue
        if all(NOISE(c) for c in cells if c):
            prev0 = False
            continue
        has0 = bool(cells[0])
        if has0 and (not prev0 or (numbered and NUMBERED_START.match(cells[0]))):
            if cur:
                recs.append(cur)
            cur = [[c] for c in cells]
        elif cur:
            for i, c in enumerate(cells):
                if c:
                    cur[i].append(c)
        prev0 = has0
    if cur:
        recs.append(cur)
    return [[join_frags([p for p in col if p]) for col in r] for r in recs]


def clean(s):
    s = re.sub(r"(\w)-\s+([A-Z])", r"\1-\2", s)     # real compound: "Permission- Based"
    s = re.sub(r"(\w)-\s+([a-z])", r"\1\2", s)      # soft wrap: "reporting- period"
    s = re.sub(r"\s+([,.;:)])", r"\1", s)
    s = s.replace("", " ").replace("→", " → ")
    return re.sub(r"\s+", " ", s).strip()


def main(path, outp):
    pages = io.open(path, encoding="utf-8", errors="replace").read().split("\f")
    fin_start = next(i for i, p in enumerate(pages) if "PARTNER ORGs - FINANCE" in p)
    t2_start = next(i for i, p in enumerate(pages) if "COMPREHENSIVE IMPROVEMENT" in p)
    # the review table ends where the narrative sections begin
    prog_end = next(i for i, p in enumerate(pages) if "BIGGEST PRODUC" in p) + 1

    # Split pages at every "Table N --" heading: a heading sits mid-page, and the
    # rows above it belong to the previous table while the wide heading line also
    # destroys the column grid if left in place.
    HEAD = re.compile(r"^\s*Table (\d) [-–—]+ (.+)$")
    segments = collections.OrderedDict()
    current = None
    for i, pg in enumerate(pages):
        if i < fin_start:
            continue
        lines = pg.split("\n")
        start = 0
        for j, l in enumerate(lines):
            m = HEAD.match(l)
            if not m:
                continue
            if current:
                segments[current].append(lines[start:j])
            current = "Table %s — %s" % (m.group(1), re.sub(r"\s+", " ", m.group(2)).strip())
            segments.setdefault(current, [])
            start = j + 1
        if current:
            segments[current].append(lines[start:])

    result = {"programs": [], "finance": collections.OrderedDict()}

    # --- Programs / Projects / Cohorts review table: 6 columns, numbered ---
    seen = set()
    for rec in assemble(page_cells(pages[0:prog_end], 6, adaptive=True), numbered=True):
        m = re.match(r"^(\d{1,3})\s*(.*)$", rec[0])
        if not m:
            continue
        if sum(1 for c in rec[1:] if NOISE(c)) >= 3:
            continue        # the repeated header row; "Good" alone is a real value
        if int(m.group(1)) in seen:
            continue        # a numbered prose heading after the table
        seen.add(int(m.group(1)))
        area = rec[1]
        if m.group(2):                              # grid merged the # and Area columns
            area = (m.group(2) + " " + area).strip()
        result["programs"].append({
            "n": int(m.group(1)), "area": clean(area), "good": clean(rec[2]),
            "problem": clean(rec[3]), "why": clean(rec[4]), "rec": clean(rec[5])})

    # --- Finance tables: 4 columns, rows named by their Design Task ---
    for nm, segs in segments.items():
        rows = []
        for rec in assemble(page_cells(["\n".join(sg) for sg in segs], 4)):
            task = clean(rec[0])
            if not task or NOISE(task) or "PARTNER ORGs" in task or re.match(r"Table \d", task):
                continue
            rows.append({"task": task, "work": clean(rec[1]),
                         "accept": clean(rec[2]), "impact": clean(rec[3])})
        result["finance"][nm] = rows

    # Two rows sit on pages whose grid the extractor cannot recover (a one-line row
    # at the foot of a page that is otherwise prose). Transcribed from the PDF text.
    for r in result["programs"]:
        if r["n"] == 58:
            r.update(good="Strong foundation",
                     problem="Currently more like an analytics dashboard than a "
                             "program-management operating system",
                     why="It does not yet fully support the PO lifecycle",
                     rec="Evolve into Program → Project → Cohort → Delivery "
                         "→ Finance → Outcomes operating model")
        if r["n"] == 26:
            r["area"] = "Q3 project: 91% consumed"

    json.dump(result, io.open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("programs rows:", len(result["programs"]),
          sorted(r["n"] for r in result["programs"]))
    for k, v in result["finance"].items():
        print("  %-66s %d rows" % (k[:66], len(v)))
    print("finance total:", sum(len(v) for v in result["finance"].values()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
