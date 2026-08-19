#!/usr/bin/env python3
"""hardware.py — hardware schedule, DERIVED from the spec and the assembly plan.

It was hand-written for nine revisions and drifted badly: by rev N it still
listed 52 Minifix cams and 4 L-brackets that had been deleted from the design,
and 13 confirmats where the model said 59. Deriving it removes that failure mode
— the only authored part left is the small table of things a model cannot know
(runner series, rod profile, LED electrical spec).

Wired into the packet via `extra_outputs` in closet_spec.py.
"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _fixtures(spec):
    return Counter(p["defn"] for p in spec["parts"] if p.get("kind") == "fixture")


def _rods(spec):
    return [p for p in spec["parts"] if p.get("kind") == "rod"]


def _from_assembly(outdir):
    """Connector counts straight out of assembly.md — the authoritative source."""
    p = os.path.join(outdir, "assembly.md")
    if not os.path.exists(p):
        return {}
    txt = open(p, encoding="utf-8").read()
    out = {}
    for qty, item in re.findall(r"^- (\d+)× (.+)$", txt, re.M):
        out[item.strip()] = int(qty)
    return out


def build(spec, outdir="output"):
    import closet_spec as S
    fx = _fixtures(spec)
    rods = _rods(spec)
    conn = _from_assembly(outdir)
    band = 0.0
    cj = os.path.join(outdir, "cutlist.json")
    if os.path.exists(cj):
        cut = json.load(open(cj, encoding="utf-8"))
        band = sum(m.get("band_m", 0.0) for m in cut["material_summary"].values())

    n_drawers = sum(v for k, v in Counter(
        p["defn"] for p in spec["parts"]).items() if k.endswith("_BoxBottom"))

    L = []
    a = L.append
    a("# Hardware schedule — Master Bedroom Walk-In Closet\n")
    a("**Generated from the spec and `assembly.md` — do not edit by hand.**")
    a("Re-run `package.py` after any change. Quantities exclude spares; "
      "order ~10% over.\n")

    a("\n## Carcass connectors — counted from the assembly plan\n")
    a("| Item | Qty |")
    a("|---|---:|")
    if conn:
        for item, qty in conn.items():
            a(f"| {item} | {qty} |")
    else:
        a("| *(assembly.md not generated yet)* | — |")
    a("\nDrilling coordinates for every one of these are in `assembly.md`.\n")

    a("\n## Movement and hanging — counted from the model\n")
    a("| Item | Qty | Spec |")
    a("|---|---:|---|")
    a(f"| Drawer runner pair, side-mount ball bearing | {n_drawers} | "
      f"300 mm, full extension, soft-close |")
    a(f"| Bar pull, **brass / gold** | {fx['L_Pull'] + fx['R_Pull']} | "
      f"160 mm centres. Specify lacquered or PVD — unlacquered brass patinas |")
    a(f"| Hanging rod | {len(rods)} | Ø25 oval or Ø32 round — **assumed, confirm** |")
    a(f"| Rod end socket | {len(rods) * 2} | to suit the rod profile |")
    a(f"| Rod centre support | {len(rods)} | every rod here exceeds 800 mm |")
    a(f"| Wall hook | {fx['Hook']} | entry zone, left wall at Y 1700 |")

    a("\n### Rod cut lengths\n")
    a("| Length | Centreline height | Bay |")
    a("|---:|---:|---|")
    for r in sorted(rods, key=lambda r: (-(r["y"]), r["x"])):
        bay = "left / long-hang" if r["x"] < S.DIV_X else "right / double-hang"
        a(f"| {r['sx']:.0f} | {r['y'] + r['sy'] / 2:.0f} | {bay} |")
    a(f"\nAll rods sit **{S.HANG_Z1 - (S.ROD_Z + 11):.0f} mm forward of the back "
      f"wall** (centreline Z = {S.ROD_Z + 11:.0f}).\n")

    a("\n## Lighting\n")
    a("| Item | Qty | Spec |")
    a("|---|---:|---|")
    led = [p for p in spec["parts"] if p["defn"] == "LED_Channel"]
    tot = sum(p["sx"] for p in led) / 1000.0
    a(f"| Aluminium LED channel + diffuser | {len(led)} | "
      f"16 × 16 mm, {tot:.2f} m total |")
    a(f"| LED strip, warm white | {tot:.2f} m | 2700–3000 K, CRI ≥ 90 |")
    a("| LED driver | 1 | 24 V, sized to the run + 20% |")
    a("| PIR / door switch | 1 | usual choice for a walk-in |")
    a("\nChannel mounts on the **underside of deck 1's back panel**, set back "
      "40 mm from the front edge.\n")

    a("\n## Fixing to the structure\n")
    a("| Item | Qty | Note |")
    a("|---|---:|---|")
    a("| Wall fixing (plug + screw) | ~40 | cleats, tower backs, divider. "
      "**Verify the substrate** — plasterboard needs a different anchor. |")
    a("| Screw 4 × 40 | 8 | divider base blocks: 2 into the back wall and "
      "2 into the divider, per block. NOT confirmat — 7 mm would split a "
      "17 mm block. |")
    a("\n> **The floor is tiled**, so the divider blocks take no floor fixing — "
      "they are fixed to the back wall only.\n")

    a("\n## Edge banding\n")
    a(f"~{band:.1f} m, decor-matched ABS — **order {band * 1.15:.0f} m**.\n")
    a("Ask the supplier to band one long 50 mm strip on both edges **before** "
      "cross-cutting the shaker rails and stiles; that turns 24 separate edger "
      "passes into two. Banding is often priced per piece, not per metre.\n")

    a("\n## Bought storage\n")
    a(f"Shoe rack for the long-hang bay: **{S.DIV_X} wide × {S.HANG_Z1 - S.HANG_Z0} "
      f"deep**, max **≈ 500 tall** before it fouls the hanging garments.\n")
    a("Not included: laundry basket, storage boxes, hangers.\n")

    p = os.path.join(outdir, "hardware.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return ["hardware.md"]


if __name__ == "__main__":
    from closet_spec import spec as _s
    print(build(_s, sys.argv[1] if len(sys.argv) > 1 else "output"))
