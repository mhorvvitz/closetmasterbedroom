"""Decompose the STL into axis-aligned rectangular faces, then pair opposite
faces into panels. Main assembly only (X < 300)."""
import struct, sys, json
from collections import defaultdict

PATH = sys.argv[1]
data = open(PATH, "rb").read()
ntri = struct.unpack("<I", data[80:84])[0]

AX = "XYZ"
plane_tris = defaultdict(list)      # (axis, coord) -> [ (o1,o2) triangle pts ]

for i in range(ntri):
    v = struct.unpack_from("<12f", data, 84 + i * 50)
    p = [v[3:6], v[6:9], v[9:12]]
    if max(q[0] for q in p) > 300:
        continue
    for ax in range(3):
        if abs(p[0][ax] - p[1][ax]) < 1e-4 and abs(p[0][ax] - p[2][ax]) < 1e-4:
            break
    else:
        continue
    o1, o2 = [a for a in range(3) if a != ax]
    ux, uy = p[1][o1] - p[0][o1], p[1][o2] - p[0][o2]
    wx, wy = p[2][o1] - p[0][o1], p[2][o2] - p[0][o2]
    area = abs(ux * wy - uy * wx) / 2.0
    if area < 1.0:
        continue
    plane_tris[(ax, round(p[0][ax], 2))].append(
        (tuple((q[o1], q[o2]) for q in p), area))

rects = []   # (axis, coord, lo1, hi1, lo2, hi2, area)
for (ax, coord), tl in plane_tris.items():
    n = len(tl)
    parent = list(range(n))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra
    v2 = defaultdict(list)
    for ti, (pts, _) in enumerate(tl):
        for q in pts:
            v2[(round(q[0], 2), round(q[1], 2))].append(ti)
    for lst in v2.values():
        for o in lst[1:]: union(lst[0], o)
    grp = defaultdict(list)
    for ti in range(n): grp[find(ti)].append(ti)
    for g in grp.values():
        pts = [q for ti in g for q in tl[ti][0]]
        a = sum(tl[ti][1] for ti in g)
        lo1, hi1 = min(q[0] for q in pts), max(q[0] for q in pts)
        lo2, hi2 = min(q[1] for q in pts), max(q[1] for q in pts)
        bb = (hi1 - lo1) * (hi2 - lo2)
        if bb <= 0: continue
        rects.append({"ax": ax, "c": coord, "lo1": lo1, "hi1": hi1,
                      "lo2": lo2, "hi2": hi2, "area": a, "bb": bb,
                      "rect": abs(bb - a) < max(1.0, 0.02 * bb)})

# ---- pair opposite faces into panels -----------------------------------
byax = defaultdict(list)
for r in rects:
    if r["rect"] and r["bb"] > 80:
        byax[r["ax"]].append(r)

panels = []
used = set()
for ax in range(3):
    rs = sorted(byax[ax], key=lambda r: r["c"])
    for i, a in enumerate(rs):
        if id(a) in used: continue
        for b in rs[i+1:]:
            if id(b) in used: continue
            d = b["c"] - a["c"]
            if d <= 0.05: continue
            if d > 6: break
            if (abs(a["lo1"]-b["lo1"]) < 0.6 and abs(a["hi1"]-b["hi1"]) < 0.6 and
                abs(a["lo2"]-b["lo2"]) < 0.6 and abs(a["hi2"]-b["hi2"]) < 0.6):
                used.add(id(a)); used.add(id(b))
                o1, o2 = [x for x in range(3) if x != ax]
                lo = [0, 0, 0]; hi = [0, 0, 0]
                lo[ax], hi[ax] = a["c"], b["c"]
                lo[o1], hi[o1] = a["lo1"], a["hi1"]
                lo[o2], hi[o2] = a["lo2"], a["hi2"]
                panels.append({"thk_axis": AX[ax], "t": round(d, 2),
                               "x0": round(lo[0],2), "x1": round(hi[0],2),
                               "y0": round(lo[1],2), "y1": round(hi[1],2),
                               "z0": round(lo[2],2), "z1": round(hi[2],2)})
                break

panels.sort(key=lambda p: (p["thk_axis"], p["z0"], p["x0"], p["y0"]))
print(f"{len(panels)} panels found\n")
print(f"{'thk':>4} {'t':>5}  {'X':>15}  {'Y':>15}  {'Z':>15}   {'W':>7} {'D':>7} {'H':>7}")
for p in panels:
    dx, dy, dz = p["x1"]-p["x0"], p["y1"]-p["y0"], p["z1"]-p["z0"]
    print(f"{p['thk_axis']:>4} {p['t']:5.2f}  {p['x0']:7.2f}..{p['x1']:6.2f}  "
          f"{p['y0']:7.2f}..{p['y1']:6.2f}  {p['z0']:7.2f}..{p['z1']:6.2f}   "
          f"{dx:7.2f} {dy:7.2f} {dz:7.2f}")

json.dump(panels, open(sys.argv[2], "w"), indent=1)
