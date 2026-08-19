"""Second pass: spatially cluster the STL components into assemblies and
summarise repeated part signatures."""
import json, sys
from collections import defaultdict

comps = json.load(open(sys.argv[1]))
print(f"{len(comps)} components\n")

# ---- 1. spatial clustering along X (the model is spread over X 0..1058) ----
xs = sorted(c["x0"] for c in comps)
gaps = []
for a, b in zip(xs, xs[1:]):
    if b - a > 40:
        gaps.append((a, b, b - a))
print("large X gaps between component origins (>40 units):")
for a, b, g in gaps:
    print(f"   {a:9.2f} -> {b:9.2f}   gap {g:8.2f}")

# cluster by X with 40-unit gap threshold
bounds = [0.0] + [(a + b) / 2 for a, b, _ in gaps] + [1e9]
clusters = defaultdict(list)
for c in comps:
    for i in range(len(bounds) - 1):
        if bounds[i] <= c["x0"] < bounds[i + 1]:
            clusters[i].append(c)
            break

print("\n=== spatial clusters ===")
for i in sorted(clusters):
    cl = clusters[i]
    print(f"\ncluster {i}: {len(cl)} components   "
          f"X {min(c['x0'] for c in cl):.1f}..{max(c['x1'] for c in cl):.1f}   "
          f"Y {min(c['y0'] for c in cl):.1f}..{max(c['y1'] for c in cl):.1f}   "
          f"Z {min(c['z0'] for c in cl):.1f}..{max(c['z1'] for c in cl):.1f}")
    # top 6 by volume
    for c in sorted(cl, key=lambda c: -c["vol"])[:6]:
        print(f"      {c['dx']:8.2f} x {c['dy']:8.2f} x {c['dz']:8.2f}  "
              f"@ ({c['x0']:8.2f},{c['y0']:8.2f},{c['z0']:8.2f})  tri={c['ntri']}")

# ---- 2. repeated size signatures (panels / shelves / rods) ----
print("\n=== repeated size signatures (rounded to 0.1) ===")
sig = defaultdict(list)
for c in comps:
    key = tuple(round(v, 1) for v in sorted((c["dx"], c["dy"], c["dz"])))
    sig[key].append(c)
for key, cl in sorted(sig.items(), key=lambda kv: -len(kv[1]))[:25]:
    print(f"  x{len(cl):<3}  {key[0]:8.2f} x {key[1]:8.2f} x {key[2]:8.2f}"
          f"   (Xrange {min(c['x0'] for c in cl):.0f}..{max(c['x0'] for c in cl):.0f})")

# ---- 3. panel-like parts (one dim between 1.5 and 2.2 = 15-22 mm) ----
print("\n=== panel-like parts (thin dim 1.5..2.2) sorted by area ===")
pans = []
for c in comps:
    d = sorted((c["dx"], c["dy"], c["dz"]))
    if 1.5 <= d[0] <= 2.2 and d[1] > 15:
        pans.append((d[2] * d[1], c, d))
pans.sort(key=lambda t: -t[0])
print(f"  {len(pans)} panel-like parts")
for area, c, d in pans[:60]:
    axis = "thk-" + ("X" if abs(c["dx"] - d[0]) < 1e-6 else "Y" if abs(c["dy"] - d[0]) < 1e-6 else "Z")
    print(f"   {d[2]:8.2f} x {d[1]:8.2f} x {d[0]:5.2f}  {axis}  "
          f"@ ({c['x0']:8.2f},{c['y0']:8.2f},{c['z0']:8.2f})")

# ---- 4. rod-like parts (two similar small dims, one long) ----
print("\n=== rod-like parts (2 small similar dims < 6, one long > 20) ===")
for c in comps:
    d = sorted((c["dx"], c["dy"], c["dz"]))
    if d[1] < 6 and abs(d[0] - d[1]) < 0.6 and d[2] > 20:
        axis = "len-" + ("X" if abs(c["dx"] - d[2]) < 1e-6 else "Y" if abs(c["dy"] - d[2]) < 1e-6 else "Z")
        print(f"   dia~{d[0]:.2f}/{d[1]:.2f}  len {d[2]:8.2f}  {axis}  "
              f"@ ({c['x0']:8.2f},{c['y0']:8.2f},{c['z0']:8.2f})  tri={c['ntri']}")
