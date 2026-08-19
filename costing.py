#!/usr/bin/env python3
"""costing.py — materials + hardware cost estimate for the walk-in closet.

DERIVED, not authored: reads output/cutlist.json (which itself derives from
closet_spec.py) and rates.json (the authored price source). Nothing here is
hand-typed, so the estimate cannot drift from the cut list.

Every rate is an ASSUMED market price and is labelled as such in the output.
Carpenter labour, delivery and installation are excluded.

Usage:  python costing.py            -> writes output/cost.md
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.join(HERE, "output", "cutlist.json")
RATES = os.path.join(HERE, "rates.json")
OUT = os.path.join(HERE, "output", "cost.md")

cut = json.load(open(CUT, encoding="utf-8"))
rates = json.load(open(RATES, encoding="utf-8"))

CUR = rates["currency"]
WASTE = rates["waste_pct"]["value"] / 100.0
summary = cut["material_summary"]

rows, sheet_lo, sheet_hi = [], 0.0, 0.0
for mid, s in summary.items():
    r = rates["sheets"].get(mid)
    if r is None:
        rows.append((mid, "?", "—", "—", "**NO RATE — add to rates.json**"))
        continue
    n = s["sheets_est"]
    lo, hi = n * r["low"], n * r["high"]
    sheet_lo += lo
    sheet_hi += hi
    rows.append((r["desc"], n, f"{lo:,.0f}", f"{hi:,.0f}",
                 f"{s['parts']} parts · {s['area']:.2f} m²"))

band_m = sum(s.get("band_m", 0.0) for s in summary.values())
b = rates["banding_per_m"]
band_lo, band_hi = band_m * b["low"], band_m * b["high"]

hw_rows, hw_lo, hw_hi = [], 0.0, 0.0
for h in rates["hardware"]:
    lo, hi = h["qty"] * h["low"], h["qty"] * h["high"]
    hw_lo += lo
    hw_hi += hi
    hw_rows.append((h["item"], h["qty"], f"{lo:,.0f}", f"{hi:,.0f}"))

sub_lo = sheet_lo + band_lo + hw_lo
sub_hi = sheet_hi + band_hi + hw_hi
w_lo, w_hi = sub_lo * WASTE, sub_hi * WASTE
net_lo, net_hi = sub_lo + w_lo, sub_hi + w_hi
vat = rates["vat_pct"] / 100.0
tot_lo, tot_hi = net_lo * (1 + vat), net_hi * (1 + vat)

L = []
a = L.append
a("# Materials cost estimate — Master Bedroom Walk-In Closet\n")
a(f"Currency: **{CUR}**. Derived from `output/cutlist.json` + `rates.json`.\n")
a("> ⚠️ **Every rate below is an ASSUMED market price, not a quote.** Replace the\n"
  "> numbers in `rates.json` with real supplier prices before committing money.\n"
  "> **Carpenter labour, delivery and installation are NOT included** — on a job\n"
  "> like this they are usually the larger half of the bill.\n")

a("\n## Boards\n")
a(f"| Material | Sheets (est.) | {CUR} low | {CUR} high | Basis |")
a("|---|---:|---:|---:|---|")
for d, n, lo, hi, note in rows:
    a(f"| {d} | {n} | {lo} | {hi} | {note} |")
a(f"| **Boards subtotal** | | **{sheet_lo:,.0f}** | **{sheet_hi:,.0f}** | |")
a("\nSheet counts come from the cut list's yield heuristic, **not** an optimised\n"
  "nesting plan. Run OpenCutList or CutList Optimizer on the real parts for a\n"
  "firm sheet count — it can move this line by a whole sheet either way.\n")

a("\n## Edge banding\n")
a(f"| Item | Metres | {CUR} low | {CUR} high |")
a("|---|---:|---:|---:|")
a(f"| {b['desc']} | {band_m:.1f} | {band_lo:,.0f} | {band_hi:,.0f} |")

a("\n## Hardware\n")
a(f"| Item | Qty | {CUR} low | {CUR} high |")
a("|---|---:|---:|---:|")
for item, qty, lo, hi in hw_rows:
    a(f"| {item} | {qty} | {lo} | {hi} |")
a(f"| **Hardware subtotal** | | **{hw_lo:,.0f}** | **{hw_hi:,.0f}** |")

a("\n## Total\n")
a(f"| | {CUR} low | {CUR} high |")
a("|---|---:|---:|")
a(f"| Boards | {sheet_lo:,.0f} | {sheet_hi:,.0f} |")
a(f"| Edge banding | {band_lo:,.0f} | {band_hi:,.0f} |")
a(f"| Hardware | {hw_lo:,.0f} | {hw_hi:,.0f} |")
a(f"| Subtotal | {sub_lo:,.0f} | {sub_hi:,.0f} |")
a(f"| Waste allowance {rates['waste_pct']['value']}% | {w_lo:,.0f} | {w_hi:,.0f} |")
a(f"| **Net** | **{net_lo:,.0f}** | **{net_hi:,.0f}** |")
a(f"| VAT {rates['vat_pct']}% | {tot_lo - net_lo:,.0f} | {tot_hi - net_hi:,.0f} |")
a(f"| **TOTAL inc. VAT** | **{tot_lo:,.0f}** | **{tot_hi:,.0f}** |")
a("")
a(f"**Materials and hardware: roughly {CUR} {net_lo:,.0f}–{net_hi:,.0f} before VAT, "
  f"{CUR} {tot_lo:,.0f}–{tot_hi:,.0f} with it.**")
a("\nExcluded: carpenter labour, CNC/edging shop time, delivery, installation,\n"
  "electrical work for the LED, and the props (laundry basket, storage boxes).\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(f"  cost.md  ({CUR} {net_lo:,.0f}–{net_hi:,.0f} net, {tot_lo:,.0f}–{tot_hi:,.0f} inc VAT)")
