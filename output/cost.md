# Materials cost estimate — Master Bedroom Walk-In Closet

Currency: **ILS**. Derived from `output/cutlist.json` + `rates.json`.

> ⚠️ **Every rate below is an ASSUMED market price unless its row says
> _quoted_.** Replace the assumed numbers in `rates.json` with real supplier
> prices before committing money.
> **Carpenter labour, delivery and installation are NOT included** — on a job
> like this they are usually the larger half of the bill.


## Boards

| Material | Sheets (est.) | ILS low | ILS high | Basis | Price source |
|---|---:|---:|---:|---|---|
| 17mm coloured melamine, 2440x1220 — SUPPLIER QUOTED, incl. cutting | 6 | 1,680 | 1,680 | 72 parts · 12.79 m² | **quoted** |
| 15mm birch plywood (drawer boxes) | 1 | 260 | 380 | 24 parts · 1.79 m² | assumed |
| 6mm birch plywood (grooved drawer bottoms) | 1 | 120 | 200 | 6 parts · 0.95 m² | assumed |
| **Boards subtotal** | | **2,060** | **2,260** | | |

Sheet counts come from the cut list's yield heuristic, **not** an optimised
nesting plan. Run OpenCutList or CutList Optimizer on the real parts for a
firm sheet count — it can move this line by a whole sheet either way.


## Edge banding

| Item | Metres | ILS low | ILS high | Price source |
|---|---:|---:|---:|---|
| ABS edge banding, decor-matched, applied | 55.9 | 447 | 496 | **quoted** |

## Hardware

| Item | Qty | ILS low | ILS high |
|---|---:|---:|---:|
| Confirmat screw 7x50 + cap | 59 | 30 | 59 |
| Wood glue PVA D3, 750ml | 1 | 35 | 60 |
| 23ga pins, 30mm (drawer boxes) | 1 | 15 | 30 |
| Drawer runner pair, 300mm soft-close | 6 | 270 | 570 |
| Bar pull, 160mm centres, BRASS/GOLD finish | 6 | 210 | 660 |
| Hanging rod (807 / 825 / 825) | 3 | 105 | 210 |
| Rod end socket | 6 | 48 | 120 |
| Rod centre support bracket | 3 | 45 | 105 |
| Shelf pin 5mm | 8 | 8 | 16 |
| Heavy-duty shelf L-bracket, 350mm arm | 4 | 140 | 320 |
| Wall fixing (plug + screw) | 45 | 45 | 112 |
| LED aluminium channel + diffuser (per m) | 2.1 | 52 | 105 |
| LED strip, warm white CRI>=90 (per m) | 2.1 | 84 | 189 |
| LED driver 24V | 1 | 90 | 180 |
| PIR / door switch | 1 | 60 | 150 |
| **Hardware subtotal** | | **1,237** | **2,886** |

## Quotes on file

| Supplier | Document | Date | Covers | Record |
|---|---|---|---|---|
| אלפנדרי שיווק לבידים בע"מ / Alfandari | הצעת מחיר No 51/040609 | 2026-08-20 | 12mm French-white melamine, 2440 sheet; applying matched edge banding | `Suppliers/quote-2026-08-20-alfandari.md` |

Quoted rates above trace to these. Read the record files for what each
quote excludes and how long it stays valid.


## Total

| | ILS low | ILS high |
|---|---:|---:|
| Boards | 2,060 | 2,260 |
| Edge banding | 447 | 496 |
| Hardware | 1,237 | 2,886 |
| Subtotal | 3,744 | 5,642 |
| Waste allowance 10% | 374 | 564 |
| **Net** | **4,119** | **6,207** |
| VAT 18% | 741 | 1,117 |
| **TOTAL inc. VAT** | **4,860** | **7,324** |

**Materials and hardware: roughly ILS 4,119–6,207 before VAT, ILS 4,860–7,324 with it.**

Excluded: carpenter labour, CNC/edging shop time, delivery, installation,
electrical work for the LED, and the props (laundry basket, storage boxes).
