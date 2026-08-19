"""Third pass: extract axis-aligned planar faces from the STL to recover exact
panel positions. Only looks at the main assembly (X < 300)."""
import struct, sys, json
from collections import defaultdict

PATH = sys.argv[1]
XMAX = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0

data = open(PATH, "rb").read()
ntri = struct.unpack("<I", data[80:84])[0]

buckets = defaultdict(lambda: {"area": 0.0, "lo": [1e9, 1e9], "hi": [-1e9, -1e9], "n": 0})
TOL = 1e-3

for i in range(ntri):
    v = struct.unpack_from("<12f", data, 84 + i * 50)
    p = [v[3:6], v[6:9], v[9:12]]
    if max(q[0] for q in p) > XMAX:
        continue
    # which axis is constant?
    for ax in range(3):
        if abs(p[0][ax] - p[1][ax]) < TOL and abs(p[0][ax] - p[2][ax]) < TOL:
            break
    else:
        continue
    o1, o2 = [a for a in range(3) if a != ax]
    # triangle area in the plane
    ux, uy = p[1][o1] - p[0][o1], p[1][o2] - p[0][o2]
    wx, wy = p[2][o1] - p[0][o1], p[2][o2] - p[0][o2]
    area = abs(ux * wy - uy * wx) / 2.0
    if area < 0.05:
        continue
    key = (ax, round(p[0][ax], 2))
    b = buckets[key]
    b["area"] += area
    b["n"] += 1
    for q in p:
        b["lo"][0] = min(b["lo"][0], q[o1]); b["hi"][0] = max(b["hi"][0], q[o1])
        b["lo"][1] = min(b["lo"][1], q[o2]); b["hi"][1] = max(b["hi"][1], q[o2])

AX = "XYZ"
for ax in range(3):
    o1, o2 = [a for a in range(3) if a != ax]
    rows = sorted(((k[1], b) for k, b in buckets.items() if k[0] == ax and b["area"] > 60),
                  key=lambda r: r[0])
    print(f"\n=== planes perpendicular to {AX[ax]}  (area > 60) ===")
    print(f"  {AX[ax]:>9}  {'area':>9}  {'ntri':>5}   "
          f"{AX[o1]}: {'lo':>8} {'hi':>8}    {AX[o2]}: {'lo':>8} {'hi':>8}")
    for coord, b in rows:
        print(f"  {coord:9.2f}  {b['area']:9.1f}  {b['n']:5d}   "
              f"   {b['lo'][0]:8.2f} {b['hi'][0]:8.2f}       "
              f"{b['lo'][1]:8.2f} {b['hi'][1]:8.2f}")
