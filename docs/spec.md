# Master Bedroom Walk-In Closet — Project Record

**Rev C** — 2026-08-15. Deck 1 raised to 1900 (closing the double-hang problem),
the left run's front end left **open** on L-brackets, presentation render added.
Rev B corrected the shell against the architectural floor plan
(the architect's construction drawing (not published in this repo)). Rev A was reverse-engineered from
`Master Closet V2` (SketchUp, 30 Nov 2025).
**Units:** millimetres (mm) throughout.

---

## Brief

A built-in **U-shaped walk-in closet** in a recessed room off the master bedroom.
Frameless, no doors, melamine carcasses with shaker drawer fronts and LED lighting.

- **Left wall run (1600 deep)** — first 400 kept **empty and fully open** for
  entry and the laundry basket (no end panel; the decks are carried over it on
  wall L-brackets); then a 600-long tower; then hanging.
- **Right wall run (1200 deep)** — a 600-long tower, then hanging. Starts 400
  further back than the left run, per the floor plan.
- **Both towers are identical**: shoe shelves low, three shaker drawers in the
  middle, open shelving above.
- **Back / hanging zone (600 deep, full 1650 width)** — split by a centre
  divider: long-hang left, double-hang right. Low shelf in the long-hang bay.
- **Two open decks above**, both running the **full length** of all three runs.
- **LED strip** under deck 1.

**Construction style: `frameless_kd`** — 18 mm melamine, System-32, knock-down
cam-and-dowel carcasses, assembled in the room.

---

## How these numbers were obtained

The SketchUp share link is a read-only viewer with no export, so **no dimension
here was read off a screen or a photo**. The model was exported as a binary STL
(338,450 triangles) and parsed directly: triangles welded into 503 connected
solids, all axis-aligned faces bucketed by plane, coplanar faces re-assembled
into rectangles. Model units were centimetres (×10 → mm).

The **floor plan is authoritative** for the shell and overrides the model where
they differ. The plan confirms the 1650 width the STL gave; it corrects the left
run's depth from the 1700 the model showed to **1600**.

### Coordinate datum

| Axis | Origin | Direction |
|---|---|---|
| **X** | inside face of the **left** side wall | → toward the right wall (width) |
| **Y** | finished **floor** | → up (height) |
| **Z** | front of the **left wall run** | → toward the back wall (depth) |

---

## Measurements

### The shell — from the floor plan (authoritative)

| Dimension | Value (mm) | Source | Note |
|---|---:|---|---|
| Clear width, wall to wall (X) | **1650** | plan + model (agree) | plan reads "165" |
| Depth, **left** wall run (Z) | **1600** | plan / user | Z 0…1600 |
| Depth, **right** wall run (Z) | **1200** | plan / user | Z 400…1600 — starts 400 back |
| Clear height, floor to ceiling (Y) | **2600** | **confirmed by user** | was model-derived; now confirmed |
| Entry zone kept clear (left run, front) | **400** | user | Z 0…400, laundry basket lives here |

### Shell cross-check against the floor plan (rev D)

The plan dimensions the width as **128 + 37 = 165**. That confirms the model
independently:

| Plan | Model | Meaning |
|---|---|---|
| 128 | X 0…1280 | the portion of the width at the **full 1600** depth |
| 37 | X 1280…1650 | a **370-wide strip** at only **1200** depth |
| 37 = tower depth | right tower is 370 deep | **the right tower's front face lands flush with the wall step at Z = 400** |
| 120 / 160 | Z 400…1600 / 0…1600 | the two run depths |
| 165 | X 0…1650 | total width |

Further shell features read off the plan (render context only — no cut part
depends on them):

| Feature | Value | Note |
|---|---|---|
| Bathroom wall — straight run before it angles | **370** | the "37"; ends at the step corner (X 1280, Z 400) |
| Diagonal bathroom wall | 45° from that corner, **800 solid before the door** | the "80" — corrected rev E; it is wall length, not the whole diagonal |
| Bathroom door | **700** wide × **2100** high, starting at 800 along the diagonal | the "70" / "210"; has a swing leaf |
| Entrance doorway | 750 wide, **no door leaf** | cased opening (user) |

Diagonal geometry, from the step corner (X 1280, Z 400) at 45°:

| Along the diagonal | X, Z | What |
|---|---|---|
| 0 | 1280, 400 | step corner — where the 370 straight run ends |
| 0 → 800 | to 714, −166 | solid wall |
| 800 → 1500 | to 219, −661 | the 700 bathroom door |

### Depth zoning — both side walls

| Zone | Z range | Depth | Contents |
|---|---|---:|---|
| Entry | 0 … 400 | 400 | empty (left run only) |
| Towers | 400 … 1000 | **600** | identical tower each side |
| Hanging | 1000 … 1600 | **600** | full width, centre divider |

600 + 600 = 1200 = the right wall run exactly. 400 + 600 + 600 = 1600 = the left. ✓

### Closet joinery

| Element | Value (mm) | Source |
|---|---:|---|
| Tower depth (projection from its wall) | 370 | measured (model) |
| Tower length along Z | 600 outer / 564 clear | user constraint |
| Tower height | **1900** | rev C — follows deck 1 |
| Walkway between tower faces | **910** | derived (1650 − 2×370) |
| Drawer bay clear height | 226 | measured (model) |
| Shoe shelf bay clear heights | 132 / 117 / 117 / 117 | measured (model), rationalised |
| Hanging divider | 18 × 600 deep × 1900 tall, at X 807…825 | derived (centred) |
| Rod centreline, from back wall | **300** (Z = 1300) | standard for 600-deep hanging |
| Rod height — upper (both bays) | **1850** | rev C — 50 below deck 1 |
| Rod height — lower (right bay) | 900 | measured (model) |
| Low shelf, long-hang bay | Y 150, 300 deep | measured (model) |
| Deck 1 underside | **1900** | rev C — user choice (option 3) |
| Deck 2 underside | **2250** | rev C — raised to keep the upper bays equal |
| Clear bay, deck 1 → deck 2 | 332 | derived |
| Clear above deck 2 to ceiling | 332 | derived |
| Panel thickness | **18** | standard |

### Ergonomic / standard values

| Item | Value (mm) | Source |
|---|---:|---|
| Hanging depth (shoulder) | 600 | standard — **met exactly** |
| Walk-in clearance | 900–1100 | standard — 910 achieved |
| Long-hang drop (left bay) | **1850** | derived |
| Double-hang drop, upper | **950** | derived — **meets the standard** (was 840 in rev B) |
| Double-hang drop, lower | 900 | derived |
| Scribe/filler allowance per wall | 10 | standard (built-in) |

---

## Decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | Carcass: 18 mm melamine-faced board, oak woodgrain decor | Israeli closet standard; the model's oak look is a decor film, not veneer. |
| 2 | Thickness normalised to 18 mm (model mixed 18/20) | Stock thickness and the System-32 basis; one thickness through the cut list. |
| 3 | ~~Construction `frameless_kd`, cam-and-dowel~~ → **SUPERSEDED by 3a** | Carcasses go in flat and are squared in the room. |
| 3a | **Confirmat screws throughout — zero cams, zero dowels** (rev H, user) | Confirmats are made for exactly this: screwing into a chipboard panel edge. Removes the alignment-critical work — a dowel pair 0.5 mm out and the panel will not close, whereas a confirmat pilot is drilled through the first panel into the second *in situ*, so it self-aligns. Drilling operations drop **358 → 246**, and three bits leave the tool list (Ø8 brad-point, Ø8 with depth stop, Ø15 Forstner). Connectors go from 48 cams + 28 dowels + 11 confirmats to **59 confirmats**. Also marginally cheaper. |
| 3b | Coplanar deck butt joints: no fastener — they rest on the wall cleats | The cleats already carry and align them; a dowel there was solving a problem that does not exist. |
| 3c | Drawer boxes: glued + pinned in a jig, not dowelled | Standard for a small ply box, and a 7 mm confirmat body is too big for a 15 mm ply side. |
| 3d | Trade-offs accepted: no longer knock-down, and screw heads need caps | Disassembly only matters if the closet moves house. Caps are decor-matched; the base design already used caps on the cam housings. |
| 4 | No back panels on the towers | Matches the model; racking resisted by fixing to the wall. |
| 5 | **Both towers identical** — same 600 length, same shelf grid, same 3 drawers | User instruction. Also fixes rev A's problem that the two runs' shelf lines missed each other by ~90 mm across a 910 walkway. |
| 5a | ~~LEFT tower drops its 1530 shelf~~ — **REVERTED at rev L.** Rev K removed the wrong shelf: the ones meant were the bracketed overhangs at the end of the left run, not a tower shelf. Both towers are identical again. |
| 5b | **Bracketed overhangs over the entry deleted** (rev L, user) | The two deck pieces that cantilevered over the entry zone, plus all **4 L-brackets** and the LED channel under them, are gone. Deck 2's arm now stops at the tower. The entry reads clear floor-to-ceiling, with **3 hooks on the left wall at Y 1700** (Z 90/200/310) — nothing above them, so a coat hangs its full length, which the old deck at 1900 prevented. |
| 5c | **Deck 2's back is ONE 1650 × 600 panel crossing over the divider** (rev L, user) | Possible only because the divider tops out at 2250 (decision 5c on continuous panels), so deck 2 lands on its top edge instead of butting either side. No seam. Deck 1 at 1900 still needs two panels — the divider passes through that level. |
| 5d | **Low shoe shelf in the long-hang bay deleted** (rev M, user) | A bought rack is more space-efficient than a fixed 300-deep shelf. Removes the shelf and its two cleats. Bay floor now clear at **807 × 600**, with **≈ 500 mm** of height before the hanging garments — see the envelope in `hardware.md`. |
| 5e | **Two blocks at the base of the divider** (rev N, user) — chosen over a full-height wall cleat | The divider was restrained at 900 / 1850 / 1900 / 2250 but **free below 900** and fixed to neither wall nor floor: a 900 mm cantilever at **0.33 mm/N** (a 5 kg shove moved the base 16 mm), with nothing to stop it creeping sideways over years. Holding the base converts that cantilever into a span — L³/3EI becomes L³/48EI, **16× stiffer** at **0.021 mm/N** — and even discounting the lower rod entirely it is still 2× better. Two blocks, each two 17 mm offcuts glued to 34, screwed to the floor and to the divider face. |
| 5f | Blocks screwed with **4 × 40, not confirmat** | A 7 mm confirmat body would split a 17 mm block. |
| 5c | **Panels run floor → deck 2 in one 2250 piece** (rev J, user: minimise cuts) | 2250 fits the 2440 sheet with 190 to spare. Deletes 4 uprights + the upright-over-divider and their 5 cuts, and replaces two butt joints per panel with continuous material. Consequence: deck 1 can no longer cross the towers as one arm — inside each tower it is simply the top shelf (y=1900 added to the shelf list, so it merges with the existing shelf row instead of adding one), and only the open entry zone keeps a separate deck-1 piece. |
| 6 | **Wire baskets dropped**, replaced by drawers matching the left | Follows from decision 5. Baskets can still be added later in the open bays. |
| 7 | **Drawer fronts: melamine base panel + applied shaker frame trim, all in the same oak decor as the shelves** (rev D, user) | Wood-coloured to match, so MDF-and-lacquer is out. Each front is an 18 mm melamine panel (594 × 220) with a 10 mm × 50 mm applied frame — 2 rails full width, 2 stiles between — glued and pin-nailed, then a bar pull. 6 fronts, 3 per side, identical. MDF leaves the job entirely. |
| 7a | Bar pulls, 160 mm centres | User asked for pulls. Bought item; 6 off. |
| 8 | Both decks run the **full length** of all three runs | User instruction. |
| 9 | Deck back panels are 600 deep, split at the divider | Matches the hanging depth so the shelf covers what's below it. Split keeps each panel handleable and lands the joint on the divider. |
| 10 | ~~All deck panels 25 mm~~ → **SUPERSEDED by 10b** | Was: 25 mm carries the 807/826 front-edge span unaided, so no valance is needed. |
| 10b | **Board is 17 mm throughout** — supplier's coloured melamine, ₪280/sheet incl. cutting (rev I, user) | The colour is only made in 17 mm. Every internal dimension re-derives: tower clear **566**, drawer box **540**, upright height **333**, deck 1 top **1917**. |
| 10c | **Deck load limit accepted rather than re-stiffened** (rev I, user — option 3) | 17 mm is (25/17)³ ≈ **3.2× less stiff** than the 25 mm this was drawn at, and the stiffening rail was deliberately removed at rev D. Offered three fixes — 25 mm in colour, reinstate the rail, or accept — and **accept** was chosen. Consequence is now carried as a stated load limit rather than a hidden risk. |
| 10d | **The 12 mm white board quoted on 2026-08-20 is not adopted** (Alfandari No 51/040609, ₪225/sheet) | It is a different material, not a cheaper price for the same one. 12 mm re-derives every internal dimension, is (17/12)³ ≈ **2.8× less stiff** than 17 mm — which would drop the deck limit of decision 10c from ~15 kg to roughly **5 kg** per back panel — cannot take a 7 mm confirmat, and is white rather than the chosen colour. The board line stays at ₪280 for 17 mm coloured; the quote's **banding** line is adopted. Full record: `Suppliers/quote-2026-08-20-alfandari.md`. |
| 10a | LED channel moves to the **underside of deck 1's back panel**, set back 40 mm from the front edge | Its old home was the valance. Surface-mounted channel, inset in X clear of the wall cleats. |
| 11 | **One** divider only between the decks over the hanging zone, on the centre line — a straight continuation of the hanging divider (rev C2, user) | The hanging zone reads as one clean opening from floor to deck 2, broken by a single vertical line. The quarter-point uprights I had at X 400 and 1200 are deleted. |
| 11a | Deck 2's span handled by its 25 mm thickness (rev D) | Supersedes the deck-2 valance from rev C2. Both upper bays are back to their full **325 mm** clear. |
| 12 | **No end panel** — the left run's front stays fully open (rev C, user) | Keeps the entry visually open. Both deck arms are carried over the 400 zone by **4 heavy-duty wall L-brackets** (350 mm arm, 2 per deck). A 40 mm wall cleat could not do this — it would leave the deck's 370 front edge cantilevered. |
| 12a | Deck 1 raised 1780 → **1900**, towers follow (rev C, user — option 3) | Closes the double-hang problem: upper drop goes 840 → **950 mm**, at the standard. Upper rods move to 1850. |
| 12b | Deck 2 raised 2182 → **2250** | Consequence of 12a, and my call: leaving deck 2 at 2182 would have squeezed the deck-1→deck-2 bay to 264 mm while 400 mm sat unused above. Now both upper bays are **332 mm**. Easy to revert if you prefer the taller top bay. |
| 13 | Wall cleats under both decks and the low shelf | **Not in the model.** Deck arms and back panels need bearing where no carcass sits under them. |
| 14 | Drawer boxes: 15 mm birch ply, side-mount ball-bearing runners, grooved bottoms | Standard, tolerant of a site-assembled carcass. |
| 15 | **LED**: aluminium channel + warm-white strip on the valance (both hanging bays) and under deck 1 over the entry zone | User instruction. Lights the clothes and the entry. Bought item, not a cut part. |
| 16 | All **50 touching part-pairs** carry an explicitly chosen joint | Cam-and-dowel for KD carcass joints, glued dowel for drawer boxes and coplanar deck butts, confirmat onto cleats, `none` where parts merely abut. Zero joints left to the script's default. |
| 17 | Grain/decor runs along each panel's longest dimension | Woodgrain decor — must be stated per part or the shop nests it wrong. |
| 18 | **Presentation render** built by a project-local emitter (`render_scene.py`), not the shared one | The shared emitter has no vocabulary for rooms or props. This one reads the *same* positioned-part spec, then adds two toggleable overlay groups: **context** (room shell + bathroom door) and **contents** (basket, shoes, boots, hat boxes, garments). Both are presentation-only — neither reaches the cut list, assembly plan or elevations, so a prop can never be mistaken for a part. Melamine is drawn in oak here to match your SketchUp. |
| 18a | Room shell drawn as **single-sided planes facing inward**, not solid slabs | A cutaway room: seen from outside, each wall's back face is culled, so the walls never stand between the camera and the closet. With solid boxes the model was unviewable from most of the orbit. |
| 18b | Idle camera **oscillates ±0.3 rad** around a hero angle instead of spinning freely | An unbounded spin drifted the opening view away within seconds and made the first impression arbitrary. |
| 18c | Render Z is **negated on the way into the scene** | three.js is right-handed with Y up, so a camera in front looking along +Z mirrors X — which put the long 1600 run on the viewer's right, disagreeing with the plan and elevations. Negating Z lets the camera look along −Z (standard) so +X lands on the viewer's right, matching how you walk in. Render-only; no dimension changed. |
| 18d | **Four** render toggles: room & door, contents, left tower, right tower (rev E, user) | Each tower can be hidden to see past it. Tower props (the shoes on its shelves) are tagged to the same run, so they hide with it and stay governed by Contents too. 99 objects per tower — identical counts, a useful check that the two runs really are the same. |
| 19 | **Board-finish swatches** in the render: oak / **sage green** / **light blue** / white / grey (rev G, user) | All melamine parts share one material, so one click re-finishes carcass, shelves, decks, drawer fronts and shaker trim together. The plywood drawer boxes and the metal rods/pulls deliberately do **not** follow. Finish is a decor choice; it changes nothing dimensional, so the cut list is unaffected. A `?finish=sage` URL parameter selects one on load, so a specific finish can be linked or captured. |
| 19a | **Pulls in brass / gold** (rev G, user) | Rendered as a true metallic (metalness 0.9, low roughness) rather than a painted colour, so they read as metal against any board finish. Six pulls; they hold the brass tone whichever finish is selected. |
| 20 | **Cost estimate is derived, not authored** — `costing.py` reads `output/cutlist.json` + `rates.json` | The estimate can never drift from the cut list. `rates.json` is the single authored price file; every number in it is an assumed market rate, clearly flagged, for replacement with real quotes. Labour is excluded. |
| 20a | **Quotes are transcribed into `Suppliers/`, and every rate that came from one carries a `_source`** | A price with no provenance is an assumption wearing a suit. `costing.py` reads the flag and marks each line **quoted** or *assumed* in `cost.md`, and lists the quotes on file, so the estimate says which half of itself is real. |

---

## Open questions — verify before cutting

1. ~~Ceiling height~~ — **CLOSED (rev E)**. 2600 confirmed by the user.
2. **Site-measure the niche**: width at 3 heights, both depths at 3 positions,
   and the diagonals. Walls are not square. Carry the 10 mm scribe allowance.
3. ~~Double-hang upper drop~~ — **CLOSED (rev C)**. Deck 1 raised to 1900, upper
   rods to 1850; upper drop is now 950 mm, lower 900 mm.
4. **DECK LOAD LIMIT — ~15 kg per back panel, sustained.**
   The two deck-back panels (807 × 600 and 826 × 600, 17 mm) have a free front
   edge and are supported on their other three sides. Estimate: simply-supported
   approximation (conservative — the three-edge support helps), creep-reduced
   modulus E ≈ 1200 N/mm² for sustained load in chipboard, deflection limit
   span/200 ≈ 4 mm. That gives ~17 kg; call it **15 kg**, roughly 3–4 boxes of
   folded clothes per panel. **This is an engineering estimate, not a certified
   figure.** Books, tools or stacked linen will exceed it. Deck 2 is seasonal
   storage only. Accepted knowingly at rev I — see decision 10c.
4a. **Deck 2's back panels are 600 deep at 2250 high** — hard to reach the back.
4a. **L-bracket load.** The two brackets per deck carry a 370 × 400 deck arm plus
   whatever sits on it. Specify brackets rated ≥ 50 kg each and fix into solid
   substrate — not plasterboard anchors. See open question 9.
5. **Construction style assumed** `frameless_kd` / 18 mm melamine. If the
   carpenter prefers permanent glued carcasses, the cut list widths change.
6. **Rod diameter assumed** 25 mm oval / 32 mm round. The model draws a 40 mm
   placeholder. Confirm with the supplier.
7. **Shaker front detail**: specified as one-piece routed MDF. A 5-piece applied
   frame is the alternative — confirm which your shop does.
8. **Board decor, lacquer colour, and edge-banding colour** to confirm.
8a. ~~Is cutting included in the board price?~~ — **CLOSED (2026-08-20, user)**.
   It is, on both quotes, even though the 2026-08-20 sheet shows no separate
   cutting line. Sheet prices are cut-to-list prices.
8b. ~~Edge-banding unit~~ — **CLOSED (2026-08-20, user)**. The quote's 62 × ₪8
   is **per metre**: 55.9 m plus the 10% waste allowance. It is not a part
   count — no count in the job lands on 62 (72 melamine parts, 60 carrying a
   banding instruction, 36 without the shaker trim, 116 banded edges).
9. **Wall substrate** for the cleats and wall fixings — concrete/block vs
   plasterboard needs entirely different anchors.
10. **Floor level.** If out of level, the towers need levelling feet or a
    scribed plinth.

---

## Derivation chain

```
docs/spec.md  (this file — authored inputs, source of truth)
     │
     ▼
closet_spec.py  (positioned-part spec via scripts/carcass.py)
     │
     ├─► plan.svg / front.svg            2D dimensioned views
     ├─► elev_{left,right,back}.svg      three wall elevations (elevations.py)
     ├─► render.html                     3D preview
     ├─► cutlist.{md,csv,xlsx,json}      cut list / BOM
     ├─► assembly.md                     drilling coords + build order
     ├─► hardware.md                     hardware schedule
     ├─► cost.md                         materials estimate  ◄── rates.json
     └─► packet.pdf                      the carpenter packet

Suppliers/quote-*.md  (transcribed supplier quotes) ──► rates.json _source
```

Three authored sources of truth: **this file** (design inputs), **`rates.json`**
(prices), and the skill's **`assets/joinery.json`** (drilling specs). Everything
else is derived. `Suppliers/quote-*.md` sits behind `rates.json`: it is evidence,
transcribed as received, not an input anything reads.

Regenerate after any change:

```bash
python C:\Users\mhorv\.claude\skills\furniture-design\scripts\package.py closet_spec.py --out output/ && python elevations.py
```
