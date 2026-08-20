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

Covered: **boards and banding application only.**

Not covered — all still unpriced or on assumed rates:

- the **15 mm birch ply** drawer boxes (24 parts) and the **6 mm ply** drawer
  bottoms (6 parts);
- **all hardware** — runners, pulls, rods, brackets, confirmats, LED;
- **cutting to the cut list.** The ₪280 board price on file was explicitly
  *incl. cutting*; this sheet has no cutting line at all. Ask whether cutting
  is included in the ₪225, or billed per cut.
- delivery, carpenter labour, installation.

## How it compares to what the project assumes

| Item | `rates.json` before | This quote | Effect |
|---|---|---|---|
| Board, per 2440×1220 sheet | ₪280 (17 mm coloured, incl. cutting) | ₪225 (12 mm French white) | **different board — see below** |
| Applied edge banding, per m | ₪4.00–8.00 assumed | ₪8.00 (or ₪8.87/m — see unit note) | now **quoted**, at the top of the assumed range |
| VAT | 18% assumed | 18% | confirmed |

**Unit note on line 2.** The quote says 62 units at ₪8. Two readings fit the
job almost equally well, and the line total is the same either way:

- **per metre** — the cut list needs **55.9 m** of banding; +10% waste = 61.5,
  which rounds to the 62 quoted. Rate ₪8.00/m.
- **per banded part** — the cut list has **60** melamine parts carrying banding.
  Rate would then be ₪496 ÷ 55.9 m = ₪8.87/m equivalent.

`costing.py` prices the bare 55.9 m and adds its own 10% waste allowance, so
the quoted 62 and the estimate's 61.5 land in the same place — the allowance is
not double-counted in any material way.

`rates.json` carries this as a **₪8.00–8.87/m** range so the ambiguity is priced
rather than guessed away. Confirm the unit with the supplier and collapse it.

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

1. Price **17 mm coloured** melamine, same sheet size, and say whether cutting
   to our list is included.
2. Confirm the banding line unit — per metre or per part.
3. Confirm the 62 against our **55.9 m** requirement (`output/cutlist.json`).
4. Confirm the sheet size behind "טפ 244" — the cut list assumes 2440 × 1220.
5. Quote validity: today only. Anything ordered later needs re-quoting.
