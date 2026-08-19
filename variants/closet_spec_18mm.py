#!/usr/bin/env python3
"""closet_spec.py — Master Bedroom Walk-In Closet, positioned-part spec.

Rev B — rebuilt to the architectural floor plan and the user's constraints
(2026-08-15). Every input number here is transcribed from docs/spec.md, which is
the source of truth. Do not edit dimensions here without changing it first.

Frame (carcass.py convention, mm):
    X = width   0 .. 1650   (0 = inside face of the LEFT side wall)
    Y = height  0 .. 2600   (0 = finished floor, up)
    Z = depth   0 .. 1600   (0 = front of the LEFT wall run, 1600 = back wall)

Depth zones, both side walls:
    Z    0 ..  400   left wall only — KEPT EMPTY for entry + laundry basket
    Z  400 .. 1000   towers, 600 long, identical both sides
    Z 1000 .. 1600   hanging, 600 deep, full width
The right wall run starts at Z=400 (it is 1200 deep against the left's 1600).
"""
import sys

sys.path.insert(0, r"C:\Users\mhorv\.claude\skills\furniture-design\scripts")

from carcass import Carcass  # noqa: E402

# ---------------------------------------------------------------- parameters
T = 18                 # carcass panel thickness
T_DECK = 25            # decks — thick enough to span unaided; no valance needed
T_TRIM = 18            # shaker trim: cut from 18mm offcuts of the main sheets
GROOVE = 6             # drawer-bottom groove depth
TRIM_W = 50            # shaker frame width
MAT = "melamine"       # melamine-faced board, oak decor — carcass AND fronts
PLY = "plywood_birch"  # drawer boxes

NICHE_W, NICHE_H, NICHE_D = 1650, 2600, 1600

ENTRY_Z = 400                   # front zone kept clear (left wall)
T_Z0, T_Z1 = 400, 1000          # tower footprint along Z — both sides
HANG_Z0, HANG_Z1 = 1000, 1600   # hanging zone, 600 deep
TOWER_D, TOWER_H = 370, 1900    # rev C: deck 1 raised to 1900, towers follow
TOWER_CLEAR = (T_Z1 - T_Z0) - 2 * T          # 564
R_X0 = NICHE_W - TOWER_D                     # 1280

DIV_X = 807                     # hanging divider, left face
DECK1_Y, DECK2_Y = 1900, 2250   # deck 2 raised too, to keep the upper bays equal
UPRIGHT_H = DECK2_Y - (DECK1_Y + T_DECK)     # 325

ROD_Z = 1289                    # → centreline Z 1300 (300 from the back wall)
ROD_Y_HIGH, ROD_Y_LOW = 1839, 889            # → centrelines 1850 / 900
#   double-hang upper drop = 1850 - 900 = 950  (was 840 — open question 3 closed)

CLEAT_W, CLEAT_T = 40, 18

c = Carcass(NICHE_W, NICHE_H, NICHE_D, t=T, material=MAT,
            name="Master Bedroom Walk-In Closet")


# ================================================ LEFT RUN — OPEN AT THE FRONT
# No end panel (user): the entry zone stays fully open. Both deck arms are
# carried over it by wall-mounted L-brackets — see the fixtures at the bottom.


# ================================================ TOWERS — IDENTICAL BOTH SIDES
SHOE_Y = (150, 285, 420)
SHELF_Y = (555, 799, 1043, 1287, 1530)
DRAWER_Y = (573, 817, 1061)          # bay bottoms, 226 clear each

L_BOX_W = TOWER_CLEAR - 26           # 538 — side-mount runner clearance
L_BOX_H, L_BOX_D, BOX_T = 180, 320, 15

FRONT_LEN = (T_Z1 - T_Z0) - 6        # 594
FRONT_H = 220
FRONT_Z = T_Z0 + 3                   # 403

for tag, x0, dirn, front_x in (("L", 0, +1, TOWER_D),
                               ("R", R_X0, -1, R_X0 - T)):
    for z in (T_Z0, T_Z1 - T):
        c.add(f"{tag}_Side", x=x0, y=0, z=z, sx=TOWER_D, sy=TOWER_H, sz=T,
              note="grain vertical; System-32 line 37mm from the wall face")

    zi = T_Z0 + T                    # 418 — inside face of the near side
    c.add(f"{tag}_Bottom", x=x0, y=0, z=zi, sx=TOWER_D, sy=T, sz=TOWER_CLEAR,
          note="fixed — cam-and-dowel")
    for y in SHOE_Y:
        c.add(f"{tag}_ShoeShelf", x=x0, y=y, z=zi,
              sx=TOWER_D, sy=T, sz=TOWER_CLEAR, note="shoe shelf")
    for y in SHELF_Y:
        c.add(f"{tag}_Shelf", x=x0, y=y, z=zi,
              sx=TOWER_D, sy=T, sz=TOWER_CLEAR, note="fixed — carries a drawer bay")

    # shaker drawer fronts — melamine base panel in the SAME oak decor as the
    # shelves, with applied melamine frame trim, plus a bar pull.
    trim_x = (front_x + T) if dirn > 0 else (front_x - T_TRIM)
    pull_x = (trim_x + T_TRIM) if dirn > 0 else (trim_x - 35)
    for y0 in DRAWER_Y:
        fy = y0 + 3
        c.add(f"{tag}_DrawerFront", x=front_x, y=fy, z=FRONT_Z,
              sx=T, sy=FRONT_H, sz=FRONT_LEN, kind="door",
              note="base panel — oak decor, same board as the shelves; 3mm reveal")
        # frame: rails run the full width, stiles fit between them
        for ry in (fy, fy + FRONT_H - TRIM_W):
            c.add(f"{tag}_ShakerRail", x=trim_x, y=ry, z=FRONT_Z,
                  sx=T_TRIM, sy=TRIM_W, sz=FRONT_LEN, kind="door",
                  note="applied shaker trim — glued + pinned to the front")
        for rz in (FRONT_Z, FRONT_Z + FRONT_LEN - TRIM_W):
            c.add(f"{tag}_ShakerStile", x=trim_x, y=fy + TRIM_W, z=rz,
                  sx=T_TRIM, sy=FRONT_H - 2 * TRIM_W, sz=TRIM_W, kind="door",
                  note="applied shaker trim — glued + pinned to the front")
        c.fixture(f"{tag}_Pull", x=pull_x, y=fy + FRONT_H / 2 - 10,
                  z=FRONT_Z + FRONT_LEN / 2 - 100, sx=35, sy=20, sz=200,
                  note="bar pull, 160mm centres — bought")

    # drawer boxes — pull toward the walkway
    bx = 0 if tag == "L" else R_X0 + (TOWER_D - L_BOX_D)
    for y0 in DRAWER_Y:
        bz = zi + (TOWER_CLEAR - L_BOX_W) / 2
        by = y0 + 12
        c.add(f"{tag}_BoxSide", x=bx, y=by, z=bz,
              sx=L_BOX_D, sy=L_BOX_H, sz=BOX_T, material=PLY, grain="none")
        c.add(f"{tag}_BoxSide", x=bx, y=by, z=bz + L_BOX_W - BOX_T,
              sx=L_BOX_D, sy=L_BOX_H, sz=BOX_T, material=PLY, grain="none")
        c.add(f"{tag}_BoxFB", x=bx, y=by, z=bz + BOX_T,
              sx=BOX_T, sy=L_BOX_H, sz=L_BOX_W - 2 * BOX_T, material=PLY, grain="none")
        c.add(f"{tag}_BoxFB", x=bx + L_BOX_D - BOX_T, y=by, z=bz + BOX_T,
              sx=BOX_T, sy=L_BOX_H, sz=L_BOX_W - 2 * BOX_T, material=PLY, grain="none")
        # 6mm ply bottom captured in a groove, 10mm up from the box bottom.
        # Cut size adds 2 x GROOVE each way so it lands in the grooves — this
        # is why it reads as an overlap against the four box parts (expected).
        c.add(f"{tag}_BoxBottom", x=bx + BOX_T - GROOVE, y=by + 10,
              z=bz + BOX_T - GROOVE,
              sx=L_BOX_D - 2 * BOX_T + 2 * GROOVE, sy=GROOVE,
              sz=L_BOX_W - 2 * BOX_T + 2 * GROOVE,
              material=PLY, grain="none",
              note="sits in a 6mm groove, 10mm up from the bottom edge")


# ================================================================ HANGING ZONE
HANG_D = HANG_Z1 - HANG_Z0      # 600
c.add("Divider", x=DIV_X, y=0, z=HANG_Z0, sx=T, sy=TOWER_H, sz=HANG_D,
      note="grain vertical; splits long-hang (left) from double-hang (right)")

c.rod(y=ROD_Y_HIGH, x0=0, x1=DIV_X, z=ROD_Z)              # long hang
c.rod(y=ROD_Y_HIGH, x0=DIV_X + T, x1=NICHE_W, z=ROD_Z)    # double hang, upper
c.rod(y=ROD_Y_LOW, x0=DIV_X + T, x1=NICHE_W, z=ROD_Z)     # double hang, lower

c.add("ShoeShelf", x=0, y=150, z=1300, sx=DIV_X, sy=T, sz=300,
      note="low shelf in the long-hang bay")
c.add("ShoeCleat_Back", x=0, y=132, z=HANG_Z1 - CLEAT_W, sx=DIV_X, sy=CLEAT_T, sz=CLEAT_W)
c.add("ShoeCleat_Left", x=0, y=132, z=1300, sx=CLEAT_W, sy=CLEAT_T, sz=260)


# ============================================ DECK 1 — runs the FULL length
c.add("Deck1_LeftArm", x=0, y=DECK1_Y, z=0, sx=TOWER_D, sy=T_DECK, sz=HANG_Z0)
c.add("Deck1_RightArm", x=R_X0, y=DECK1_Y, z=T_Z0, sx=TOWER_D, sy=T_DECK, sz=HANG_Z0 - T_Z0)
c.add("Deck1_Back", x=0, y=DECK1_Y, z=HANG_Z0, sx=DIV_X, sy=T_DECK, sz=HANG_D)
c.add("Deck1_Back", x=DIV_X + T, y=DECK1_Y, z=HANG_Z0,
      sx=NICHE_W - DIV_X - T, sy=T_DECK, sz=HANG_D)

# no valance (user): 25mm decks carry the 807/825 span on their own
c.add("Cleat_D1_SideL", x=0, y=DECK1_Y - CLEAT_T, z=HANG_Z0,
      sx=CLEAT_W, sy=CLEAT_T, sz=HANG_D - CLEAT_W)
c.add("Cleat_D1_SideR", x=NICHE_W - CLEAT_W, y=DECK1_Y - CLEAT_T, z=HANG_Z0,
      sx=CLEAT_W, sy=CLEAT_T, sz=HANG_D - CLEAT_W)
c.add("Cleat_D1_Back", x=0, y=DECK1_Y - CLEAT_T, z=HANG_Z1 - CLEAT_W,
      sx=DIV_X, sy=CLEAT_T, sz=CLEAT_W)
c.add("Cleat_D1_Back", x=DIV_X + T, y=DECK1_Y - CLEAT_T, z=HANG_Z1 - CLEAT_W,
      sx=NICHE_W - DIV_X - T, sy=CLEAT_T, sz=CLEAT_W)


# ================================================ UPRIGHTS between the decks
UP_Y = DECK1_Y + T_DECK
for x0 in (0, R_X0):
    for z in (T_Z0, T_Z1 - T):
        c.add("Upright", x=x0, y=UP_Y, z=z, sx=TOWER_D, sy=UPRIGHT_H, sz=T)
# above the divider: full 600 deep, aligned with the divider below.
c.add("Upright_Div", x=DIV_X, y=UP_Y, z=HANG_Z0, sx=T, sy=UPRIGHT_H, sz=HANG_D,
      note="continues the divider line up to deck 2")
# (user) NO quarter-point uprights: the hanging zone reads as one clean opening
# top to bottom, broken only by the central divider line. Deck 2's back span is
# instead handled by its own valance, matching deck 1's.


# ============================================ DECK 2 — runs the FULL length
c.add("Deck2_LeftArm", x=0, y=DECK2_Y, z=0, sx=TOWER_D, sy=T_DECK, sz=HANG_Z0)
c.add("Deck2_RightArm", x=R_X0, y=DECK2_Y, z=T_Z0, sx=TOWER_D, sy=T_DECK, sz=HANG_Z0 - T_Z0)
c.add("Deck2_Back", x=0, y=DECK2_Y, z=HANG_Z0, sx=DIV_X, sy=T_DECK, sz=HANG_D)
c.add("Deck2_Back", x=DIV_X + T, y=DECK2_Y, z=HANG_Z0,
      sx=NICHE_W - DIV_X - T, sy=T_DECK, sz=HANG_D)

c.add("Cleat_D2_SideL", x=0, y=DECK2_Y - CLEAT_T, z=HANG_Z0,
      sx=CLEAT_W, sy=CLEAT_T, sz=HANG_D - CLEAT_W)
c.add("Cleat_D2_SideR", x=NICHE_W - CLEAT_W, y=DECK2_Y - CLEAT_T, z=HANG_Z0,
      sx=CLEAT_W, sy=CLEAT_T, sz=HANG_D - CLEAT_W)
c.add("Cleat_D2_Back", x=0, y=DECK2_Y - CLEAT_T, z=HANG_Z1 - CLEAT_W,
      sx=DIV_X, sy=CLEAT_T, sz=CLEAT_W)
c.add("Cleat_D2_Back", x=DIV_X + T, y=DECK2_Y - CLEAT_T, z=HANG_Z1 - CLEAT_W,
      sx=NICHE_W - DIV_X - T, sy=CLEAT_T, sz=CLEAT_W)


# ======================================================== LED (bought, not cut)
# With the valance gone the channel surface-mounts on the UNDERSIDE of deck 1's
# back panel, set back 40mm from the front edge and inset clear of the cleats.
c.fixture("LED_Channel", x=45, y=DECK1_Y - 16, z=HANG_Z0 + 40,
          sx=DIV_X - 45, sy=16, sz=16,
          note="aluminium channel + warm-white strip, under deck 1")
c.fixture("LED_Channel", x=DIV_X + T, y=DECK1_Y - 16, z=HANG_Z0 + 40,
          sx=NICHE_W - DIV_X - T - 45, sy=16, sz=16,
          note="aluminium channel + warm-white strip, under deck 1")
c.fixture("LED_Channel", x=TOWER_D - 16, y=DECK1_Y - 16, z=0,
          sx=16, sy=16, sz=ENTRY_Z, note="over the entry zone, under deck 1")


# ===================== L-BRACKETS carrying the decks over the open entry zone
# Replaces the deleted end panel (user: leave the entry open). Heavy-duty
# shelf brackets screwed to the left wall — the 350mm arm supports the deck's
# full depth, which a 40mm cleat could not.
for deck_y in (DECK1_Y, DECK2_Y):
    for z in (80, 300):
        c.fixture("L_Bracket", x=0, y=deck_y - 300, z=z, sx=350, sy=300, sz=40,
                  note="heavy-duty wall bracket, 350mm arm — carries the deck arm "
                       "over the open entry zone")


# ==================================================================== output
spec = c.spec()

project = "Master Bedroom Walk-In Closet"
rev = "SCREWS variant — melamine board, confirmat throughout"
style = "frameless_permanent"   # screws + glue; not knock-down

# 24 expected overlap flags, ALL of them the grooved drawer bottoms: 6 bottoms
# x (2 sides + 2 front/back). The box-only model cannot represent a groove, so
# a bottom sized to sit IN the groove necessarily reads as penetrating the
# parts that hold it. Verified there is nothing else in the list.
expected_overlaps = 24

# Regenerate the whole package in one command: package.py honours these.
elevation_walls = ["left", "right", "back"]


def _drawer_sheet(spec, outdir):
    import os
    _here = os.path.dirname(os.path.abspath(__file__))
    if _here not in sys.path:
        sys.path.insert(0, _here)
    import drawers
    return drawers.build(spec, outdir)


extra_outputs = [_drawer_sheet]

_BAND_FRONT = ["L_Side", "R_Side", "Upright", "Upright_Back",
               "L_Bottom", "R_Bottom", "L_Shelf", "R_Shelf",
               "Upright_Div",
               "Deck1_LeftArm", "Deck1_RightArm", "Deck1_Back",
               "Deck2_LeftArm", "Deck2_RightArm", "Deck2_Back"]
# BANDING AUDIT — only edges a person can actually see.
# "front" bands a LENGTH edge; "w1" bands a WIDTH edge. Which one is correct
# depends on the part's proportions, so it is checked per part, not assumed:
#   * Uprights are 370 deep x 325 tall — the visible vertical edge is the 325
#     one, i.e. a WIDTH edge. Banding "front" here would band the 370 edge,
#     which is buried between deck 1 and deck 2.
#   * Deck arms are open-ended where their run stops (left run at Z=0, right
#     run at Z=400), so they need the end banded as well as the long edge.
# Everything hidden — cleats, drawer boxes, panel backs against a wall, ends
# butting another panel — gets nothing.
banding = {n: ["front"] for n in _BAND_FRONT}
banding["Upright"] = ["w1"]            # visible edge is the 325 height
banding["Upright_Div"] = ["w1"]        # ditto
for _arm in ("Deck1_LeftArm", "Deck1_RightArm", "Deck2_LeftArm", "Deck2_RightArm"):
    banding[_arm] = ["front", "w1"]    # long edge + the open end of the run
banding["L_DrawerFront"] = ["all"]
banding["R_DrawerFront"] = ["all"]

# VARIANT: screws throughout. _CAM -> confirmat (what confirmats are FOR:
# screwing into a chipboard panel edge). _DOW -> "none": the coplanar deck
# butts are aligned and carried by the wall cleats below them, and the ply
# drawer boxes are glued + pinned in a jig. Result: zero cams, zero dowels.
_CAM, _DOW, _SCR = "confirmat", "none", "confirmat"
joint_overrides = {}
for tag in ("L", "R"):
    joint_overrides.update({
        (f"{tag}_Bottom", f"{tag}_Side"): _CAM,
        (f"{tag}_Shelf", f"{tag}_Side"): _CAM,
        (f"{tag}_ShoeShelf", f"{tag}_Side"): _CAM,
        (f"{tag}_BoxFB", f"{tag}_BoxSide"): _DOW,
        (f"{tag}_BoxBottom", f"{tag}_BoxFB"): "none",
        (f"{tag}_BoxBottom", f"{tag}_BoxSide"): "none",
    })
joint_overrides.update({
    # decks onto carcass members
    ("Deck1_LeftArm", "L_Side"): _CAM,
    ("Deck1_RightArm", "R_Side"): _CAM,
    ("Deck1_LeftArm", "Upright"): _CAM,
    ("Deck1_RightArm", "Upright"): _CAM,
    ("Deck2_LeftArm", "Upright"): _CAM,
    ("Deck2_RightArm", "Upright"): _CAM,
    ("Deck1_Back", "Divider"): _CAM,
    ("Deck1_Back", "Upright_Back"): _CAM,
    ("Deck2_Back", "Upright_Back"): _CAM,
    ("Deck1_Back", "Upright_Div"): _CAM,
    ("Deck2_Back", "Upright_Div"): _CAM,
    ("Upright", "Upright_Div"): "none",
    ("Upright_Back", "Upright_Div"): "none",
    ("Cleat_D2_SideL", "Upright_Div"): "none",
    ("Cleat_D2_SideR", "Upright_Div"): "none",
    ("Cleat_D2_Back", "Upright_Div"): "none",
    # coplanar butt joints between deck panels
    ("Deck1_Back", "Deck1_LeftArm"): _DOW,
    ("Deck1_Back", "Deck1_RightArm"): _DOW,
    ("Deck2_Back", "Deck2_LeftArm"): _DOW,
    ("Deck2_Back", "Deck2_RightArm"): _DOW,
    ("Deck1_Back", "Deck1_Back"): _DOW,
    ("Deck2_Back", "Deck2_Back"): _DOW,
    # valance
    # screwed onto wall cleats
    ("Cleat_D1_SideL", "Deck1_Back"): _SCR,
    ("Cleat_D1_SideR", "Deck1_Back"): _SCR,
    ("Cleat_D1_Back", "Deck1_Back"): _SCR,
    ("Cleat_D2_SideL", "Deck2_Back"): _SCR,
    ("Cleat_D2_SideR", "Deck2_Back"): _SCR,
    ("Cleat_D2_Back", "Deck2_Back"): _SCR,
    ("ShoeCleat_Back", "ShoeShelf"): _SCR,
    ("ShoeCleat_Left", "ShoeShelf"): _SCR,
    ("Divider", "ShoeShelf"): _SCR,
    # merely abutting — each independently fixed to the wall/structure
    ("Cleat_D1_SideL", "L_Side"): "none",
    ("Cleat_D1_SideR", "R_Side"): "none",
    ("Cleat_D1_SideL", "Cleat_D1_Back"): "none",
    ("Cleat_D1_SideR", "Cleat_D1_Back"): "none",
    ("Cleat_D2_SideL", "Cleat_D2_Back"): "none",
    ("Cleat_D2_SideR", "Cleat_D2_Back"): "none",
    ("Cleat_D1_Back", "Divider"): "none",
    ("Cleat_D2_Back", "Upright_Back"): "none",
    ("Cleat_D1_SideL", "Divider"): "none",
    ("Cleat_D2_SideL", "Upright_Back"): "none",
    ("Cleat_D2_SideR", "Upright_Back"): "none",
    ("Upright", "Cleat_D2_SideL"): "none",
    ("Upright", "Cleat_D2_SideR"): "none",
    ("Divider", "ShoeCleat_Back"): "none",
    ("ShoeCleat_Back", "ShoeCleat_Left"): "none",
    ("Upright", "Upright_Back"): "none",
    ("Upright_Back", "Upright_Back"): "none",
})

notes = {
    "L_DrawerFront": "SHAKER — 18mm MDF, CNC-routed 50mm frame, lacquered, banded all round",
    "R_DrawerFront": "SHAKER — 18mm MDF, CNC-routed 50mm frame, lacquered, banded all round",
    "Deck1_Back": "600 deep — valance rail stiffens the front edge",
    "Deck2_Back": "600 deep — carried by the three back uprights",
}

if __name__ == "__main__":
    from carcass import check_overlaps, cutlist_parts
    print(f"parts: {len(spec['parts'])}")
    flags = check_overlaps(spec)
    print(f"overlap flags: {len(flags)}")
    for f in flags:
        print("   ", f)
    for p in sorted(cutlist_parts(spec), key=lambda p: (-p["qty"], p["name"])):
        print(f"  {p['qty']:>2}x {p['name']:<16} {p['length']:>5} x {p['width']:>4}  {p['material']}")


