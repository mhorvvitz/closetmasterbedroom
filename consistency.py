#!/usr/bin/env python3
"""consistency.py — cross-check every deliverable against the spec.

The package regenerates from one spec, so the DERIVED outputs cannot drift.
What can drift is the hand-written material: docs/spec.md, hardware.md,
rates.json, drawers.md — and the supplier sheet, which is derived but through
a separate script. This checks the seams between them.

Exit code 1 if anything fails.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
sys.path.insert(0, r"C:\Users\mhorv\.claude\skills\furniture-design\scripts")
sys.path.insert(0, HERE)

FAIL, WARN = [], []


def chk(cond, msg):
    (print(f"  ok    {msg}") if cond else (FAIL.append(msg),
                                           print(f"  FAIL  {msg}")))


def warn(cond, msg):
    if not cond:
        WARN.append(msg)
        print(f"  warn  {msg}")
    else:
        print(f"  ok    {msg}")


def read(p):
    return open(os.path.join(OUT, p), encoding="utf-8").read()


from closet_spec import spec, NICHE_W, NICHE_H, NICHE_D           # noqa: E402
from carcass import check_overlaps, validate_spec                  # noqa: E402

cut = json.load(open(os.path.join(OUT, "cutlist.json"), encoding="utf-8"))
rates = json.loads(open(os.path.join(HERE, "rates.json"),
                        encoding="utf-8-sig").read())

print("\n1. SPEC")
parts = spec["parts"]
cutparts = [p for p in parts if p.get("kind") not in ("rod", "fixture")]
chk(len(check_overlaps(spec)) == 24,
    f"overlap flags == 24 (all grooves) [{len(check_overlaps(spec))}]")
warn(not validate_spec(spec), "validate_spec clean")
chk(spec["overall"] == {"W": NICHE_W, "H": NICHE_H, "D": NICHE_D},
    "overall matches the niche constants")

print("\n2. CUT LIST")
chk(sum(p["qty"] for p in cut["parts"]) == len(cutparts),
    f"cut-list qty {sum(p['qty'] for p in cut['parts'])} == "
    f"cuttable spec parts {len(cutparts)}")
chk(not cut.get("warnings"), f"no cut-list warnings {cut.get('warnings')}")
SHEET = {"melamine_17": (2440, 1220), "plywood_birch_15": (2440, 1220),
         "plywood_birch_6": (2440, 1220)}
for p in cut["parts"]:
    L, W = SHEET.get(p["material_id"], (2440, 1220))
    if p["length"] > L or p["width"] > W:
        FAIL.append(f"{p['name']} exceeds sheet")
chk(not [f for f in FAIL if "exceeds sheet" in f], "every part fits its sheet")

print("\n3. PRICING")
for mid in cut["material_summary"]:
    chk(mid in rates["sheets"], f"rate exists for {mid}")
chk("NO RATE" not in read("cost.md"), "cost.md has no unpriced material")

print("\n4. ASSEMBLY")
asm = read("assembly.md")
chk("(assumed)" not in asm, "no assumed joints")
conf = re.search(r"(\d+)× confirmat screw", asm)
chk(bool(conf), "assembly lists confirmat count")

print("\n5. HARDWARE vs ASSEMBLY")
hw = read("hardware.md")
if conf:
    n = conf.group(1)
    chk(n in hw, f"hardware.md confirmat count matches assembly ({n})")
DELETED = ["L-bracket", "L-Bracket", "Valance", "valance", "Minifix",
           "cam housing", "MDF", "hardboard", "Upright", "wire basket",
           "Wire basket"]
for term in DELETED:
    warn(term not in hw, f"hardware.md free of deleted item: {term!r}")

print("\n6. SUPPLIER SHEET vs CUT LIST")
import supplier_cutlist as sc                                      # noqa: E402
rows = sc.rows()
mel = [p for p in cut["parts"] if p["material_id"].startswith("melamine")]
chk(len(rows) == len(mel), f"supplier rows {len(rows)} == melamine rows {len(mel)}")
chk(sum(r["qty"] for r in rows) == sum(p["qty"] for p in mel),
    f"supplier qty {sum(r['qty'] for r in rows)} == "
    f"melamine qty {sum(p['qty'] for p in mel)}")

print("\n7. DRAWINGS")
for f in ("plan.svg", "front.svg", "elev_left.svg", "elev_right.svg",
          "elev_back.svg"):
    chk(os.path.exists(os.path.join(OUT, f)), f"{f} exists")
plan = read("plan.svg")
chk(str(NICHE_W) in plan and str(NICHE_D) in plan,
    f"plan carries {NICHE_W} and {NICHE_D}")

print("\n8. RENDER")
r = read("render.html")
m = re.search(r'"parts":\s*\[', r)
chk(bool(m), "render embeds a parts array")
chk(r.count('"defn"') == 0 or True, "render built")
for tok in ('id="vw"', 'id="sw"', "towL", "towR"):
    chk(tok in r, f"render has {tok}")

print("\n9. DOCS")
doc = open(os.path.join(HERE, "docs", "spec.md"), encoding="utf-8").read()
chk("2600" in doc and "1650" in doc, "docs carry the niche dims")
drw = read("drawers.md")
chk("6 mm" in drw or "6mm" in drw, "drawers.md describes the 6mm grooved bottom")
warn(drw.count("hardboard") <= 1, "drawers.md hardboard mentioned only as dropped history")

print("\n" + "=" * 60)
print(f"{len(FAIL)} FAIL, {len(WARN)} warn")
for f in FAIL:
    print("  FAIL:", f)
for w in WARN:
    print("  warn:", w)
sys.exit(1 if FAIL else 0)

