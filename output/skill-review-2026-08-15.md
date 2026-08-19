# Skill review — furniture-design

**Project shape:** U-shaped built-in walk-in closet in a recessed room — three runs
of frameless casework, two towers with drawers, a hanging zone, two upper decks.
Reverse-engineered from an existing SketchUp model, then taken through the full
pipeline across 7 revisions.
**Date:** 2026-08-15

---

## P0 — verified bugs

### 1. `draw.plan()` labels the plan front-to-back backwards

`scripts/draw.py:147`

```python
def PZ(z): return pz0+(D-z)*s     # comment: "z=0 (back) at top, z=D (front) at bottom"
```

The code does the opposite of its comment. `PZ(0) = pz0 + D*s` is the **largest**
SVG y, i.e. the **bottom** of the page; `PZ(D) = pz0` is the **top**.

`carcass.py` defines the front as `Z = D` ("front face at Z=D", and `door()` uses
`zf = self.D  # overlay in front`). So a spec that follows the documented
convention gets its **front drawn at the top**, under a caption that reads
`"plan — front at bottom"` (`draw.py:150`).

**Impact:** every plan view is mirrored front-to-back relative to its own label.
Silent — it produces a plausible drawing, so it survives review.

**Fix:** either flip to `PZ(z) = pz0 + z*s`, or correct the comment and the
caption. Whichever — the two must agree, and a project should not have to derive
which one is lying.

### 2. Nothing catches an inverted depth axis

I built this project with `Z = 0` at the **front** and `Z = D` at the back — the
inverse of the documented convention — and nothing objected:

- `cutlist.py` passed (thickness/area are direction-agnostic)
- `check_overlaps` passed (relative geometry unchanged)
- `assembly.py` passed
- front elevations were unaffected (pure XY projection)
- the plan *looked* right, because bug #1 cancelled my inversion out

It only surfaced as a **mirrored 3D render**, and only because the client spotted
it: "Render is reversed, you have the right side with the extended deck."

The shipped `render.py` is **correct** under the documented convention
(`render.py:108` places the camera at `tgt.z + rad·sin(pol)·cos(az)` with
`az=-0.72`, so it sits at max-Z looking down −Z and +X lands on the viewer's
right). I had wrongly suspected it; reading the code cleared it.

**Fix:** a cheap `validate_spec()` lint, or make the convention unmissable at
the point of use. Two independent errors cancelling is the worst failure mode —
it hides both.

---

## P1 — capabilities that cost the most hand-built code

Roughly 600 lines of throwaway glue were written for this one project. Each item
below is code that already exists in working form and should be packaged.

### 3. No way to read an existing model (biggest single gap)

The SketchUp MCP is build-only, the web share link has no export, and there is no
`.skp` parser. Reverse-engineering the client's model meant asking for an STL
export and writing **five** analysis scripts from scratch:

| script | job |
|---|---|
| `stl_parts.py` | binary STL → triangles → union-find weld → connected solids + bboxes |
| `analyze.py` | spatial clustering, repeated-size signatures, panel/rod detection |
| `planes.py` | axis-aligned plane extraction → exact panel coordinates |
| `shell.py` | isolate the room shell, classify faces as FULL/HOLE |
| `rects.py` | coplanar faces → rectangles → paired into panels |

This recovered 338,450 triangles → 503 solids → an exact positioned-part spec,
and the width it derived (1650) was later confirmed independently by the
architectural floor plan.

**Proposal:** `scripts/import_mesh.py` — STL/OBJ/DAE → candidate positioned-part
spec. For anyone doing built-ins, starting from an existing model is the *normal*
case, not the exception.

### 4. No multi-run elevations

`draw.draw()` gives front + side; `draw.plan()` gives the plan. A U- or L-shaped
built-in — i.e. **every** walk-in, kitchen and corner wardrobe — needs one
elevation per wall run. I wrote `elevations.py` to re-project the same spec onto
each wall plane and reuse `draw.draw()`.

**Proposal:** ship that projection helper. ~40 lines, and it makes the skill
usable for the entire built-in category rather than single-box pieces.

### 5. `joint_overrides` has no discovery path

`assembly.py` flags unclassified joints loudly and correctly — that pattern is
good and it forced real decisions. But finding *which* pairs need overriding
meant writing a scratch script to enumerate `derive_connections()` output, then
hand-writing ~50 entries — and re-running it after **every** geometry change,
because each change created new adjacencies (valance↔cleat, upright↔cleat).

**Proposal:** `assembly.py --list-pairs` emitting a paste-ready `joint_overrides`
dict, pre-filled with the style default so only the exceptions need editing.

### 6. Hardware schedule is hand-maintained

`hardware.md` was written and re-synced by hand every revision, while
`assembly.md` generated its own authoritative counts. Two sources of the same
numbers, drifting.

**Proposal:** derive the hardware schedule from the spec's fixtures plus
`assembly.py`'s connector counts.

### 7. No costing

Built `rates.json` (authored prices) + `costing.py` (derived from
`cutlist.json`). For anyone quoting clients this is a first-class deliverable.

**Proposal:** ship both, with the rates file clearly marked as
replace-before-use and labour excluded.

### 8. `package.py`'s step list is closed

Fixed at `cutlist, views, render, assembly, packet`. The three extra emitters
this project needed (elevations, hardware, cost) had to be run separately, so
"one command regenerates everything" stopped being true.

**Proposal:** let the spec module declare extra emitters.

---

## P1 (added) — reading floor plans, colour, and render inspection

### 8b. Cannot open a PDF plan at all — verified missing dependency

The client's architectural plan arrived as a PDF. `Read` failed:

```
pdftoppm is not installed. Install poppler-utils ...
```

Checked the environment: **no PyMuPDF, no pypdfium2, no poppler — only PIL.**
There is no fallback, so the plan could only be read via a 524 × 365 screenshot
the client cropped by hand. At that resolution I misread the "80" as the whole
diagonal length when it was the wall length *before* the door — a mistake that
survived one revision and needed the client to correct it.

**Proposal:**
- Declare a PDF-render dependency (`pypdfium2` — pip wheel, no system install,
  permissive licence) and a `scripts/plan_read.py` that renders pages at a
  chosen DPI and crops/upscales regions. I hand-wrote the crop/upscale helper
  here; it should ship.
- **Doctrine, and this is the important half:** the skill's hard rule 1 says
  never take dimensions from images. A dimensioned architectural plan is the
  legitimate exception — *reading the printed number "165"* is reading data the
  architect authored, which is categorically different from *scaling pixels*.
  The rule should say so explicitly, and impose the discipline that made it work
  here: record the source as `plan`, and **cross-check against a second source**.
  In this project the plan's 165 was independently confirmed by the STL parse,
  and the plan's 128 + 37 = 165 split confirmed the tower position. That
  triangulation is what made plan-reading safe. Where I had only one source (the
  diagonal), I got it wrong.

### 8c. No paint / decor colour catalog

Board and paint colours were invented hex values (`#c6a172` for oak,
`#9caf88` for sage). They look fine and mean nothing — no supplier can match
them.

**Proposal:** an `assets/colors.json` alongside `materials.json` and
`rates.json`, same authored-source discipline:

```json
{"tambour": {"_source": "supplier fan deck, verified <date>",
             "TB-1234": {"name": "...", "hex": "#...", "system": "Tambour"}},
 "ral":     {"RAL 9010": {"hex": "#...", "name": "Pure White"}},
 "decor":   {"H1145": {"name": "...", "hex": "#...", "brand": "Egger"}}}
```

**Do not let the model populate it from memory.** Colour codes are exactly the
class of data hard rule 13 already fences off for drilling coordinates — plausible
recall, unreliable in fact. Populate from a fan deck, a supplier list, or a
verified web source, and stamp each entry with where it came from.

Also worth stating in the skill: **a render is not a colour approval.** Screen
colour is not paint colour. Sign off from a physical sample or drawdown.

### 8d. Render needs group toggles and fixed views (implemented here)

Added: per-group visibility (left tower / right tower / hanging & divider /
decks & uprights, plus room and contents) and five camera presets
(iso / front / left / right / top). Groups derive from the `defn` prefixes the
spec already uses, so new parts are classified with no extra work.

Verified by query: 96 / 96 / 58 / 46 objects per group, towers symmetric, and
each toggle hides exactly its own group.

**Proposal:** fold both into `scripts/render.py`.

---

## P2 — ergonomics

9. **Material colour is not overridable per project.** `melamine` renders white;
   the client's board is oak. Changing it means editing the shared
   `assets/materials.json`. A `materials_local.json` merged over the catalog
   would fix it. (Thickness handling is already good — 10/18/25 mm melamine
   auto-split into separate catalog entries with no work.)

10. **`check_facade_coverage` is noise on open casework.** An open walk-in with
    no doors produced 5 "uncovered hole" warnings on *every* regeneration. Warnings
    that always fire train you to ignore warnings. Skip when no part has
    `kind="door"`, or let the spec declare `open_facade=True`.

11. **Banding tag vocabulary is undiscoverable.** Used `["left","right"]`, got
    "unrecognised banding tags" — with no list of valid ones. Had to grep
    `BANDING_EDGES`. Put the valid set in the message.

12. **`kind="fixture"` conflates two things:** bought hardware that belongs in the
    hardware schedule (wire baskets, brackets, pulls, LED channel) and pure
    presentation props (shoes, garments). I kept props out of the spec entirely,
    which was right, but the skill gives no guidance.

13. **Verify renders by querying the scene, not screenshotting it.** Headless
    WebGL took 2–5 min per frame here, and two background jobs writing the same
    filename silently clobbered each other — a stale frame nearly shipped as
    current. Querying the live page was faster and far stronger evidence:
    bounding boxes, NDC projection to confirm framing, object counts per toggle,
    material state.

    **Strongest evidence for this:** adding the view presets introduced a
    temporal-dead-zone error — `const VIEWS` referenced `AZ0` above its
    declaration, so the script threw at load and the lighting, orbit and render
    loop never ran. A screenshot would have shown a blank or black canvas, which
    on this machine is indistinguishable from "headless WebGL is being slow
    again" — the failure mode I had already seen three times that session. One
    console read named it exactly: `Cannot access 'AZ0' before initialization`.
    Screenshots confirm appearance; queries confirm *state*. For a generated
    page, state is what you actually need.

14. **Decision-log format drifts.** `docs/spec.md` decisions grew to 7a/10a/11a/
    12a/18a–d/19a across revisions. Suggest stable IDs plus an
    active/superseded status.

---

## What worked — keep leaning on it

- **The positioned-part spec as single source of truth.** Seven revisions,
  including a material-thickness change that touched everything, and no
  deliverable ever disagreed with another.
- **`check_overlaps` earned its keep three separate times** — a valance through a
  cleat, an upright through a back cleat, and a 7 mm penetration when the deck
  thickness changed from 18 to 25 and a dependent constant didn't follow. That
  last one is the strongest argument for the whole approach: it was invisible by
  inspection.
- **Hard rule 1 (no dimensions from images)** shaped the entire project
  correctly. It forced the STL route instead of scaling a screenshot, which
  produced exact geometry that the floor plan later confirmed.
- **`assembly.py`'s "REVIEW REQUIRED — assigned by default" flag.** Refusing to
  quietly ship guessed joints is exactly right.
- **Cut-list validation** (sheet-fit, banding totals, material auto-split by
  thickness) never needed a second look.
