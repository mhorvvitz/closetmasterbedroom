#!/usr/bin/env python3
"""elevations.py — three wall elevations for the U-shaped walk-in.

package.py's front.svg looks at the back wall only. A U-shaped built-in needs one
elevation per run, so this re-projects the SAME positioned-part spec onto each
wall plane and reuses the tested draw.py emitter. Nothing is re-measured: every
rectangle here is the spec's own part boxes, rotated.

Projections (spec frame: X=width, Y=height, Z=depth):
  left wall  — viewer faces -X. Room front (Z=0) on the left  -> u = z
  right wall — viewer faces +X. Room front (Z=0) on the right -> u = D-(z+sz)
  back wall  — viewer faces +Z. Straight through            -> u = x
"""
import os
import sys

sys.path.insert(0, r"C:\Users\mhorv\.claude\skills\furniture-design\scripts")
import draw  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closet_spec import spec, NICHE_W, NICHE_H, NICHE_D, TOWER_D, DIV_X  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def project(parts, mode):
    out = []
    for p in parts:
        q = dict(p)
        if mode == "left":
            q["x"], q["sx"] = p["z"], p["sz"]
            q["z"], q["sz"] = p["x"], p["sx"]
        elif mode == "right":
            q["x"], q["sx"] = NICHE_D - (p["z"] + p["sz"]), p["sz"]
            q["z"], q["sz"] = NICHE_W - (p["x"] + p["sx"]), p["sx"]
        out.append(q)
    return out


VIEWS = [
    ("elev_left.svg", "left",
     "Left wall elevation — shoe shelves, 3 drawers, open shelving  ·  view looking at X=0",
     lambda p: p["x"] < DIV_X + 18,
     (NICHE_D, NICHE_H, TOWER_D)),
    ("elev_right.svg", "right",
     "Right wall elevation — 5 wire baskets, open shelving  ·  view looking at X=1650",
     lambda p: p["x"] + p["sx"] > DIV_X,
     (NICHE_D, NICHE_H, TOWER_D)),
    ("elev_back.svg", "back",
     "Back wall elevation — hanging zone, long-hang left / double-hang right",
     lambda p: p["z"] + p["sz"] > 900,
     (NICHE_W, NICHE_H, NICHE_D)),
]

for fname, mode, title, keep, (W, H, D) in VIEWS:
    parts = [p for p in spec["parts"] if keep(p)]
    if mode != "back":
        parts = project(parts, mode)
    sub = dict(name=title, overall=dict(W=W, H=H, D=D),
               origin=spec.get("origin", [0, 0, 0]), parts=parts)
    draw.draw(sub, os.path.join(OUT, fname), title=title)
    print(f"  {fname}  ({len(parts)} parts)")
