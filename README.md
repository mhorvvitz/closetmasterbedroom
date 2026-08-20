# Master Bedroom Walk-In Closet

A built-in U-shaped walk-in closet for a 1650 × 1600 mm recess, taken from an
existing SketchUp model all the way to a carpenter-ready package.

**[→ Project overview (index.html)](index.html)** — render, plan, elevations, cost.

Built with the [furniture-design skill](https://github.com/mhorvvitz/furniture-design-skill).

## What's here

| | |
|---|---|
| `closet_spec.py` | **the single source of geometry** — every deliverable derives from it |
| `docs/spec.md` | project record: measurements with their sources, every decision with its rationale |
| `output/` | cut list, shop drawings, assembly plan, hardware schedule, cost, 3D render |
| `output/רשימת-חיתוך-מלא.xls` | the supplier's own cutting-list template, filled |
| `Suppliers/quote-*.md` | supplier quotes as received, transcribed — the evidence behind `rates.json` |
| `prototypes/` | the STL parsers used to reverse-engineer the original model |
| `variants/` | cut lists for the material options that were priced and rejected |

## Regenerate everything

```bash
python <skill>/scripts/package.py closet_spec.py --out output/   # the whole package
python supplier_cutlist.py && python make_index.py               # supplier sheet + site
python consistency.py                                            # cross-check
```

`closet_spec.py` declares three hooks the skill honours: `extra_outputs` for the
hardware, cost and drawer sheets; `replaces` so the project's own renderer runs
instead of the stock one; and `packet_docs` so all five documents land in the PDF.

`consistency.py` validates the cut list against the spec, the supplier sheet
against the cut list, the hardware schedule against the assembly plan, and every
material against a priced rate. It exits non-zero on any mismatch.

## Headline numbers

- **102 cut parts**, 8 sheets, 0 assumed joints
- 17 mm coloured melamine at ₪280/sheet incl. cutting (**quoted**)
- Applied edge banding at ₪8.00/m (**quoted**, 2026-08-20)
- Materials + hardware **₪4,119–6,153 net** — labour excluded
- Board and banding prices are real; hardware and plywood rates are still assumed

## Not published here

`reference/` is excluded from this public repo: the architect's construction
drawing, the original SketchUp model (`.skp`) and its STL export, and the model
screenshots. Everything derived from them — shell dimensions, the parsed part
geometry, the decision trail — is recorded in `docs/spec.md` and `closet_spec.py`.

`prototypes/` holds the parsers that read the STL, so the reverse-engineering
method is reproducible even though the source model is not published.
