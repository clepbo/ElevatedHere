# -*- coding: utf-8 -*-
"""Emit the QA sign-off register page from qa-matrix.json."""
import json, io, os, html, collections

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(io.open(os.path.join(HERE, "qa-matrix.json"), encoding="utf-8"))

GROUPS = [
    ("F1", "Table 1", "Balance model and Finance Overview", "pp. 37-46"),
    ("F2", "Table 2", "Budgets, allowances, approvals", "pp. 46-54"),
    ("F3", "Table 3", "Invoices, seats, transactions, accounting", "pp. 55-64"),
    ("F4", "Table 4", "Reports, programme economics, ROI", "pp. 64-71"),
    ("F5", "Table 5", "Enterprise readiness, roles, states", "pp. 72-79"),
    ("F6", "Table 6", "Handoff and acceptance", "pp. 79-81"),
    ("P0", "P0", "Programs, projects and cohorts — blocking", "pp. 1-36"),
    ("P1", "P1", "Programs, projects and cohorts — important", "pp. 1-36"),
    ("P2", "P2", "Programs, projects and cohorts — enhancement", "pp. 1-36"),
]
ROLE_SHORT = {"Owner": "Owner", "Admin-Manager": "Admin", "Finance-Billing": "Finance",
              "Project Manager": "PM", "Analyst-Viewer": "Analyst", "Shared": "Shared"}


def role_of(name):
    for r in ("Owner", "Admin-Manager", "Finance-Billing", "Project Manager", "Analyst-Viewer"):
        if "(%s)" % r in name:
            return r
    return "Shared"


def e(s):
    return html.escape(s, quote=True)


def screen_block(s):
    label = s["screen"]
    for p in ("PO - ", "PO-"):
        if label.startswith(p):
            label = label[len(p):] if p == "PO - " else label
    links = "".join(
        '<a class="role" href="%s" target="_blank" rel="noopener">%s</a>'
        % (v["url"], e(ROLE_SHORT[role_of(v["name"])])) for v in s["variants"])
    return '<span class="screen"><span class="sname">%s</span>%s</span>' % (e(label), links)


rows = []
by = collections.defaultdict(list)
for it in D["items"]:
    by[it["id"].split(".")[0]].append(it)

for key, tag, title, pages in GROUPS:
    items = by.get(key, [])
    if not items:
        continue
    rows.append('<section class="group" data-group="%s">' % key)
    rows.append('<header class="ghead"><h2>%s</h2><p>%s</p><span class="pages">%s</span>'
                '<span class="gcount" data-gcount="%s"></span></header>' % (e(tag), e(title), e(pages), key))
    for it in items:
        search = " ".join([it["id"], it["requirement"], it["change"]] +
                          [s["screen"] for s in it["screens"]]).lower()
        screens = ("".join(screen_block(s) for s in it["screens"])
                   if it["screens"] else '<span class="nolink">documentation deliverable</span>')
        rows.append(
            '<article class="item" data-id="%s" data-group="%s" data-search="%s">'
            '<div class="col-id"><span class="iid">%s</span><span class="src">%s</span></div>'
            '<div class="col-main"><p class="req">%s</p>'
            '<p class="chg"><span class="clabel">Changed</span>%s</p>'
            '<div class="links">%s</div></div>'
            '<div class="col-sign">'
            '<button class="sbtn v" data-act="verified" type="button">Verified</button>'
            '<button class="sbtn f" data-act="flagged" type="button">Flag</button>'
            '<p class="who" data-who="%s"></p></div></article>'
            % (e(it["id"]), e(it["id"].split(".")[0]), e(search), e(it["id"]), e(it["source"]),
               e(it["requirement"]), e(it["change"]), screens, e(it["id"])))
    rows.append("</section>")

dec = "".join(
    '<article class="dec"><div class="col-id"><span class="iid">%s</span></div>'
    '<div class="col-main"><p class="req">%s</p><p class="chg">%s</p>'
    '<div class="links">%s</div></div></article>'
    % (e(d["id"]), e(d["title"]), e(d["text"]),
       "".join(screen_block(s) for s in d["screens"]))
    for d in D["decisions"])

openq = "".join(
    '<article class="dec open"><div class="col-id"><span class="iid">%s</span></div>'
    '<div class="col-main"><p class="req">%s</p><p class="chg">%s</p>'
    '<p class="status">%s</p></div></article>'
    % (e(o["id"]), e(o["title"]), e(o["text"]), e(o["status"])) for o in D["open"])

s = D["stats"]
PAGE = u"""<title>ElevatedHere QA Register</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
/* Layout: a sticky filter rail over grouped register rows; id rail left, sign-off right. */
:root {
  --bg:#f6f8f5; --surface:#ffffff; --surface-2:#f0f3ef;
  --ink:#15181a; --muted:#5d645f; --faint:#878e89;
  --line:#e0e5df; --line-2:#cdd4cc;
  --accent:#098e2d; --accent-soft:#e7f3ea;
  --warn:#9a5208; --warn-soft:#fbf0dd;
  --sans:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#0e110f; --surface:#151916; --surface-2:#1b201c;
    --ink:#e7ebe7; --muted:#9ba39d; --faint:#79817b;
    --line:#242a25; --line-2:#333b34;
    --accent:#4cbd6c; --accent-soft:#16291b;
    --warn:#e2a04a; --warn-soft:#2b2113;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg:#0e110f; --surface:#151916; --surface-2:#1b201c;
  --ink:#e7ebe7; --muted:#9ba39d; --faint:#79817b;
  --line:#242a25; --line-2:#333b34;
  --accent:#4cbd6c; --accent-soft:#16291b;
  --warn:#e2a04a; --warn-soft:#2b2113;
  color-scheme: dark;
}
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font-family: var(--sans); line-height:1.5; }
.wrap { max-width: 1180px; margin-inline:auto; padding-inline:16px; padding-block: 28px 72px; }
a { color: inherit }
h1 { font-size: clamp(22px,3.4vw,30px); line-height:1.2; margin:0 0 6px; letter-spacing:-.015em;
     font-weight:600; text-wrap:balance; }
.lede { color: var(--muted); margin:0; max-width:62ch; font-size:14px; }
.filebar { margin-top:14px; display:flex; flex-wrap:wrap; gap:8px; align-items:center; font-size:12.5px; }
.filebar a { color: var(--accent); font-weight:500; text-decoration:none; border-bottom:1px solid currentColor; }
.filebar .dot { color: var(--faint) }

.stats { display:flex; flex-wrap:wrap; gap:10px; margin:22px 0 0; }
.stat { background:var(--surface); border:1px solid var(--line); border-radius:10px;
        padding:10px 14px; flex:1 1 130px; min-width:0; }
.stat b { display:block; font-size:20px; font-weight:600; font-variant-numeric:tabular-nums; }
.stat span { font-size:11.5px; color:var(--muted); text-transform:uppercase; letter-spacing:.055em; }

.rail { position:sticky; top:env(safe-area-inset-top, 0px); z-index:5; margin:20px 0 0;
        background:var(--bg); padding-block:10px; border-bottom:1px solid var(--line); }
.rail-in { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
input[type=search] { flex:1 1 220px; min-width:0; font:inherit; font-size:13.5px; color:var(--ink);
  background:var(--surface); border:1px solid var(--line-2); border-radius:8px; padding:8px 11px; }
input[type=search]:focus-visible, .chip:focus-visible, .sbtn:focus-visible, .filebar a:focus-visible
  { outline:2px solid var(--accent); outline-offset:2px; }
.chip { font:inherit; font-size:12.5px; cursor:pointer; background:var(--surface);
  color:var(--muted); border:1px solid var(--line-2); border-radius:999px; padding:6px 12px; }
.chip[aria-pressed="true"] { background:var(--accent); border-color:var(--accent); color:#fff; font-weight:500 }
.prog { display:flex; align-items:center; gap:10px; width:100%; margin-top:4px; font-size:12.5px; color:var(--muted) }
.track { flex:1; height:6px; border-radius:3px; background:var(--surface-2); overflow:hidden; min-width:0 }
.fill { height:100%; width:0; background:var(--accent); border-radius:3px; transition:width .25s ease }
.cnt { font-variant-numeric:tabular-nums; white-space:nowrap }

.group { margin-top:34px }
.group[hidden] { display:none }
.ghead { display:flex; flex-wrap:wrap; align-items:baseline; gap:8px 12px; padding-bottom:9px;
         border-bottom:2px solid var(--ink); margin-bottom:2px }
.ghead h2 { font-size:13px; margin:0; font-weight:600; letter-spacing:.07em; text-transform:uppercase }
.ghead p { margin:0; font-size:14px; color:var(--ink); flex:1 1 220px; min-width:0 }
.pages, .gcount { font-family:var(--mono); font-size:11.5px; color:var(--faint) }

.item, .dec { display:grid; grid-template-columns: 104px minmax(0,1fr) 128px; gap:18px;
  padding:17px 0; border-bottom:1px solid var(--line); align-items:start }
.dec { grid-template-columns: 104px minmax(0,1fr) }
.item[hidden] { display:none }
.col-id { display:flex; flex-direction:column; gap:3px; min-width:0 }
.iid { font-family:var(--mono); font-size:13px; font-weight:500; color:var(--accent) }
.src { font-size:11px; color:var(--faint); line-height:1.35 }
.col-main { min-width:0 }
.req { margin:0 0 7px; font-size:14.5px; }
.chg { margin:0 0 10px; font-size:13px; color:var(--muted); }
.clabel { display:inline-block; font-size:10px; font-weight:600; letter-spacing:.07em;
  text-transform:uppercase; color:var(--faint); border:1px solid var(--line-2);
  border-radius:4px; padding:1px 5px; margin-right:7px; vertical-align:1px }
.links { display:flex; flex-wrap:wrap; gap:7px }
.screen { display:inline-flex; flex-wrap:wrap; align-items:center; gap:5px; background:var(--surface);
  border:1px solid var(--line); border-radius:8px; padding:4px 7px 4px 9px; max-width:100% }
.sname { font-size:12px; font-weight:500; min-width:0 }
.role { font-family:var(--mono); font-size:10.5px; text-decoration:none; color:var(--accent);
  background:var(--accent-soft); border-radius:5px; padding:2px 6px; white-space:nowrap }
.role:hover { background:var(--accent); color:#fff }
.nolink { font-size:12px; color:var(--faint); font-style:italic }

.col-sign { display:flex; flex-direction:column; gap:6px; align-items:stretch }
.sbtn { font:inherit; font-size:12px; cursor:pointer; border-radius:7px; padding:6px 8px;
  background:var(--surface); border:1px solid var(--line-2); color:var(--muted) }
.sbtn[aria-pressed="true"].v { background:var(--accent); border-color:var(--accent); color:#fff; font-weight:500 }
.sbtn[aria-pressed="true"].f { background:var(--warn-soft); border-color:var(--warn); color:var(--warn); font-weight:500 }
.sbtn[disabled] { opacity:.45; cursor:default }
.who { margin:0; font-size:10.5px; color:var(--faint); line-height:1.35; min-height:1em }
.item.is-verified { background:linear-gradient(90deg, var(--accent-soft), transparent 42%) }
.item.is-flagged  { background:linear-gradient(90deg, var(--warn-soft), transparent 42%) }

.panel { margin-top:44px }
.panel > h2 { font-size:17px; margin:0 0 4px; font-weight:600; letter-spacing:-.01em }
.panel > p.sub { margin:0 0 14px; color:var(--muted); font-size:13.5px; max-width:62ch }
.dec.open .status { margin:8px 0 0; font-size:11.5px; font-weight:500; color:var(--warn);
  background:var(--warn-soft); display:inline-block; padding:3px 8px; border-radius:6px }
.foot { margin-top:40px; padding-top:16px; border-top:1px solid var(--line);
  font-size:12.5px; color:var(--muted); max-width:70ch }
.note { font-size:12.5px; color:var(--muted); background:var(--surface); border:1px solid var(--line);
  border-left:3px solid var(--accent); border-radius:8px; padding:11px 14px; margin-top:14px; max-width:78ch }
@media (max-width:760px) {
  .item, .dec { grid-template-columns:1fr; gap:10px }
  .col-sign { flex-direction:row }
  .sbtn { flex:1 }
  .who { flex-basis:100%; }
}
@media (prefers-reduced-motion: reduce) { * { transition:none !important } }
</style>

<div class="wrap">
  <h1>ElevatedHere QA register</h1>
  <p class="lede">Every item raised in the two QA documents, the decision taken, and a direct link to
  each Figma frame where it was resolved. Mark an item verified or flag it &mdash; the marks are shared
  with everyone who opens this page.</p>
  <p class="filebar"><a href="__FILEURL__" target="_blank" rel="noopener">Open the Figma file</a>
    <span class="dot">&middot;</span> page Partner-Organizations
    <span class="dot">&middot;</span> __FRAMES__ frame links, all resolved against the live canvas</p>

  <div class="stats">
    <div class="stat"><b>__ITEMS__</b><span>QA items</span></div>
    <div class="stat"><b>__SCREENREFS__</b><span>screen references</span></div>
    <div class="stat"><b>__DECISIONS__</b><span>decisions recorded</span></div>
    <div class="stat"><b>__OPEN__</b><span>awaiting your call</span></div>
  </div>

  <div class="rail">
    <div class="rail-in">
      <input type="search" id="q" placeholder="Search requirement, change or screen" aria-label="Search">
      <button class="chip" id="c-all" data-filter="all" aria-pressed="true" type="button">All</button>
      <button class="chip" id="c-fin" data-filter="F" aria-pressed="false" type="button">Finance</button>
      <button class="chip" id="c-prog" data-filter="P" aria-pressed="false" type="button">Programs</button>
      <button class="chip" id="c-todo" data-filter="unmarked" aria-pressed="false" type="button">Not yet checked</button>
      <button class="chip" id="c-flag" data-filter="flagged" aria-pressed="false" type="button">Flagged</button>
      <div class="prog">
        <span class="track"><span class="fill" id="fill"></span></span>
        <span class="cnt" id="cnt">&mdash;</span>
      </div>
    </div>
  </div>

  <div id="list">
__ROWS__
  </div>

  <section class="panel">
    <h2>Decisions recorded</h2>
    <p class="sub">Four of these were open questions the product owner asked me to settle. All are
    overturnable &mdash; what could not stand was a screen built on an undefined term.</p>
    __DEC__
  </section>

  <section class="panel">
    <h2>Still needs your call</h2>
    <p class="sub">Nothing here blocks the design. Each one changes the file if you decide differently.</p>
    __OPENQ__
  </section>

  <p class="note"><b>Coverage.</b> 150 of the 176 screens on the page are linked above. The 26 that are
  not were outside the scope of both QA documents &mdash; sign-up, sign-in, OTP, password reset, the
  beneficiary directory and engagement screens, add-beneficiary, the provider panel and marketplace,
  and provider-engaged. They were still changed by item <b>P0.15</b>, which rebuilt the side navigation
  on every frame that has one, so the links on that row are representative rather than exhaustive.</p>

  <p class="foot">Generated from <span style="font-family:var(--mono);font-size:12px">tools/qa_items.py</span>
  in the ElevatedHere docs repository, resolved against a live index of the Figma page. Re-run it if node
  IDs change. Figures throughout the design are the reconciled design dataset, not the organisation's
  real data &mdash; see decision D1.</p>
</div>

<script>
(function () {
  var list = document.getElementById('list');
  var items = Array.prototype.slice.call(list.querySelectorAll('.item'));
  var groups = Array.prototype.slice.call(list.querySelectorAll('.group'));
  var q = document.getElementById('q');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var fill = document.getElementById('fill'), cnt = document.getElementById('cnt');
  var state = {};          // id -> {status, by, at}
  var names = {};          // userId -> display name
  var filter = 'all';
  var db = null, me = null, canWrite = false;

  function draft() { try { return JSON.parse(localStorage.getItem('qa-ui') || '{}'); } catch (e) { return {}; } }
  function saveDraft(o) { try { localStorage.setItem('qa-ui', JSON.stringify(o)); } catch (e) {} }

  function apply() {
    var term = q.value.trim().toLowerCase();
    items.forEach(function (el) {
      var id = el.dataset.id, st = (state[id] || {}).status || '';
      var okF = filter === 'all'
        || (filter === 'unmarked' && !st)
        || (filter === 'flagged' && st === 'flagged')
        || (filter.length === 1 && id.charAt(0) === filter);
      var okQ = !term || el.dataset.search.indexOf(term) !== -1;
      el.hidden = !(okF && okQ);
    });
    groups.forEach(function (g) {
      var vis = g.querySelectorAll('.item:not([hidden])').length;
      var all = g.querySelectorAll('.item').length;
      g.hidden = vis === 0;
      var c = g.querySelector('[data-gcount]');
      var done = 0;
      Array.prototype.forEach.call(g.querySelectorAll('.item'), function (el) {
        if ((state[el.dataset.id] || {}).status === 'verified') done++;
      });
      c.textContent = done + '/' + all + ' verified';
    });
    var v = 0, f = 0;
    items.forEach(function (el) {
      var st = (state[el.dataset.id] || {}).status;
      if (st === 'verified') v++; else if (st === 'flagged') f++;
    });
    fill.style.width = (items.length ? (v / items.length * 100) : 0) + '%';
    cnt.textContent = v + ' of ' + items.length + ' verified' + (f ? ' \\u00b7 ' + f + ' flagged' : '');
    saveDraft({ q: q.value, filter: filter });
  }

  function paint(id) {
    var el = list.querySelector('.item[data-id="' + id + '"]');
    if (!el) return;
    var rec = state[id] || {}, st = rec.status || '';
    el.classList.toggle('is-verified', st === 'verified');
    el.classList.toggle('is-flagged', st === 'flagged');
    Array.prototype.forEach.call(el.querySelectorAll('.sbtn'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.act === st));
      b.disabled = !canWrite;
    });
    var who = el.querySelector('.who');
    if (!st) { who.textContent = ''; return; }
    var nm = rec.by ? (names[rec.by] || '') : '';
    var when = '';
    if (rec.at) { try { when = new Date(rec.at).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }); } catch (e) {} }
    who.textContent = (st === 'verified' ? 'Verified' : 'Flagged') +
      (nm ? ' by ' + nm : '') + (when ? ' \\u00b7 ' + when : '');
  }

  function paintAll() { items.forEach(function (el) { paint(el.dataset.id); }); apply(); }

  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      filter = c.dataset.filter;
      chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
      apply();
    });
  });
  q.addEventListener('input', apply);

  list.addEventListener('click', function (ev) {
    var b = ev.target.closest ? ev.target.closest('.sbtn') : null;
    if (!b || b.disabled) return;
    var el = b.closest('.item'), id = el.dataset.id;
    var cur = (state[id] || {}).status || '';
    var next = cur === b.dataset.act ? '' : b.dataset.act;
    var rec = { status: next, by: me || '', at: new Date().toISOString() };
    state[id] = rec; paint(id); apply();
    if (!db) return;
    var doc = db.collection('signoff').doc(id);
    (next ? doc.set(rec) : doc.delete()).catch(function () {
      state[id] = { status: cur }; paint(id); apply();
    });
  });

  var d = draft();
  if (d.q) q.value = d.q;
  if (d.filter) {
    var hit = chips.filter(function (c) { return c.dataset.filter === d.filter; })[0];
    if (hit) { filter = d.filter; chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === hit)); }); }
  }
  paintAll();

  (async function () {
    if (!window.claude || !window.claude.use) return;
    var user = await window.claude.use('user');
    db = await window.claude.use('db');
    if (user) {
      try { me = await user.id(); } catch (e) {}
      try { canWrite = user.can ? (user.can('data.write') !== false) : true; } catch (e) { canWrite = true; }
    }
    if (!db) { paintAll(); return; }
    db.collection('signoff').onSnapshot(function (snap) {
      var next = {}, ids = [];
      snap.forEach(function (doc) {
        var v = doc.data() || {};
        next[doc.id] = v;
        if (v.by && ids.indexOf(v.by) === -1) ids.push(v.by);
      });
      state = next;
      if (user && user.profiles && ids.length) {
        user.profiles(ids).then(function (ps) {
          ids.forEach(function (i) { names[i] = (ps[i] && ps[i].name) || ''; });
          paintAll();
        }).catch(function () { paintAll(); });
      } else { paintAll(); }
    }, function () { paintAll(); });
    paintAll();
  })();
})();
</script>
"""

PAGE = (PAGE.replace("__ROWS__", "\n".join(rows))
            .replace("__DEC__", dec)
            .replace("__OPENQ__", openq)
            .replace("__FILEURL__", D["file"]["url"])
            .replace("__ITEMS__", str(s["items"]))
            .replace("__SCREENREFS__", str(s["screenRefs"]))
            .replace("__FRAMES__", str(s["frameLinks"]))
            .replace("__DECISIONS__", str(s["decisions"]))
            .replace("__OPEN__", str(s["open"])))

out = os.path.join(HERE, "qa-register.html")
io.open(out, "w", encoding="utf-8").write(PAGE)
print("wrote", out, len(PAGE), "chars")
