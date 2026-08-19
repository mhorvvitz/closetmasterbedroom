"""Parse a binary STL, cluster triangles into connected solids, report bounding boxes.

Reverse-engineering aid: every axis-aligned box part in the model shows up as one
connected component whose bbox IS its cut size. Nothing here is read off an image.
"""
import struct, sys, json
from collections import defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else r"C:\projects\MasterBedRoomClosetDesign\Master Closet Sketchup Export 14.8.2026.stl"

with open(PATH, "rb") as f:
    data = f.read()

ntri = struct.unpack("<I", data[80:84])[0]
print(f"triangles: {ntri}   filesize: {len(data)}  expected: {84 + ntri*50}")

# --- read all triangles -------------------------------------------------
tris = []          # list of (v0,v1,v2) with quantised int coords
QUANT = 1000.0     # quantise to 1/1000 of a unit for vertex welding
off = 84
raw = memoryview(data)
for i in range(ntri):
    base = off + i * 50
    vals = struct.unpack_from("<12f", raw, base)
    vs = []
    for k in range(1, 4):
        x, y, z = vals[k*3:k*3+3]
        vs.append((round(x*QUANT), round(y*QUANT), round(z*QUANT)))
    tris.append(tuple(vs))

# --- overall extents ----------------------------------------------------
xs = [v[0] for t in tris for v in t]
ys = [v[1] for t in tris for v in t]
zs = [v[2] for t in tris for v in t]
print("model extents (raw units):")
print(f"  X {min(xs)/QUANT:12.3f} .. {max(xs)/QUANT:12.3f}   span {(max(xs)-min(xs))/QUANT:.3f}")
print(f"  Y {min(ys)/QUANT:12.3f} .. {max(ys)/QUANT:12.3f}   span {(max(ys)-min(ys))/QUANT:.3f}")
print(f"  Z {min(zs)/QUANT:12.3f} .. {max(zs)/QUANT:12.3f}   span {(max(zs)-min(zs))/QUANT:.3f}")

# --- union-find over shared vertices ------------------------------------
parent = list(range(len(tris)))
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

vert_to_tris = defaultdict(list)
for ti, t in enumerate(tris):
    for v in t:
        vert_to_tris[v].append(ti)
for v, tl in vert_to_tris.items():
    first = tl[0]
    for other in tl[1:]:
        union(first, other)

groups = defaultdict(list)
for ti in range(len(tris)):
    groups[find(ti)].append(ti)

print(f"\nconnected components: {len(groups)}")

# --- per-component bbox -------------------------------------------------
comps = []
for gid, tl in groups.items():
    gx = [v[0] for ti in tl for v in tris[ti]]
    gy = [v[1] for ti in tl for v in tris[ti]]
    gz = [v[2] for ti in tl for v in tris[ti]]
    comp = {
        "ntri": len(tl),
        "x0": min(gx)/QUANT, "x1": max(gx)/QUANT,
        "y0": min(gy)/QUANT, "y1": max(gy)/QUANT,
        "z0": min(gz)/QUANT, "z1": max(gz)/QUANT,
    }
    comp["dx"] = comp["x1"] - comp["x0"]
    comp["dy"] = comp["y1"] - comp["y0"]
    comp["dz"] = comp["z1"] - comp["z0"]
    comp["vol"] = comp["dx"] * comp["dy"] * comp["dz"]
    # is it a plain axis-aligned box? 12 triangles and 8 distinct corners
    verts = {v for ti in tl for v in tris[ti]}
    comp["nvert"] = len(verts)
    comp["box"] = (len(tl) == 12 and len(verts) == 8)
    comps.append(comp)

comps.sort(key=lambda c: -c["vol"])
with open(sys.argv[2] if len(sys.argv) > 2 else "comps.json", "w") as f:
    json.dump(comps, f, indent=1)

print(f"\n{'#':>4} {'tri':>7} {'vert':>6} {'box':>4}  {'dx':>9} {'dy':>9} {'dz':>9}   "
      f"{'x0':>9} {'y0':>9} {'z0':>9}")
for i, c in enumerate(comps[:80]):
    print(f"{i:>4} {c['ntri']:>7} {c['nvert']:>6} {'Y' if c['box'] else '.':>4}  "
          f"{c['dx']:>9.2f} {c['dy']:>9.2f} {c['dz']:>9.2f}   "
          f"{c['x0']:>9.2f} {c['y0']:>9.2f} {c['z0']:>9.2f}")
if len(comps) > 80:
    print(f"... {len(comps)-80} more (see json)")
