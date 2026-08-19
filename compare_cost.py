#!/usr/bin/env python3
"""compare_cost.py — HISTORICAL material comparison (melamine+cam / plywood+screws
/ melamine+screws), each derived from its own cut list.

NOT like-for-like: columns 1-2 are the 18mm variants the comparison was made
with, column 3 is the current 17mm build at the quoted 280/sheet. It shows the
shape of the trade-off, not a precise delta. The conclusion it drove is recorded
in docs/spec.md decision 3a. Rates are ASSUMED Israeli market prices; replace before use.
Labour excluded — which matters here, see the note at the bottom of the output.
"""
import json

SHEET = {  # (low, high) per 2440x1220 sheet
    "melamine_18": (190, 280), "melamine_17": (280, 280), "melamine_25": (300, 420), "melamine_10": (120, 180),
    "plywood_birch_18": (380, 650), "plywood_birch_15": (300, 500),
    "plywood_birch_12": (260, 450), "hardboard_4": (35, 60),
        "plywood_birch_6": (120, 200),
}
BAND = (4.0, 8.0)          # per m, applied
WASTE, VAT = 0.10, 0.18

# hardware that is IDENTICAL in both schemes
COMMON = [("Drawer runner pair 300mm soft-close", 6, 45, 95),
          ("Bar pull, brass", 6, 35, 110),
          ("Hanging rod", 3, 35, 70), ("Rod end socket", 6, 8, 20),
          ("Rod centre support", 3, 15, 35), ("Shelf pin", 8, 1.0, 2.0),
          ("L-bracket 350mm arm", 4, 35, 80), ("Wall fixing", 45, 1.0, 2.5),
          ("LED channel (m)", 2.1, 25, 50), ("LED strip (m)", 2.1, 40, 90),
          ("LED driver", 1, 90, 180), ("PIR switch", 1, 60, 150)]

CONNECTORS = {
    "melamine": [("Minifix cam+bolt+cap set", 48, 2.5, 4.5),
                 ("Confirmat + cap", 11, 0.5, 1.0),
                 ("Fluted dowel 8x30", 28, 0.2, 0.4),
                 ("Wood glue 750ml", 1, 35, 60)],
    "ply":      [("Confirmat + cap", 87, 0.5, 1.0),
                 ("Wood glue 750ml", 1, 35, 60)],
    # real count from output_screws/assembly.md
    "screws":   [("Confirmat + cap", 59, 0.5, 1.0),
                 ("Wood glue 750ml", 1, 35, 60),
                 ("23ga pins for drawer boxes", 1, 15, 30)],
}


def price(cutlist_path, scheme):
    cut = json.load(open(cutlist_path, encoding="utf-8"))
    sm = cut["material_summary"]
    b_lo = b_hi = 0.0
    sheets = 0
    for mid, s in sm.items():
        lo, hi = SHEET[mid]
        b_lo += s["sheets_est"] * lo
        b_hi += s["sheets_est"] * hi
        sheets += s["sheets_est"]
    band_m = sum(s.get("band_m", 0.0) for s in sm.values())
    band = (band_m * BAND[0], band_m * BAND[1])
    hw = COMMON + CONNECTORS[scheme]
    h_lo = sum(q * l for _, q, l, _ in hw)
    h_hi = sum(q * h for _, q, _, h in hw)
    sub = (b_lo + band[0] + h_lo, b_hi + band[1] + h_hi)
    net = (sub[0] * (1 + WASTE), sub[1] * (1 + WASTE))
    tot = (net[0] * (1 + VAT), net[1] * (1 + VAT))
    return dict(sheets=sheets, band_m=band_m, boards=(b_lo, b_hi), band=band,
                hw=(h_lo, h_hi), sub=sub, net=net, tot=tot,
                mats=len(sm), conn=len(CONNECTORS[scheme]))


a = price("variants/cam_cutlist.json", "melamine")
b = price("variants/ply_cutlist.json", "ply")
c = price("output/cutlist.json", "screws")   # melamine board, screws

print(f"{'':30} {'MELAMINE + cam':>22} {'PLYWOOD + screws':>22} {'MELAMINE + screws':>22}")
print("-" * 99)
rows = [("distinct board materials", "mats", "{:.0f}"),
        ("sheets (est.)", "sheets", "{:.0f}"),
        ("edge banding (m)", "band_m", "{:.1f}"),
        ("fastener types", "conn", "{:.0f}")]
for label, k, f in rows:
    print(f"{label:30} {f.format(a[k]):>22} {f.format(b[k]):>22} {f.format(c[k]):>22}")
print("-" * 99)
for label, k in [("boards", "boards"), ("banding", "band"), ("hardware", "hw"),
                 ("subtotal", "sub"), ("net (+10% waste)", "net"),
                 ("TOTAL inc 18% VAT", "tot")]:
    av, bv, cv = a[k], b[k], c[k]
    print(f"{label:30} {av[0]:>9,.0f}-{av[1]:<12,.0f} {bv[0]:>9,.0f}-{bv[1]:<12,.0f} {cv[0]:>9,.0f}-{cv[1]:<12,.0f}")
print("-" * 99)
d_lo = b["net"][0] - a["net"][0]
c_lo = c["net"][0] - a["net"][0]
c_hi = c["net"][1] - a["net"][1]
d_hi = b["net"][1] - a["net"][1]
print(f"{'DELTA ply+screws vs base':30} {d_lo:>+9,.0f} to {d_hi:>+,.0f} ILS")
print(f"{'DELTA melamine+screws vs base':30} {c_lo:>+9,.0f} to {c_hi:>+,.0f} ILS")


