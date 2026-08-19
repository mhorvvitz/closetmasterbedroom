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
T = 17                 # supplier board: coloured melamine 17mm, 2440x1220
T_DECK = 17            # only 17mm available in colour — see DECK_RAIL below
T_TRIM = 17            # shaker trim from 17mm offcuts
GROOVE = 6             # drawer-bottom groove depth
TRIM_W = 50            # shaker frame width
MAT = "melamine"       # melamine-faced board, oak decor — carcass AND fronts
PLY = "plywood_birch"  # drawer boxes

NICHE_W, NICHE_H, NICHE_D = 1650, 2600, 1600

ENTRY_Z = 400                   # front zone kept clear (left wall)
T_Z0, T_Z1 = 400, 1000          # tower footprint along Z — both sides
HANG_Z0, HANG_Z1 = 1000, 1600   # hanging zone, 600 deep
TOWER_D, TOWER_H = 370, 2250   # sides run FLOOR -> DECK 2 in one piece (2250 < 2440 sheet)
TOWER_CLEAR = (T_Z1 - T_Z0) - 2 * T          # 564
R_X0 = NICHE_W - TOWER_D                     # 1280

DIV_X = 807                     # hanging divider, left face
DECK1_Y, DECK2_Y = 1900, 2250   # deck 2 raised too, to keep the upper bays equal
UPRIGHT_H = 0   # no separate uprights: the side panels are continuous

ROD_Z = 1289                    # → centreline Z 1300 (300 from the back wall)
ROD_Y_HIGH, ROD_Y_LOW = 1839, 889            # → centrelines 1850 / 900
#   double-hang upper drop = 1850 - 900 = 950  (was 840 — open question 3 closed)

CLEAT_W, CLEAT_T = 40, 17

c = Carcass(NICHE_W, NICHE_H, NICHE_D, t=T, material=MAT,
            name="Master Bedroom Walk-In Closet")


# ================================================ LEFT RUN — OPEN AT THE FRONT
# No end panel (user): the entry zone stays fully open. Both deck arms are
# carried over it by wall-mounted L-brackets — see the fixtures at the bottom.


# ================================================ TOWERS — IDENTICAL BOTH SIDES
SHOE_Y = (150, 285, 420)
SHELF_Y = (555, 799, 1043, 1287, 1530, 1900)   # 1900 = the old deck-1 level

# rev K was a misread — the shelves to remove were the bracketed ones over the
# ENTRY zone, not a tower shelf. Both towers are identical again (decision 5).
SHELF_BY_TAG = {"L": SHELF_Y, "R": SHELF_Y}
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
    for y in SHELF_BY_TAG[tag]:
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

# (user, rev N) Two blocks at the base of the divider, one each face, instead of
# a full-height wall cleat. Holding the tip converts the bottom of the divider
# from a cantilever (L^3/3EI) into a span (L^3/48EI) — 16x stiffer over the same
# 900mm, and the base can no longer creep sideways, which is the failure that
# actually matters over years. Each block is two 17mm offcuts glued to 34.
# (rev O) Floor is tiled, so the blocks fix to the BACK WALL instead: moved back
# to sit against it (z 1450..1600) and made 120 tall to take two wall screws.
BLOCK_L, BLOCK_H = 150, 120
BLOCK_Z = HANG_Z1 - BLOCK_L
for _bx in (DIV_X - 2 * T, DIV_X - T, DIV_X + T, DIV_X + 2 * T):
    c.add("DividerBlock", x=_bx, y=0, z=BLOCK_Z, sx=T, sy=BLOCK_H, sz=BLOCK_L,
          note="glue in pairs -> 2 blocks of 34; screw to the BACK WALL (2 fixings "
               "each) and to the divider face with 4x40 — no floor fixing, tiles")

c.rod(y=ROD_Y_HIGH, x0=0, x1=DIV_X, z=ROD_Z)              # long hang
c.rod(y=ROD_Y_HIGH, x0=DIV_X + T, x1=NICHE_W, z=ROD_Z)    # double hang, upper
c.rod(y=ROD_Y_LOW, x0=DIV_X + T, x1=NICHE_W, z=ROD_Z)     # double hang, lower

# (user, rev L) Hooks go in the ENTRY zone, on the left wall, where the two
# bracketed deck shelves used to overhang. Nothing above them now, so a coat
# hangs its full length.
for _hz in (90, 200, 310):
    c.fixture("Hook", x=0, y=1700, z=_hz, sx=55, sy=55, sz=40,
              note="wall hook in the entry zone — bought; 3 off")

# (user, rev M) The low shoe shelf and its two cleats are deleted from the
# long-hang bay — a bought shoe rack is more space-efficient than a fixed
# 300-deep shelf. The bay floor is now clear: 807 wide x 600 deep, with about
# 500mm of headroom before the hanging garments start (rod at 1850, longest
# dress ~1330). Buy to that envelope.

# ============================================ DECK 1 — runs the FULL length
# (user, rev L) NOTHING overhangs the entry zone any more. The deck-1 piece
# that used to cantilever out over it on L-brackets is deleted, and deck 2's
# arm now stops at the tower. The entry reads as fully open from floor to
# ceiling, with hooks on the wall.
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


# ================================ NO UPRIGHTS — the panels run through instead
# (user, rev J) The tower sides and the hanging divider now run FLOOR to DECK 2
# in one 2250mm piece, which fits the 2440 sheet with 190 to spare. That deletes
# 4 uprights + 1 upright-over-divider and the 5 cuts that went with them, and
# replaces two butt joints per panel with continuous material — stiffer, and
# nothing to align on top of a panel edge.
#
# Consequence: deck 1 can no longer run over the towers as one arm, because the
# side panels now pass through that level. Inside each tower it is simply the
# top shelf (y=1900 was added to SHELF_Y, so it merges with the existing shelf
# row rather than adding one). Only the open entry zone still needs a separate
# deck-1 piece, and the right run needs none at all.
UP_Y = DECK1_Y + T_DECK


# ============================================ DECK 2 — runs the FULL length
c.add("Deck2_LeftArm", x=0, y=DECK2_Y, z=T_Z0, sx=TOWER_D, sy=T_DECK,
      sz=HANG_Z0 - T_Z0, note="stops at the tower — no overhang over the entry")
c.add("Deck2_RightArm", x=R_X0, y=DECK2_Y, z=T_Z0, sx=TOWER_D, sy=T_DECK, sz=HANG_Z0 - T_Z0)
c.add("Deck2_Back", x=0, y=DECK2_Y, z=HANG_Z0, sx=NICHE_W, sy=T_DECK, sz=HANG_D,
      note="ONE panel across the full 1650 — the divider tops out at 2250 so "
           "deck 2 lands on it rather than butting either side of it")

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


def _project_path():
    import os
    _here = os.path.dirname(os.path.abspath(__file__))
    if _here not in sys.path:
        sys.path.insert(0, _here)


def _sheets(spec, outdir):
    """Hardware first — it reads assembly.md and cutlist.json, both of which
    package.py has already written by the time extra_outputs runs."""
    _project_path()
    import costing
    import hardware
    import drawers
    return (hardware.build(spec, outdir)
            + costing.build(spec, outdir)
            + drawers.build(spec, outdir))


def _render(spec, outdir):
    """Our presentation render, run INSTEAD of the stock one."""
    _project_path()
    import render_scene
    return render_scene.build(spec, outdir)


extra_outputs = [_sheets]

# Run our renderer in place of package.py's. Before skill PR #3 there was no way
# to do this: writing render.html afterwards meant the next plain package.py run
# silently overwrote it, which went unnoticed here for ten revisions.
replaces = {"render": _render}

# The packet is built last now, so sheets produced above can go into it.
packet_docs = ["cutlist.md", "assembly.md", "drawers.md", "hardware.md", "cost.md"]

_BAND_FRONT = ["L_Side", "R_Side",
               "L_Bottom", "R_Bottom", "L_Shelf", "R_Shelf",
               # restored: these four were lost in an earlier edit and shipped
               # unbanded for one revision. All are plainly visible.
               "L_ShoeShelf", "R_ShoeShelf", "Divider",
               "Deck1_Back",
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
for _arm in ("Deck2_LeftArm", "Deck2_RightArm"):
    banding[_arm] = ["front", "w1"]    # long edge + the open end of the run
banding["L_DrawerFront"] = ["all"]
banding["R_DrawerFront"] = ["all"]
# Applied shaker frame — the trim sits ON the face, so BOTH long edges of every
# piece show: the outer one at the panel perimeter and the inner one around the
# recess. The RAILS run the full width, so their two short ends land on the
# panel's side edges and show as well; the STILES butt into the rails, so their
# ends are hidden.
for _t in ("L", "R"):
    banding[f"{_t}_ShakerRail"] = ["all"]     # 2 long + 2 ends
    banding[f"{_t}_ShakerStile"] = ["long"]   # 2 long only; ends are covered

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
    # --- new adjacencies created by running the panels floor->deck 2 (rev J) ---
    ("Deck2_LeftArm", "L_Side"): _SCR,    # deck 2 now lands on the tower side
    ("Deck2_RightArm", "R_Side"): _SCR,
    ("Deck1_Back", "L_Side"): _SCR,       # back panel butts the side's edge
    ("Deck1_Back", "R_Side"): _SCR,
    ("Cleat_D2_SideL", "L_Side"): "none",  # cleat is wall-fixed; merely abuts
    ("Cleat_D2_SideR", "R_Side"): "none",
    ("Cleat_D2_Back", "Divider"): "none",  # divider now reaches the deck-2 cleat
    # deck 2 now crosses OVER the divider in one piece and lands on its top edge
    ("Deck2_Back", "Divider"): _SCR,
    ("DividerBlock", "Divider"): _SCR,      # 4x40 screws, see the part note
    ("DividerBlock", "DividerBlock"): "none",   # glued face to face
    ("Deck1_Back", "Divider"): _CAM,
    # coplanar butt joints between deck panels
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
    # merely abutting — each independently fixed to the wall/structure
    ("Cleat_D1_SideL", "L_Side"): "none",
    ("Cleat_D1_SideR", "R_Side"): "none",
    ("Cleat_D1_SideL", "Cleat_D1_Back"): "none",
    ("Cleat_D1_SideR", "Cleat_D1_Back"): "none",
    ("Cleat_D2_SideL", "Cleat_D2_Back"): "none",
    ("Cleat_D2_SideR", "Cleat_D2_Back"): "none",
    ("Cleat_D1_Back", "Divider"): "none",
    ("Cleat_D1_SideL", "Divider"): "none",
})

_DECK_LOAD = ("600 deep, free front edge over 807/826mm span. "
              "LOAD LIMIT ~15kg per panel sustained (approx 3-4 boxes of "
              "folded clothes). 17mm board is ~3x less stiff than the 25mm "
              "this was originally drawn at, and the rail that would have "
              "stiffened it was deliberately omitted — see docs/spec.md 10b.")

notes = {
    "L_DrawerFront": "SHAKER — 17mm coloured melamine base + applied 17mm frame; "
                     "banded all four edges",
    "R_DrawerFront": "SHAKER — 17mm coloured melamine base + applied 17mm frame; "
                     "banded all four edges",
    "L_ShakerRail": "applied trim, cut from offcuts of the same board",
    "R_ShakerRail": "applied trim, cut from offcuts of the same board",
    "L_ShakerStile": "applied trim, cut from offcuts of the same board",
    "R_ShakerStile": "applied trim, cut from offcuts of the same board",
    "Deck1_Back": _DECK_LOAD,
    "Deck2_Back": _DECK_LOAD + " Top deck — seasonal storage only.",
    "Divider": "grain vertical; front edge banded — it is the most visible "
               "single edge in the room",
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








