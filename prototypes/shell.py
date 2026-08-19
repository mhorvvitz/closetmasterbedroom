"""Isolate the room/niche shell component and print its faces as rectangles."""
import struct, sys
from collections import defaultdict

PATH = sys.argv[1]
data = open(PATH, "rb").read()
ntri = struct.unpack("<I", data[80:84])[0]

tris = []
for i in range(ntri):
    v = struct.unpack_from("<12f", data, 84 + i * 50)
    tris.append((v[3:6], v[6:9], v[9:12]))

Q = 1000.0
key = lambda p: (round(p[0]*Q), round(p[1]*Q), round(p[2]*Q))
parent = list(range(len(tris)))
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]; a = parent[a]
    return a
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[rb] = ra

v2t = defaultdict(list)
for ti, t in enumerate(tris):
    for p in t: v2t[key(p)].append(ti)
for tl in v2t.values():
    for o in tl[1:]: union(tl[0], o)

groups = defaultdict(list)
for ti in range(len(tris)): groups[find(ti)].append(ti)

# pick components by target bbox given on cmd line, else the shell
targets = sys.argv[2:] or ["shell"]

def bbox(tl):
    xs=[p[0] for ti in tl for p in tris[ti]]
    ys=[p[1] for ti in tl for p in tris[ti]]
    zs=[p[2] for ti in tl for p in tris[ti]]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))

cands = []
for gid, tl in groups.items():
    b = bbox(tl)
    cands.append((( b[1]-b[0])*(b[3]-b[2])*(b[5]-b[4]), gid, tl, b))
cands.sort(reverse=True, key=lambda c: c[0])

AX="XYZ"
for vol, gid, tl, b in cands[:4]:
    print(f"\n########## component vol={vol:.0f}  tris={len(tl)}  "
          f"bbox X {b[0]:.2f}..{b[1]:.2f}  Y {b[2]:.2f}..{b[3]:.2f}  Z {b[4]:.2f}..{b[5]:.2f}")
    planes = defaultdict(lambda: {"area":0.0,"lo":[1e9,1e9],"hi":[-1e9,-1e9]})
    for ti in tl:
        p = tris[ti]
        for ax in range(3):
            if abs(p[0][ax]-p[1][ax])<1e-3 and abs(p[0][ax]-p[2][ax])<1e-3: break
        else: continue
        o1,o2=[a for a in range(3) if a!=ax]
        ux,uy=p[1][o1]-p[0][o1],p[1][o2]-p[0][o2]
        wx,wy=p[2][o1]-p[0][o1],p[2][o2]-p[0][o2]
        a=abs(ux*wy-uy*wx)/2
        if a<0.01: continue
        d=planes[(ax,round(p[0][ax],2))]
        d["area"]+=a
        for q in p:
            d["lo"][0]=min(d["lo"][0],q[o1]); d["hi"][0]=max(d["hi"][0],q[o1])
            d["lo"][1]=min(d["lo"][1],q[o2]); d["hi"][1]=max(d["hi"][1],q[o2])
    for (ax,c),d in sorted(planes.items()):
        o1,o2=[a for a in range(3) if a!=ax]
        w=d["hi"][0]-d["lo"][0]; h=d["hi"][1]-d["lo"][1]
        print(f"   {AX[ax]}={c:8.2f}  area={d['area']:9.1f}  bboxarea={w*h:9.1f}  "
              f"{'FULL' if abs(w*h-d['area'])<1 else 'HOLE'}  "
              f"{AX[o1]} {d['lo'][0]:7.2f}..{d['hi'][0]:7.2f} ({w:7.2f})   "
              f"{AX[o2]} {d['lo'][1]:7.2f}..{d['hi'][1]:7.2f} ({h:7.2f})")
