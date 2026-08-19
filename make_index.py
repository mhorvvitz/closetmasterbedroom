#!/usr/bin/env python3
"""make_index.py — project overview page, derived like everything else.

Reads the spec, the cut list and the cost sheet and writes index.html at the
repo root. Nothing is retyped, so the page cannot disagree with the package.
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
                         DECK2_Y, TOWER_H)

cut = json.load(open(os.path.join(OUT, "cutlist.json"), encoding="utf-8"))
cost_md = open(os.path.join(OUT, "cost.md"), encoding="utf-8").read()

m = re.search(r"\*\*TOTAL inc\. VAT\*\* \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\*", cost_md)
tot_lo, tot_hi = (m.group(1), m.group(2)) if m else ("—", "—")
m2 = re.search(r"\| \*\*Net\*\* \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\*", cost_md)
net_lo, net_hi = (m2.group(1), m2.group(2)) if m2 else ("—", "—")

sheets = sum(s["sheets_est"] for s in cut["material_summary"].values())
nparts = sum(p["qty"] for p in cut["parts"])
band = sum(s.get("band_m", 0) for s in cut["material_summary"].values())
walkway = NICHE_W - 2 * TOWER_D

MAT_ROWS = "".join(
    f"<tr><td>{k.replace('_', ' ')}</td><td>{s['parts']}</td>"
    f"<td>{s['area']:.2f} m²</td><td>{s['sheets_est']}</td></tr>"
    for k, s in cut["material_summary"].items())

FIG = """<figure><img src="{src}" alt="{alt}"><figcaption>{cap}</figcaption></figure>"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Master Bedroom Walk-In Closet</title>
<style>
:root{{--ink:#22201d;--mut:#6f6960;--line:#e3ded4;--bg:#faf8f4;--accent:#8a6d3b}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
 font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
.wrap{{max-width:1000px;margin:0 auto;padding:48px 24px 80px}}
header{{border-bottom:2px solid var(--ink);padding-bottom:22px;margin-bottom:36px}}
h1{{margin:0 0 6px;font-size:30px;letter-spacing:-.4px}}
.sub{{color:var(--mut);font-size:15px}}
.badge{{display:inline-block;margin-top:14px;padding:5px 11px;border:1px solid var(--accent);
 border-radius:999px;color:var(--accent);font-size:12px;letter-spacing:.4px;text-transform:uppercase}}
h2{{margin:44px 0 14px;font-size:19px;border-left:3px solid var(--accent);padding-left:11px}}
p{{max-width:70ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:22px 0}}
.stat{{background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px 16px}}
.stat .n{{font-size:23px;font-weight:600;letter-spacing:-.5px}}
.stat .l{{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.5px;margin-top:3px}}
table{{border-collapse:collapse;width:100%;margin:16px 0;background:#fff;
 border:1px solid var(--line);border-radius:9px;overflow:hidden;font-size:15px}}
th,td{{padding:9px 13px;text-align:left;border-bottom:1px solid var(--line)}}
th{{background:#f3efe7;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.4px}}
tr:last-child td{{border-bottom:none}}
td:nth-child(n+2){{text-align:right;font-variant-numeric:tabular-nums}}
figure{{margin:22px 0;background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px}}
figure img{{width:100%;height:auto;display:block}}
figcaption{{color:var(--mut);font-size:13px;margin-top:9px}}
a.cta{{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;
 padding:11px 20px;border-radius:7px;font-size:15px}}
a.cta:hover{{background:var(--accent)}}
.files a{{display:inline-block;margin:0 10px 8px 0;color:var(--accent);font-size:14px}}
.note{{background:#fff;border-left:3px solid var(--accent);padding:12px 16px;
 border-radius:0 7px 7px 0;font-size:14.5px;margin:18px 0}}
footer{{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);
 color:var(--mut);font-size:13px}}
code{{background:#f0ebe1;padding:1px 5px;border-radius:4px;font-size:13.5px}}
</style></head><body><div class="wrap">

<header>
  <h1>Master Bedroom Walk-In Closet</h1>
  <div class="sub">Built-in, U-shaped · 17&nbsp;mm coloured melamine · frameless, screw-assembled</div>
  <div class="badge">Built with the furniture-design skill</div>
</header>

<p>A fitted walk-in closet for a {NICHE_W}&nbsp;×&nbsp;{NICHE_D}&nbsp;mm recess, reverse-engineered
from an existing SketchUp model and then re-derived against the architect's floor plan.
Two matched towers face each other across a {walkway}&nbsp;mm walkway, with hanging across the
full width at the back and two open decks above.</p>

<div class="grid">
  <div class="stat"><div class="n">{NICHE_W}&nbsp;×&nbsp;{NICHE_D}</div><div class="l">Niche, mm</div></div>
  <div class="stat"><div class="n">{NICHE_H}</div><div class="l">Height, mm</div></div>
  <div class="stat"><div class="n">{nparts}</div><div class="l">Cut parts</div></div>
  <div class="stat"><div class="n">{sheets}</div><div class="l">Sheets</div></div>
  <div class="stat"><div class="n">₪{net_lo}–{net_hi}</div><div class="l">Materials, net</div></div>
</div>

<h2>3D view</h2>
{FIG.format(src="output/render_revM.png", alt="3D render",
            cap="Interactive version has toggles for the room, contents and each tower, five fixed viewpoints, and five board finishes.")}
<a class="cta" href="output/render.html">Open the interactive render →</a>

<h2>Plan</h2>
{FIG.format(src="output/plan.png", alt="Plan view",
            cap=f"Depth zones: {ENTRY_Z} entry · {T_Z1 - T_Z0} towers · {HANG_Z1 - HANG_Z0} hanging. The right run starts {T_Z0} back — the left wall is {NICHE_D} deep, the right {NICHE_D - T_Z0}.")}

<h2>Elevations</h2>
{FIG.format(src="output/elev_left.png", alt="Left wall elevation", cap="Left wall — entry zone with hooks, tower, hanging.")}
{FIG.format(src="output/elev_right.png", alt="Right wall elevation", cap="Right wall — tower and hanging. Identical tower to the left.")}
{FIG.format(src="output/elev_back.png", alt="Back wall elevation", cap="Back wall — long-hang left, double-hang right, split by the central divider.")}

<h2>Key dimensions</h2>
<table>
<tr><th>Element</th><th>mm</th></tr>
<tr><td>Niche width / height</td><td>{NICHE_W} / {NICHE_H}</td></tr>
<tr><td>Depth — left wall / right wall</td><td>{NICHE_D} / {NICHE_D - T_Z0}</td></tr>
<tr><td>Tower depth / length / height</td><td>{TOWER_D} / {T_Z1 - T_Z0} / {TOWER_H}</td></tr>
<tr><td>Walkway between towers</td><td>{walkway}</td></tr>
<tr><td>Hanging zone depth</td><td>{HANG_Z1 - HANG_Z0}</td></tr>
<tr><td>Deck 1 / deck 2 underside</td><td>{DECK1_Y} / {DECK2_Y}</td></tr>
<tr><td>Board thickness</td><td>{T}</td></tr>
</table>

<h2>Materials</h2>
<table>
<tr><th>Material</th><th>Parts</th><th>Area</th><th>Sheets</th></tr>
{MAT_ROWS}
</table>
<p>Edge banding: <strong>{band:.1f} m</strong> decor-matched ABS.</p>

<h2>Cost</h2>
<table>
<tr><th></th><th>Low</th><th>High</th></tr>
<tr><td>Materials + hardware, net</td><td>₪{net_lo}</td><td>₪{net_hi}</td></tr>
<tr><td>Including VAT</td><td>₪{tot_lo}</td><td>₪{tot_hi}</td></tr>
</table>
<div class="note"><strong>Board price is a real supplier quote</strong> — ₪280 per
2440×1220 sheet of 17&nbsp;mm coloured melamine, including cutting. Banding, hardware
and the plywood lines are still assumed rates. <strong>Carpenter labour is excluded</strong>,
and on fitted work it is usually the larger half of the bill.</div>

<h2>Documents</h2>
<div class="files">
  <a href="output/packet.pdf">Carpenter packet (PDF)</a>
  <a href="output/cutlist.xlsx">Cut list (xlsx)</a>
  <a href="output/%D7%A8%D7%A9%D7%99%D7%9E%D7%AA-%D7%97%D7%99%D7%AA%D7%95%D7%9A-%D7%9E%D7%9C%D7%90.xls">רשימת חיתוך לספק (xls)</a>
  <a href="output/assembly.md">Assembly plan</a>
  <a href="output/drawers.md">Drawer build</a>
  <a href="output/hardware.md">Hardware schedule</a>
  <a href="output/cost.md">Cost estimate</a>
  <a href="docs/spec.md">Project record &amp; decisions</a>
</div>

<footer>
  <p>Every deliverable on this page is <strong>derived</strong> from a single
  positioned-part spec (<code>closet_spec.py</code>). Regenerate the lot with:</p>
  <p><code>python package.py closet_spec.py --out output/</code></p>
  <p>Cross-checked by <code>consistency.py</code>, which validates the cut list against
  the spec, the supplier sheet against the cut list, the hardware schedule against the
  assembly plan, and every material against a priced rate.</p>
</footer>

</div></body></html>
"""

path = os.path.join(HERE, "index.html")
with open(path, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wrote {path}  ({nparts} parts, {sheets} sheets, ILS {net_lo}-{net_hi} net)")
