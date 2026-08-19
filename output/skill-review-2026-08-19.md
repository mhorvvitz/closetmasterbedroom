# Skill review #2 — furniture-design

**Project shape:** built-in U-shaped walk-in closet, reverse-engineered from an
existing 3D model, then carried through ~15 revisions to a supplier-ready
package including a shop's own cutting-list template.
**Since review #1:** material change, thickness change (18→17), topology change
(continuous panels), joinery change (cam+dowel → screws), and a public repo.
**Date:** 2026-08-19

---

## P0 — two structural bugs in the emit pipeline

### 1. `package.py`'s `render` step silently clobbers a project's own render

`extra_outputs` runs last, but there is no way to *replace* an earlier step's
output — only to re-write the same filename afterwards. This project needed a
richer render (room shell, props, group toggles, view presets, finish swatches),
so `render_scene.py` wrote `output/render.html`… and every `package.py` run
overwrote it with the stock version.

**It survived ten revisions undetected**, because the workaround — re-running
`render_scene.py` by hand afterwards — looked like a normal step. It was only
caught when a consistency checker asserted the file still contained `id="sw"`.

**Fix:** either `--skip <step>`, or let a spec module declare
`replaces = {"render": callable}`. Silent clobbering of a declared output is the
worst failure mode: the file exists, it looks right, and it is wrong.

### 2. The packet cannot include anything a project generates

`package.py:169` builds the packet from a hardcoded `[cl_md, asm_md]`, **before**
`extra_outputs` runs. So a project-generated sheet can never reach `packet.pdf`
— which is the thing the carpenter actually holds. The packet also omits wall
elevations even when `elevation_walls` produced them.

This project ended up rebuilding the packet inside an `extra_output` to get the
drawer sheet, hardware schedule and cost into it.

**Fix:** build the packet from whatever exists in the output directory (or let
the spec declare `packet_docs` / `packet_views`), and run it after
`extra_outputs`.

---

## P1 — derived-vs-authored, and the drift it causes

### 3. The hardware schedule is not derived, and rots

Hand-maintained across nine revisions, it ended up listing **52 Minifix cams and
4 L-brackets that had been deleted from the design**, and **13 confirmats where
the model said 59**. Every one of those would have been ordered.

Connector counts already exist in `assembly.md`; fixture counts already exist in
the spec. **Fix:** derive it. Leave authored only what a model cannot know —
runner series, rod profile, LED electrical spec.

### 4. There is no cross-check between deliverables

The derived outputs cannot drift from each other, but the *seams* can: hardware
vs assembly, supplier export vs cut list, docs vs deleted parts, materials vs
priced rates. Nothing checks them.

A ~130-line checker written for this project found bugs #1 and #3 within a minute
of first running. **Fix:** ship `scripts/consistency.py`, exiting non-zero, with
checks for: cut-list qty vs spec parts; every part within its sheet; every
material priced; zero assumed joints; hardware counts matching assembly; exports
matching the cut list; drawings present; docs free of deleted part names.

### 5. `notes={}` is free text and is never validated

Stale part notes reached the carpenter for three revisions: drawer fronts
described as *"18 mm MDF, CNC-routed, lacquered"* when they were 17 mm melamine
with applied trim, and a deck panel noted *"valance rail stiffens the front
edge"* when the valance had been deleted.

**Fix:** at minimum warn when a `notes`/`banding` key matches no `defn` in the
spec. That alone would have caught both.

### 6. Part thickness is not validated against the material

`materials.json` lists each material's available thicknesses. MDF is
`[3, 5.5, 7.5, 10, 12, 16, 19, 22, 28, 30]`. A variant specifying **18 mm and
25 mm MDF** passed the cut list without complaint — neither thickness exists.

**Fix:** check `thickness in materials[mat]["thick"]` and warn.

### 7. Banding tags need per-part reasoning that is easy to get wrong

`"front"` bands a **length** edge. For a part that is 370 deep × 325 tall the
visible vertical edge is the 325 — a **width** edge — so `"front"` bands the
wrong one. Got this wrong on the uprights, and separately shipped four parts
(including the single most visible edge in the room) with **no banding at all**
after an edit deleted the line they were declared on.

**Fix:** a helper taking a face — `banding_for(part, faces=["front","end"])` —
that resolves to the right tag from the part's own proportions.

### 8. `validate_spec` false-positives on side-facing fronts

Added since review #1 and useful, but it assumes `kind="door"` parts face +Z. In
any U-shaped built-in the fronts face **along X** into the walkway, so it fires
on every one. A persistent false positive trains people to ignore the check.

**Fix:** infer the facing axis per part (the axis its thinnest dimension lies on,
relative to the nearest carcass), or let the spec declare `front_axis`.

### 9. No supplier-export path

Shops here send their own cutting-list template and want it filled — not a
generic cut list. This project wrote a mapper: cut list → the shop's Hebrew
`.xls`, with banding translated to their vocabulary (`1 ארוך`, `4 צדדים`) and a
per-row rotation flag.

**Fix:** ship a template-mapping exporter. Worth carrying the domain insight too:
**a plain colour has no grain, so every part may be rotated** — which materially
improves the shop's yield, and is a real argument for a solid colour over a
woodgrain decor.

---

## P2

10. **`expected_overlaps` is a single integer.** It worked well, but after
    changing the groove I had to re-verify all 24 flags by hand to be sure the
    count still meant what I thought. A per-pair allowlist —
    `{("BoxBottom","BoxSide"): 24}` — would fail loudly if the *composition*
    changed while the total held.

11. **No overview/handoff artefact.** A one-page project index (render, plan,
    elevations, key dims, cost, document links) turned out to be the natural
    handoff to a client and the natural portfolio piece. Cheap to generate from
    what already exists.

12. **Windows note worth documenting:** PowerShell's `Set-Content -Encoding utf8`
    writes a BOM, which `json.load` rejects outright — it silently broke a data
    file mid-project. Windows is a primary target for this skill.

---

## What worked — and is worth protecting

- **`assembly.py`'s assumed-joint flag is the best thing in the toolchain.**
  Every topology change surfaced its new adjacencies — around ten across the
  project — and refused to ship a guess. It converted "did I forget anything?"
  into a list.
- **`check_overlaps` caught a class of bug nothing else would**: changing
  `T_DECK` 18→25 left a dependent constant behind and the uprights penetrated
  the decks by 7 mm. Invisible by inspection, obvious to the checker.
- **The positioned-part spec held through everything** — material, thickness,
  joinery method and topology all changed, and no two deliverables ever
  disagreed. The one-way derivation chain is the right architecture.
- **The `docs/spec.md` decision log earned its keep**, specifically the
  convention of marking decisions *superseded* rather than editing them away.
  When a change was made on a misread and reverted, the record still reads
  honestly — which matters when the carpenter asks why something is the way it is.
