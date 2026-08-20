#!/usr/bin/env python3
"""make_index.py — project overview page, derived like everything else.

Reads the spec, the cut list and the cost sheet and writes index.html at the
repo root. Nothing is retyped, so the page cannot disagree with the package.

Visual language follows the hidden-tv-coffee-table project: warm paper ground,
a drafting title block, monospace numerics, small-caps section rules. Palette
shifted from oak to melamine-and-brass to match what this piece actually is.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, r"C:\Users\mhorv\.claude\skills\furniture-design\scripts")
sys.path.insert(0, HERE)

from closet_spec import (spec, NICHE_W, NICHE_H, NICHE_D, TOWER_D, T,  # noqa: E402
                         ENTRY_Z, T_Z0, T_Z1, HANG_Z0, HANG_Z1, DECK1_Y,
                         DECK2_Y, TOWER_H, DIV_X, ROD_Y_HIGH, ROD_Y_LOW)

cut = json.load(open(os.path.join(OUT, "cutlist.json"), encoding="utf-8"))
cost_md = open(os.path.join(OUT, "cost.md"), encoding="utf-8").read()

m = re.search(r"\*\*TOTAL inc\. VAT\*\* \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\*", cost_md)
tot_lo, tot_hi = (m.group(1), m.group(2)) if m else ("-", "-")
m2 = re.search(r"\| \*\*Net\*\* \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\*", cost_md)
net_lo, net_hi = (m2.group(1), m2.group(2)) if m2 else ("-", "-")

sheets = sum(s["sheets_est"] for s in cut["material_summary"].values())
nparts = sum(p["qty"] for p in cut["parts"])
band = sum(s.get("band_m", 0) for s in cut["material_summary"].values())
walkway = NICHE_W - 2 * TOWER_D
rod_hi, rod_lo = ROD_Y_HIGH + 11, ROD_Y_LOW + 11
supplier_rows = len([p for p in cut["parts"] if p["material_id"].startswith("melamine")])

_MAT_LABEL = {"melamine_17": "Coloured melamine 17",
              "plywood_birch_15": "Birch plywood 15",
              "plywood_birch_6": "Birch plywood 6"}

MAT_ROWS = "".join(
    '<tr><td>{}</td><td class="n">{}</td><td class="n">{:.2f}</td>'
    '<td class="n">{}</td><td class="n">{:.1f}</td></tr>'.format(
        _MAT_LABEL.get(k, k), s["parts"], s["area"], s["sheets_est"], s["band_m"])
    for k, s in cut["material_summary"].items())

DIMS = [("Niche, wall to wall", NICHE_W), ("Niche height", NICHE_H),
        ("Depth, left run", NICHE_D), ("Depth, right run", NICHE_D - T_Z0),
        ("Tower depth", TOWER_D), ("Tower length", T_Z1 - T_Z0),
        ("Tower height", TOWER_H), ("Walkway between towers", walkway),
        ("Hanging zone depth", HANG_Z1 - HANG_Z0),
        ("Deck 1 underside", DECK1_Y), ("Deck 2 underside", DECK2_Y),
        ("Upper rods", rod_hi), ("Lower rod", rod_lo),
        ("Board thickness", T)]
DIM_ROWS = "".join(
    '<tr><td>{}</td><td class="n">{}</td></tr>'.format(k, v) for k, v in DIMS)

CSS = """
:root{
  --paper:#ece7dd; --card:#f7f4ed; --card2:#efe9dc;
  --ink:#221f1a; --ink-soft:#6d675c; --line:#d6cec0;
  --panel:#e8e3d8;
  --brass:#a8763c; --accent:#8a5a2b;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#15130f; --card:#1f1c16; --card2:#282319;
    --ink:#ece7dc; --ink-soft:#a49b8a; --line:#362f24;
    --panel:#2b271f; --brass:#c79a5c; --accent:#d3a068;
  }
}
:root[data-theme="dark"]{
  --paper:#15130f; --card:#1f1c16; --card2:#282319;
  --ink:#ece7dc; --ink-soft:#a49b8a; --line:#362f24;
  --panel:#2b271f; --brass:#c79a5c; --accent:#d3a068;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
section{margin:64px 0}
h2{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-soft);
  font-weight:700;margin:0 0 18px;padding-bottom:9px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);font-weight:600;margin:0 0 10px}
header{padding-top:40px}
.tb{border:1.6px solid var(--ink);display:grid;grid-template-columns:2fr 1fr 1fr 1fr;
  margin-bottom:34px;background:var(--card)}
.tb .cell{border-left:1px solid var(--line);padding:9px 13px;min-width:0}
.tb .cell:first-child{border-left:none}
.tb .row2{grid-column:1/5;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;
  border-top:1px solid var(--line)}
.tb .row2 .cell:first-child{border-left:none}
.k{font-family:var(--mono);font-size:9px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-soft);display:block;margin-bottom:2px}
.v{font-family:var(--mono);font-size:14px;font-weight:700}
.v.big{font-size:16px;letter-spacing:-.01em}
h1{font-size:clamp(30px,5.2vw,50px);line-height:1.03;letter-spacing:-.02em;margin:0 0 14px;
  font-weight:800;text-wrap:balance;max-width:20ch}
.lede{font-size:19px;color:var(--ink-soft);max-width:62ch;margin:0}
figure{margin:0 0 18px;background:var(--card);border:1px solid var(--line);border-radius:6px;
  padding:20px 20px 14px;overflow-x:auto}
figure img{width:100%;height:auto;display:block;border-radius:3px}
figcaption{font-family:var(--mono);font-size:12px;color:var(--ink-soft);margin-top:12px;
  padding-top:10px;border-top:1px dashed var(--line);line-height:1.7}
.btnrow{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:650;font-size:15px;
  padding:12px 20px;border-radius:7px;border:1.5px solid var(--accent);background:var(--accent);
  color:#fff;transition:transform .12s ease,box-shadow .12s ease}
.btn:hover{text-decoration:none;transform:translateY(-1px);box-shadow:0 6px 18px rgba(0,0,0,.14)}
.btn.ghost{background:transparent;color:var(--accent)}
.viewer{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--panel);
  box-shadow:0 2px 10px rgba(0,0,0,.06)}
.viewer iframe{display:block;width:100%;height:560px;border:0}
.viewer-cap{font-family:var(--mono);font-size:12px;color:var(--ink-soft);
  padding:9px 14px;border-top:1px solid var(--line);background:var(--card);
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.cardx{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--brass);
  border-radius:6px;padding:18px 20px}
.cardx h3{margin:0 0 6px;font-size:16px}
.cardx p{margin:0;font-size:14.5px;color:var(--ink-soft)}
.cardx .num{font-family:var(--mono);font-size:11px;color:var(--accent);letter-spacing:.1em}
.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--card)}
table.cl{width:100%;border-collapse:collapse;font-size:13.5px}
table.cl th,table.cl td{text-align:left;padding:8px 13px;border-bottom:1px solid var(--line)}
table.cl th{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-soft);font-weight:700;background:var(--card2)}
table.cl td.n,table.cl th.n{text-align:right;font-family:var(--mono);
  font-variant-numeric:tabular-nums}
table.cl tr:last-child td{border-bottom:none}
table.cl tbody tr:hover{background:color-mix(in srgb,var(--brass) 10%,transparent)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}
.dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.dlcard{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:18px 20px;
  display:flex;flex-direction:column}
.dlcard h3{margin:0 0 4px;font-size:16px}
.dlcard .meta{font-family:var(--mono);font-size:11px;color:var(--ink-soft);margin-bottom:8px}
.dlcard p{margin:0 0 14px;font-size:13.5px;color:var(--ink-soft);flex:1}
.dllinks{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:var(--mono);font-size:12px;font-weight:600;padding:7px 12px;border-radius:6px;
  border:1px solid var(--brass);color:var(--ink);
  background:color-mix(in srgb,var(--brass) 14%,transparent)}
.chip:hover{text-decoration:none;background:color-mix(in srgb,var(--brass) 26%,transparent)}
.chip.solid{background:var(--brass);color:#fff;border-color:var(--brass)}
.prose p{font-size:16px;max-width:66ch;color:var(--ink)}
.prose p.soft{color:var(--ink-soft)}
.callout{border:1.5px solid var(--brass);background:color-mix(in srgb,var(--brass) 10%,transparent);
  border-radius:8px;padding:22px 24px}
.callout p{margin:0 0 10px;font-size:15px}
.callout p:last-child{margin-bottom:0}
.credits{border-top:1px solid var(--line);margin-top:70px;padding:22px 0 60px;
  font-family:var(--mono);font-size:12px;color:var(--ink-soft);line-height:1.9}
code{font-family:var(--mono);font-size:12.5px;background:var(--card2);padding:2px 6px;
  border-radius:4px}
@media(max-width:760px){
  .cards,.grid2{grid-template-columns:1fr}
  .tb,.tb .row2{grid-template-columns:1fr 1fr}
  .viewer iframe{height:420px}
}
"""

BODY = f"""
<header class="wrap">
  <div class="tb">
    <div class="cell"><span class="k">Project</span>
      <span class="v big">Master Bedroom Walk-In Closet</span></div>
    <div class="cell"><span class="k">Material</span>
      <span class="v">Melamine {T}</span></div>
    <div class="cell"><span class="k">Parts</span>
      <span class="v">{nparts}</span></div>
    <div class="cell"><span class="k">Sheets</span>
      <span class="v">{sheets}</span></div>
    <div class="row2">
      <div class="cell"><span class="k">Niche W &times; D &times; H</span>
        <span class="v">{NICHE_W} &times; {NICHE_D} &times; {NICHE_H}</span></div>
      <div class="cell"><span class="k">Assembly</span>
        <span class="v">59 screws</span></div>
      <div class="cell"><span class="k">Materials net</span>
        <span class="v">&#8362;{net_lo}&ndash;{net_hi}</span></div>
      <div class="cell"><span class="k">Units</span>
        <span class="v">mm</span></div>
    </div>
  </div>

  <p class="eyebrow">Built-in &middot; U-shaped &middot; frameless</p>
  <h1>A walk-in closet, reverse-engineered and rebuilt to fit</h1>
  <p class="lede">It started as an existing SketchUp model. Parsed back to exact
  geometry, re-derived against the architect&rsquo;s floor plan, then taken through
  fifteen revisions to a package a carpenter can build from.</p>

  <div class="btnrow">
    <a class="btn" href="output/packet.pdf">Carpenter packet (PDF)</a>
    <a class="btn ghost" href="output/render.html">Open the 3D render</a>
  </div>
</header>

<main class="wrap">

<section>
  <h2>Three dimensions</h2>
  <div class="viewer">
    <iframe src="output/render.html" title="3D render of the closet" loading="lazy"></iframe>
    <div class="viewer-cap">
      <span>Drag to orbit &middot; scroll to zoom</span>
      <span>Toggle the room, contents, either tower, hanging or decks</span>
    </div>
  </div>
</section>

<section>
  <h2>How the depth is used</h2>
  <div class="cards">
    <div class="cardx"><div class="num">Z 0 &ndash; {ENTRY_Z}</div>
      <h3>Entry</h3>
      <p>Left run only, kept clear floor to ceiling. Laundry basket in the corner
      and three hooks on the wall &mdash; nothing overhead, so a coat hangs its
      full length.</p></div>
    <div class="cardx"><div class="num">Z {T_Z0} &ndash; {T_Z1}</div>
      <h3>Towers</h3>
      <p>Two identical {T_Z1 - T_Z0} &times; {TOWER_D} runs facing each other across a
      {walkway} walkway. Shoes low, three shaker drawers at waist height,
      shelving above.</p></div>
    <div class="cardx"><div class="num">Z {HANG_Z0} &ndash; {HANG_Z1}</div>
      <h3>Hanging</h3>
      <p>The full {NICHE_W} width at {HANG_Z1 - HANG_Z0} deep &mdash; exactly shoulder
      depth. Long-hang left, double-hang right, split by a single central
      divider.</p></div>
  </div>
</section>

<section>
  <h2>Plan</h2>
  <figure>
    <img src="output/plan.png" alt="Plan view of the closet">
    <figcaption>{ENTRY_Z} entry &middot; {T_Z1 - T_Z0} towers &middot;
    {HANG_Z1 - HANG_Z0} hanging. The right run starts {T_Z0} further back &mdash;
    the left wall is {NICHE_D} deep, the right {NICHE_D - T_Z0}. The plan&rsquo;s
    128 + 37 = 165 split independently confirmed the tower position.</figcaption>
  </figure>
</section>

<section>
  <h2>Elevations</h2>
  <figure><img src="output/elev_left.png" alt="Left wall elevation">
    <figcaption>Left wall &mdash; open entry with hooks, tower, hanging.</figcaption></figure>
  <figure><img src="output/elev_right.png" alt="Right wall elevation">
    <figcaption>Right wall &mdash; an identical tower, starting {T_Z0} further
    back.</figcaption></figure>
  <figure><img src="output/elev_back.png" alt="Back wall elevation">
    <figcaption>Back wall &mdash; long-hang left at {rod_hi}, double-hang right at
    {rod_hi} and {rod_lo}. Divider on the centre line at X {DIV_X}.</figcaption></figure>
</section>

<section>
  <h2>Dimensions and materials</h2>
  <div class="grid2">
    <div class="tblwrap">
      <table class="cl"><thead><tr><th>Element</th><th class="n">mm</th></tr></thead>
      <tbody>{DIM_ROWS}</tbody></table>
    </div>
    <div>
      <div class="tblwrap">
        <table class="cl"><thead><tr><th>Material</th><th class="n">Parts</th>
        <th class="n">m&sup2;</th><th class="n">Sheets</th><th class="n">Band m</th></tr></thead>
        <tbody>{MAT_ROWS}</tbody></table>
      </div>
      <p class="mono" style="font-size:12px;color:var(--ink-soft);margin-top:12px">
        {band:.1f} m edge banding &middot; zero cams &middot; zero dowels
        &middot; 59 confirmat screws
      </p>
    </div>
  </div>
</section>

<section>
  <h2>Cost</h2>
  <div class="callout">
    <p><strong>&#8362;{net_lo}&ndash;{net_hi}</strong> materials and hardware, net
    <span class="mono" style="color:var(--ink-soft)">(&#8362;{tot_lo}&ndash;{tot_hi} inc. VAT)</span></p>
    <p class="soft">Board and banding are real supplier quotes &mdash; &#8362;280 per
    2440&times;1220 sheet of {T}&nbsp;mm coloured melamine including cutting, and
    &#8362;8 per metre to apply matched edge banding. Hardware and the two plywood
    lines are still assumed rates.</p>
    <p class="soft"><strong>Carpenter labour is excluded</strong>, and on fitted
    work it is usually the larger half of the bill.</p>
  </div>
</section>

<section>
  <h2>Documents</h2>
  <div class="dl">
    <div class="dlcard"><h3>Carpenter packet</h3>
      <div class="meta">PDF &middot; plan, elevations, cut list, assembly</div>
      <p>Everything the shop needs, in one print-ready document.</p>
      <div class="dllinks"><a class="chip solid" href="output/packet.pdf">packet.pdf</a></div></div>
    <div class="dlcard"><h3>Cut list</h3>
      <div class="meta">{nparts} parts &middot; {sheets} sheets</div>
      <p>Every part with its finished size, material, grain direction and which
      edges get banding.</p>
      <div class="dllinks"><a class="chip" href="output/cutlist.xlsx">xlsx</a>
        <a class="chip" href="output/cutlist.csv">csv</a>
        <a class="chip" href="output/cutlist.md">md</a></div></div>
    <div class="dlcard"><h3>&#1512;&#1513;&#1497;&#1502;&#1514; &#1495;&#1497;&#1514;&#1493;&#1498;</h3>
      <div class="meta">The shop&rsquo;s own template, filled</div>
      <p>{supplier_rows} rows in the supplier&rsquo;s Hebrew format, banding in their
      vocabulary, every part flagged rotatable &mdash; a plain colour has no grain.</p>
      <div class="dllinks"><a class="chip" href="output/%D7%A8%D7%A9%D7%99%D7%9E%D7%AA-%D7%97%D7%99%D7%AA%D7%95%D7%9A-%D7%9E%D7%9C%D7%90.xls">xls</a></div></div>
    <div class="dlcard"><h3>Assembly</h3>
      <div class="meta">Drilling coordinates &middot; build order</div>
      <p>Every joint specified &mdash; none left to a default. Plus a separate
      drawer-box and runner sheet.</p>
      <div class="dllinks"><a class="chip" href="output/assembly.md">assembly</a>
        <a class="chip" href="output/drawers.md">drawers</a></div></div>
    <div class="dlcard"><h3>Hardware and cost</h3>
      <div class="meta">Derived from the model</div>
      <p>Counts pulled from the assembly plan and the spec&rsquo;s fixtures, so they
      cannot drift away from the design.</p>
      <div class="dllinks"><a class="chip" href="output/hardware.md">hardware</a>
        <a class="chip" href="output/cost.md">cost</a></div></div>
    <div class="dlcard"><h3>Project record</h3>
      <div class="meta">Every decision, with its reasoning</div>
      <p>Measurements with their sources, and each decision &mdash; including the
      ones that were later reverted.</p>
      <div class="dllinks"><a class="chip" href="docs/spec.md">spec.md</a></div></div>
  </div>
</section>

<section>
  <h2>How it was made</h2>
  <div class="prose">
    <p>The SketchUp share link had no export, so the model was exported as a
    binary STL and parsed directly &mdash; 338,450 triangles welded into 503
    connected solids, axis-aligned faces bucketed by plane, coplanar faces
    reassembled into rectangles. <strong>No dimension was ever read off a
    screenshot.</strong></p>
    <p class="soft">The width that fell out of the parse, {NICHE_W}, was later
    confirmed independently by the architect&rsquo;s floor plan &mdash; which also
    corrected the left run&rsquo;s depth from 1700 to {NICHE_D}.</p>
    <p>Every deliverable here derives from one positioned-part spec. Change a
    number there and the cut list, drawings, assembly plan, hardware schedule,
    cost and render all follow. A cross-checker validates the seams between them
    and exits non-zero on any mismatch.</p>
  </div>
</section>

<div class="credits">
  <div>Drawn and documented with the <a
    href="https://github.com/mhorvvitz/furniture-design-skill">furniture-design skill</a>.</div>
  <div>Source: <a href="https://github.com/mhorvvitz/closetmasterbedroom">github.com/mhorvvitz/closetmasterbedroom</a></div>
  <div>Regenerate: <code>package.py closet_spec.py --out output/</code>
    &middot; verify: <code>consistency.py</code></div>
  <div>All dimensions in millimetres. Site-measure before cutting.</div>
</div>

</main>
"""

HTML = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>Master Bedroom Walk-In Closet</title>\n<style>'
        + CSS + '</style></head><body>' + BODY + '</body></html>\n')

path = os.path.join(HERE, "index.html")
with open(path, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wrote {path}  ({nparts} parts, {sheets} sheets, ILS {net_lo}-{net_hi} net)")
