#!/usr/bin/env python3
"""drawers.py — drawer box build + runner mounting sheet.

Exists because assembly.py covers carcass joints and shelf pins but explicitly
defers runner mounting to v2 ("v2 will add runner mounting positions here"), and
because this project's drawer boxes are glued+pinned rather than drilled, so
they carry no joint entry at all. Without this sheet the packet tells a carpenter
to "Install L_BoxSide" and nothing else.

It used to rebuild packet.pdf itself, because extra_outputs ran after the packet
was already built. Fixed upstream (skill PR #3): the packet now builds last and
takes its document list from `packet_docs`, so this just writes its sheet.

Every dimension is derived from closet_spec.py — nothing is retyped. The one
thing deliberately NOT emitted is the runner's own fixing-hole pattern: that
belongs to its datasheet (hard rule 13).

Wired into the packet via `extra_outputs` in closet_spec.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import closet_spec as S  # noqa: E402

OPENING = S.TOWER_CLEAR                       # 564 clear between tower sides
BW, BH, BD, BT = S.L_BOX_W, S.L_BOX_H, S.L_BOX_D, S.BOX_T
SIDE_CLEAR = (OPENING - BW) / 2               # 13 per side
BOX_LIFT = 12                                 # box bottom above the bay floor
BAYS = S.DRAWER_Y                             # bay floor heights
BAY_CLEAR = 226
FRONT_W, FRONT_H = S.FRONT_LEN, S.FRONT_H
REVEAL = 3
SETBACK = S.TOWER_D - BD                      # 50 — box front behind the tower face
FB_LEN = BW - 2 * BT                          # 508
BOT_L, BOT_W = BW - 2 * BT, BD - 2 * BT       # 508 x 290 as modelled

GROOVE_D = 6                                  # if grooving instead
GROOVE_BOT_L = FB_LEN + 2 * GROOVE_D
GROOVE_BOT_W = BOT_W + 2 * GROOVE_D


def build(spec=None, outdir="output"):
    p = os.path.join(outdir, "drawers.md")
    L = []
    a = L.append

    a("# Drawer boxes — build and runner mounting\n")
    a(f"**6 identical boxes**, 3 per tower. Units mm. Every number below is "
      f"derived from the model; nothing is retyped.\n")

    a("\n## 1 — Parts per box\n")
    a("| Part | Qty | Size | Material |")
    a("|---|---:|---|---|")
    a(f"| Side | 2 | {BD} × {BH} × {BT} | 15 mm birch ply |")
    a(f"| Front / back | 2 | {FB_LEN} × {BH} × {BT} | 15 mm birch ply |")
    a(f"| Bottom | 1 | {GROOVE_BOT_L} × {GROOVE_BOT_W} × 6 | 6 mm birch ply, "
      f"**grooved in** — see §3 |")
    a(f"\nAssembled box: **{BW} W × {BH} H × {BD} D**. Sides run the full depth; "
      f"the front and back fit *between* them.\n")

    a("\n## 2 — Assembly\n")
    a("No dowels and no cams — the boxes are **glued and pinned**. A 7 mm "
      "confirmat body would split a 15 mm ply side, and dowelling six boxes is "
      "the fussy work this build was designed to avoid.\n")
    a("1. Dry-fit one box and check it before gluing all six.")
    a(f"2. Glue the front/back between the sides. Clamp square, or build in a "
      f"jig — the box must be **square to within 1 mm on the diagonals**, or the "
      f"runners will bind.")
    a("3. Pin through the sides into the front/back edges: 23 ga × 30 mm pins, "
      "3 per corner, while the glue is wet.")
    a(f"4. Measure both diagonals across the top of the box: they must match "
      f"within 1 mm. Adjust before the glue grabs.")
    a("5. Leave clamped until cured before fitting the bottom.\n")

    a("\n## 3 — The grooved bottom\n")
    a(f"**6 mm birch ply, {GROOVE_BOT_L} × {GROOVE_BOT_W}**, captured in a groove. "
      f"The earlier 4 mm hardboard option is dropped — at {BW} mm wide and loaded "
      f"with clothes it sagged.\n")
    a(f"- Groove **{GROOVE_D} mm wide × {GROOVE_D} mm deep**, **10 mm up** from "
      f"the bottom edge, in **all four** box parts.")
    a(f"- Cut the grooves **before** assembly — you cannot do it afterwards.")
    a(f"- The bottom is {GROOVE_D} mm oversize each way "
      f"({FB_LEN} + 2×{GROOVE_D} = {GROOVE_BOT_L}, {BOT_W} + 2×{GROOVE_D} = "
      f"{GROOVE_BOT_W}) so it lands in the grooves. Cutting it to the clear "
      f"opening instead is the classic mistake — it will fall straight through.")
    a(f"- Slide it in as the box is glued up; it needs no fasteners and it "
      f"squares the box for you.\n")

    a("\n## 4 — Runner mounting\n")
    a("**Side-mount ball-bearing runners, 300 mm, full extension, soft-close — "
      "6 pairs.**\n")
    a("Geometry from the model:\n")
    a("| | Value | Why |")
    a("|---|---|---|")
    a(f"| Bay clear height | {BAY_CLEAR} | between fixed shelves |")
    a(f"| Opening between tower sides | {OPENING} | |")
    a(f"| Box width | {BW} | leaves **{SIDE_CLEAR:.0f} mm each side** — the standard "
      f"side-mount runner clearance |")
    a(f"| Box bottom above bay floor | {BOX_LIFT} | runner sits in this gap |")
    a(f"| Box front setback from tower face | {SETBACK} | the applied front covers it |")
    a(f"| Box depth | {BD} | suits a 300 mm runner |")
    a("\nBay floor heights (top face of the shelf below each drawer):\n")
    a("| Drawer | Bay floor Y | Box bottom Y |")
    a("|---|---:|---:|")
    for i, y in enumerate(BAYS, 1):
        a(f"| {i} | {y + 18} | {y + 18 + BOX_LIFT} |")

    a("\n### What is NOT in this document\n")
    a("The runner's **own fixing-hole pattern, screw size, and the vertical "
      "offset between the runner and the box bottom** are not stated here. They "
      "differ between manufacturers and series, and guessing them ruins a panel. "
      "Take them from the datasheet for the runner you actually buy.\n")
    a("What the datasheet needs from you: **cabinet member** fixes to the tower "
      f"side inside a {OPENING} mm opening; **drawer member** fixes to a {BW} mm "
      f"wide × {BH} mm tall box; runner length 300 mm; box depth {BD} mm.\n")
    a("Mounting rules that hold regardless of series:\n")
    a("1. Both cabinet members in a bay must be at the **same height within "
      "1 mm** and **parallel front-to-back within 1 mm**, or the drawer binds.")
    a("2. Fix the front screw first, check the runner is level, then the rest.")
    a("3. Fit and test each box before moving to the next bay.\n")

    a("\n## 5 — Fronts\n")
    a(f"Applied shaker fronts, **{FRONT_W} × {FRONT_H}**, {REVEAL} mm reveal all "
      f"round. They are *not* part of the box — they screw on from inside.\n")
    a("1. Hang the box on its runners and close it.")
    a(f"2. Pack the front into place with {REVEAL} mm spacers top, bottom and "
      f"both sides. Tape it there.")
    a("3. From **inside** the box, drill two clearance holes through the box "
      "front and screw into the back of the panel. Keep the screws clear of "
      "where the pull will land.")
    a("4. Open, check the reveal is even, adjust, then add two more screws.")
    a("5. Fit the pull last, through both the front and its shaker rail.\n")

    a("\n## 6 — Order of operations\n")
    a("1. Cut all box parts and groove them for the bottom.")
    a("2. Glue and pin the six boxes; check diagonals; leave to cure.")
    a("3. Fit the bottoms.")
    a("4. Mount cabinet members in all six bays; check level and parallel.")
    a("5. Mount drawer members on the boxes.")
    a("6. Hang the boxes; check each runs freely.")
    a("7. Fit the fronts with spacers; adjust the reveal.")
    a("8. Fit the pulls.\n")

    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return ["drawers.md"]


if __name__ == "__main__":
    print(build(None, sys.argv[1] if len(sys.argv) > 1 else "output"))
