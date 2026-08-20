# Supplier quote — אלפנדרי שיווק לבידים בע"מ

**Document:** הצעת מחיר (price quote) **No 51/040609**, copy 1
**Date:** 20/08/2026, 08:59 · **Payment (פרעון):** 20/08/2026
**To:** מיכאל הורוביץ (printed "מיאל הורוביץ") · tel 0587896774
**Customer ref (מספרכם):** 0000299999 · agent 00 · credit 0000

**Supplier:** אלפנדרי שיווק לבידים בע"מ ("אלפנדרי", est. 1965)
שידלובסקי 2, מתחם ארגמן, יבנה · ת.ד 512 נס ציונה · מיקוד 7410401
ח.פ. 511069148 · tel 03-9660150 · fax 03-9671560 · mobile 050-4610417
haimalf07@gmail.com · www.alfandari.biz

Source document: the supplier's own PDF (`NextERPNo510406094CF1…`), held by the
client. Not committed here — this file is the transcription of record.

---

## Lines, as quoted

| # | תאור (as printed) | Reading | Qty | Unit ₪ | Line ₪ |
|---:|---|---|---:|---:|---:|
| 1 | מלמין 12 צרפתי לבן טפ 244 | 12 mm melamine-faced board, **French white**, 2440 sheet | 5.00 | 225.00 | 1,125.00 |
| 2 | הדבקת קנט תואם(א) | **Applying** matched edge banding | 62.00 | 8.00 | 496.00 |

| | ₪ |
|---|---:|
| סה"כ לפני הנחה — before discount | 1,621.00 |
| הנחה −0.01% — discount | −0.19 |
| סה"כ אחרי הנחה — after discount | 1,621.19 |
| מע"מ 18% — VAT | 291.81 |
| **סה"כ לתשלום — TOTAL** | **1,913.00** |

VAT is charged at **18%**, which confirms the rate `rates.json` assumed.

**Arithmetic note:** the two lines sum to 1,621.00; a −0.19 discount should give
1,620.81, but the sheet prints **1,621.19** and computes VAT and the total from
that figure. It is a ₪0.38 artefact of the supplier's rounding — immaterial, but
worth one sentence when the order is placed.

## Terms printed on the quote

- **הצעת מחיר זו תקפה ל-היום בלבד** — *this quote is valid for today only.*
- **פטור מלא מניכוי מס במקור** — full exemption from tax withholding at source.
- Title retention: the goods remain the supplier's property until payment is
  final and absolute (i.e. until cheques clear).
- The buyer confirms that the company's manager/directors and/or shareholders
  are **personally liable** for payment of the goods.
- Issued by "שיווק 2". ט.ל.ח (errors and omissions excepted).

---

## What this quote does and does not cover

Covered: **boards, cutting, and banding application.** Cutting to the cut list
is included in the board price — confirmed by the client, 2026-08-20. The sheet
carries no separate cutting line because there is nothing separate to bill.

Not covered — all still unpriced or on assumed rates:

- the **15 mm birch ply** drawer boxes (24 parts) and the **6 mm ply** drawer
  bottoms (6 parts);
- **all hardware** — runners, pulls, rods, brackets, confirmats, LED;
- delivery, carpenter labour, installation.

## How it compares to what the project assumes

| Item | `rates.json` before | This quote | Effect |
|---|---|---|---|
| Board, per 2440×1220 sheet | ₪280 (17 mm coloured, incl. cutting) | ₪225 (12 mm French white, incl. cutting) | **different board — see below** |
| Applied edge banding, per m | ₪4.00–8.00 assumed | ₪8.00/m | now **quoted**, at the top of the assumed range |
| VAT | 18% assumed | 18% | confirmed |

**Unit note on line 2.** The 62 is **metres**, not a count of parts. The cut
list needs **55.9 m** of banding; the 10% waste allowance puts it at 61.5, which
is the 62 quoted. No part count in the job lands anywhere near it:

| Count | Value |
|---|---:|
| Melamine parts | 72 |
| Parts carrying a banding instruction | 60 |
| …excluding the 24 shaker trim pieces | 36 |
| Banded edges (each part's edges, counted separately) | 116 |
| **Metres of banding** | **55.9** (61.5 with waste) |

`costing.py` prices the bare 55.9 m and adds its own 10% waste allowance, so it
and the quote arrive at the same quantity by the same route.

`rates.json` therefore carries applied banding at a flat **₪8.00/m**, quoted.

## ⚠️ The board line is not the board this design is built from

The design is **17 mm coloured melamine** throughout (decision 10b — the colour
is only made in 17 mm). This quote is for **12 mm white**. That is not a price
comparison, it is a different material:

- **Thickness.** Every internal dimension in `closet_spec.py` is derived from
  17 mm: tower clear 566, drawer box 540, deck 1 top 1917. At 12 mm they all
  re-derive, and the cut list, drawings, drilling coordinates and supplier sheet
  all change with them.
- **Stiffness.** Deck deflection goes as t³. 12 mm is (17/12)³ ≈ **2.8× less
  stiff** than 17 mm — on top of the 3.2× already given up going 25 → 17 mm.
  The ~15 kg deck load limit accepted at decision 10c would fall to roughly
  **5 kg per back panel**. That is not a storage deck any more.
- **Joinery.** A 7 mm confirmat body into a 12 mm panel edge is not viable;
  decision 5f already ruled it out for 17 mm blocks.
- **Colour.** "צרפתי לבן" is white. The chosen decor is a colour, and the render
  swatches and drawer-front trim all assume it.
- **Quantity.** 5 sheets, against the **6** melamine sheets the cut list's yield
  heuristic estimates. 5 may well be right after real nesting, but it has not
  been checked against an optimised layout.

So the board price here is **not** adopted into `rates.json`. `melamine_17`
stays at the quoted ₪280 incl. cutting. Use this line as evidence of what a
thinner white board costs, not as a price for this job.

## To put back to the supplier

1. Price **17 mm coloured** melamine, same sheet size, cutting included on the
   same basis as this quote.
2. Confirm the 62 m against our **55.9 m** requirement (`output/cutlist.json`) —
   the difference is the waste allowance, so an order should not need more.
3. Confirm the sheet size behind "טפ 244" — the cut list assumes 2440 × 1220.
4. Quote validity: today only. Anything ordered later needs re-quoting.
