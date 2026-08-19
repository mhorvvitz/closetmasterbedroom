#!/usr/bin/env python3
"""render_scene.py — presentation render for the walk-in closet.

Drives off the SAME positioned-part spec as every other deliverable
(closet_spec.py), then adds two toggleable overlay groups that the shared
render.py has no vocabulary for:

  * CONTEXT — the room shell (walls, floor, ceiling) and the bathroom door
  * CONTENTS — laundry basket, shoes, boots, hat boxes, hanging garments

Both are presentation-only. Neither reaches the cut list, the assembly plan or
the elevations: they exist here and nowhere else, so nothing downstream can
mistake a prop for a part.

Output: output/render.html  (three.js r128, manual orbit — r128 has no OrbitControls)
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from closet_spec import (spec, NICHE_W, NICHE_H, NICHE_D, TOWER_D, DIV_X,  # noqa: E402
                         R_X0, T_Z0, T_Z1, HANG_Z0, HANG_Z1, ENTRY_Z,
                         DECK1_Y, DECK2_Y, T, ROD_Y_HIGH, ROD_Y_LOW)

OUT = os.path.join(HERE, "output", "render.html")

# ------------------------------------------------------------------ palette
COLORS = {
    "melamine": "#f2f0ec",        # WHITE board as built — painted on site
    "mdf": "#ece8e1",             # lacquered shaker fronts
    "plywood_birch": "#d9c7a3",
    "hardboard": "#b3a086",
    "steel": "#9aa0a6",
    "brass": "#b8935a",           # drawer pulls — brass / gold
    "fixture": "#4a4a50",
    "wall": "#e9e5dd",
    "floor": "#c3ae95",
    "door": "#f2efe9",
}

ROD_HI = ROD_Y_HIGH + 11          # rod centrelines
ROD_LO = ROD_Y_LOW + 11
DECK2_TOP = DECK2_Y + T
DECK1_TOP = DECK1_Y + T

# ------------------------------------------------------------------ context
WALL_T = 150
Z_FRONT = -1000                   # how far forward of the closet we show the room
DOOR_W, DOOR_H = 750, 2100        # bathroom door opening in the left wall
DOOR_Z0, DOOR_Z1 = -750, 0

HALF = 1.5707963
WALL = COLORS["wall"]
ROOM_L = NICHE_D - Z_FRONT
CX = NICHE_W / 2

# ---- handedness -----------------------------------------------------------
# The spec's Z grows toward the BACK wall. three.js is right-handed with Y up,
# so a camera placed in front and looking along +Z sees the X axis mirrored —
# which put the long (1600) left-hand run on the viewer's RIGHT and disagreed
# with the plan and elevations. Fix at one point: negate Z on the way into the
# scene, so the camera looks along -Z (the standard direction) and +X lands on
# the viewer's right, matching how you actually walk in.
def fz(z, sz):
    """Spec z-range [z, z+sz] -> three.js corner z (size unchanged)."""
    return -(z + sz)

# The shell is built from SINGLE-SIDED planes facing into the room, not solid
# slabs. Seen from outside, each one's back face is culled, so the walls never
# stand between the camera and the closet however far you orbit — a cutaway
# room. Solid boxes made the model unviewable from three-quarters of the orbit.
ROOM_CX, ROOM_CZ = CX, -NICHE_D / 2      # room centre, flipped frame


def seg(x0, z0, x1, z1, y0, y1, c=WALL):
    """A wall segment between two plan points (SPEC coords), as a single-sided
    plane whose normal faces the room."""
    fz0, fz1 = -z0, -z1
    dx, dz = x1 - x0, fz1 - fz0
    L = math.hypot(dx, dz)
    th = math.atan2(-dz, dx)
    cx, cz = (x0 + x1) / 2.0, (fz0 + fz1) / 2.0
    if (ROOM_CX - cx) * math.sin(th) + (ROOM_CZ - cz) * math.cos(th) < 0:
        th += math.pi
    return dict(t="plane", c=c, p=[cx, (y0 + y1) / 2.0, cz],
                w=L, h=y1 - y0, rot=[0, th, 0])


# --- the diagonal bathroom wall (per the floor plan) -----------------------
# The right wall steps 370 inward at Z=400 — the "37" on the plan, and exactly
# the right tower's depth, so the tower's front face lands flush with the step.
# From that step the wall turns 45 deg and runs 800 SOLID ("80" on the plan)
# before the 700-wide x 2100-high bathroom door starts ("70" / "210").
DIAG_WALL, DOOR_LEAF_W = 800.0, 700.0
DIAG_LEN = DIAG_WALL + DOOR_LEAF_W
K = math.sqrt(0.5)
DX0, DZ0 = R_X0, T_Z0                        # 1280, 400 — the step corner


def diag_pt(t):
    return DX0 - t * K, DZ0 - t * K


context = [
    dict(t="plane", c=COLORS["floor"], p=[CX, 0, -(NICHE_D + Z_FRONT) / 2],
         w=NICHE_W + 2 * WALL_T, h=ROOM_L, rot=[-HALF, 0, 0]),
    dict(t="plane", c=WALL, p=[CX, NICHE_H, -(NICHE_D + Z_FRONT) / 2],
         w=NICHE_W + 2 * WALL_T, h=ROOM_L, rot=[HALF, 0, 0]),
    # left wall — the full 1600 closet run, then the entrance opening, then on.
    # The entrance is a CASED OPENING with no door leaf (user).
    seg(0, 0, 0, NICHE_D, 0, NICHE_H),
    seg(0, Z_FRONT, 0, DOOR_Z0, 0, NICHE_H),
    # right wall — only from Z=400 back (the 1200-deep run)
    seg(NICHE_W, T_Z0, NICHE_W, NICHE_D, 0, NICHE_H),
    # the 370 step at Z=400, facing into the closet
    seg(R_X0, T_Z0, NICHE_W, T_Z0, 0, NICHE_H),
    # back wall
    seg(0, NICHE_D, NICHE_W, NICHE_D, 0, NICHE_H),
    # diagonal: 800 of solid wall, then the door opening
    seg(*diag_pt(0), *diag_pt(DIAG_WALL), 0, NICHE_H),
    # head over the bathroom door
    seg(*diag_pt(DIAG_WALL), *diag_pt(DIAG_LEN), DOOR_H, NICHE_H),
    # the bathroom door leaf, hinged at the closet-side jamb, swung part-open
    dict(t="door", c=COLORS["door"],
         hinge=[diag_pt(DIAG_WALL)[0], 0, -diag_pt(DIAG_WALL)[1]],
         s=[DOOR_LEAF_W, DOOR_H, 40], ang=-2.356 + 1.05),
]

# ----------------------------------------------------------------- contents
FABRIC = ["#8a94a6", "#6f7b8c", "#b8b0a2", "#5f6b63", "#a89a8c",
          "#7d8a94", "#9aa6b2", "#6b6560", "#c2b8a8", "#77837a"]
LEATHER = ["#5a4636", "#3d3229", "#6b5442", "#4a3b30"]

contents = []

# 1 — triangular laundry basket, right-angled into the corner formed by the
#     left wall (X=0) and the left tower's front face (Z=400). Shape vertices
#     are given in plan (x, z) SPEC coords; the emitter extrudes them upward.
contents.append(dict(t="tri", c="#b9a074", y=0, h=620,
                     v=[[10, 390], [370, 390], [10, 30]]))

# 2 — shoes on the tower shoe shelves (bays sit on these shelf tops)
for x0, tower in ((60, "L"), (R_X0 + 60, "R")):
    for bay_y, n in ((18, 4), (168, 4), (303, 3)):
        for i in range(n):
            contents.append(dict(t="box", c=LEATHER[i % len(LEATHER)], g=tower,
                                 p=[x0, bay_y, 440 + i * 140], s=[250, 72, 105]))

# 3 — boots on the floor, in front of the long-hang bay's low shelf
for i in range(3):
    contents.append(dict(t="box", c=LEATHER[i % len(LEATHER)],
                         p=[80 + i * 210, 0, 1060], s=[300, 430, 135]))

# 4 — hat boxes on deck 2, plus storage boxes on deck 1
for i, x in enumerate((120, 470, 980, 1360)):
    contents.append(dict(t="cyl", c="#ded5c4" if i % 2 else "#c9bda8", g="deck",
                         p=[x + 150, DECK2_TOP, 1270], r=150, h=175))
for x in (60, 1310):
    contents.append(dict(t="box", c="#cfc4b0", g="deck", p=[x, DECK1_TOP, 1120],
                         s=[300, 250, 340]))

# 5 — hanging garments
def hang(x_start, x_end, rod_y, lengths, depth):
    """Fill a rod run with garments, front face centred on the rod."""
    x, i = x_start, 0
    while x + 58 < x_end:
        ln = lengths[i % len(lengths)]
        contents.append(dict(t="box", c=FABRIC[i % len(FABRIC)], g="hang",
                             p=[x, rod_y - ln, 1300 - depth / 2],
                             s=[54, ln, depth]))
        x += 63
        i += 1

hang(40, DIV_X - 20, ROD_HI, [1330, 1180, 1290, 980, 1240, 1120], 430)   # dresses / coats
hang(DIV_X + 40, NICHE_W - 30, ROD_HI, [770, 800, 740, 810, 760], 400)   # shirts
hang(DIV_X + 40, NICHE_W - 30, ROD_LO, [790, 760, 800, 745], 380)        # pants

# ------------------------------------------------------------------- parts
# flip the props into the scene frame too (boxes by corner, cylinders by centre)
for o in contents:
    if o["t"] == "box":
        o["p"][2] = fz(o["p"][2], o["s"][2])
    elif o["t"] == "cyl":
        o["p"][2] = -o["p"][2]
    # 'tri' carries plan-space vertices; the emitter handles its own mapping

def run_of(defn):
    """Which toggle group a part belongs to. Derived from the defn names the
    spec already uses, so adding a part needs no change here.
    L_Bracket is deck hardware on the left WALL, not part of the left tower."""
    if defn == "L_Bracket" or defn == "LED_Channel":
        return "deck"
    if defn[:2] in ("L_", "R_"):
        return defn[0]
    if defn.startswith(("Deck", "Upright", "Cleat_D")):
        return "deck"
    if defn.startswith(("Rod", "Divider", "ShoeShelf", "ShoeCleat")):
        return "hang"
    return ""


parts = []
for p in spec["parts"]:
    parts.append(dict(x=p["x"], y=p["y"], z=fz(p["z"], p["sz"]),
                      sx=p["sx"], sy=p["sy"], sz=p["sz"],
                      k=p.get("kind", ""), m=p["material"], n=p["defn"],
                      g=run_of(p["defn"])))

DATA = json.dumps(dict(parts=parts, context=context, contents=contents,
                       colors=COLORS, W=NICHE_W, H=NICHE_H, D=NICHE_D))

HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<title>Master Bedroom Walk-In Closet</title>
<style>
 html,body{margin:0;height:100%;background:#efece6;overflow:hidden;
   font:13px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;color:#2b2b2b}
 canvas{display:block}
 #hud{position:fixed;left:16px;top:16px;background:rgba(255,255,255,.9);
   border:1px solid #d8d2c6;border-radius:8px;padding:12px 14px;min-width:190px}
 #hud h1{margin:0 0 2px;font-size:14px}
 #hud .sub{color:#7a7268;font-size:11px;margin-bottom:10px}
 label{display:flex;align-items:center;gap:8px;padding:3px 0;cursor:pointer}
 input{accent-color:#8a6d3b;width:15px;height:15px}
 #fin{margin-top:11px;padding-top:9px;border-top:1px solid #e2ddd2}
 #fin .lbl{font-size:11px;color:#7a7268;margin-bottom:6px}
 #sw{display:flex;gap:6px}
 #sw button{width:28px;height:28px;border-radius:6px;border:2px solid #d8d2c6;
   cursor:pointer;padding:0}
 #sw button.on{border-color:#4a4a50;box-shadow:0 0 0 2px rgba(74,74,80,.18)}
 #vw{display:flex;flex-wrap:wrap;gap:4px}
 #vw button{font:11px inherit;padding:4px 8px;border-radius:5px;
   border:1px solid #d8d2c6;background:#fbfaf7;cursor:pointer}
 #vw button:hover{background:#f0ece3}
 #tip{position:fixed;left:16px;bottom:14px;color:#8a8175;font-size:11px}
</style></head><body>
<div id="hud">
  <h1>Master Bedroom Walk-In Closet</h1>
  <div class="sub">__W__ &times; __H__ &times; __D__ mm</div>
  <label><input type="checkbox" id="ctx" checked> Room &amp; bathroom door</label>
  <label><input type="checkbox" id="cnt" checked> Contents</label>
  <label><input type="checkbox" id="towL" checked> Left tower</label>
  <label><input type="checkbox" id="towR" checked> Right tower</label>
  <label><input type="checkbox" id="hang" checked> Hanging &amp; divider</label>
  <label><input type="checkbox" id="deck" checked> Decks &amp; uprights</label>
  <div id="fin">
    <div class="lbl">View</div>
    <div id="vw">
      <button data-v="iso">Iso</button><button data-v="front">Front</button
      ><button data-v="left">Left</button><button data-v="right">Right</button
      ><button data-v="top">Top</button>
    </div>
  </div>
  <div id="fin">
    <div class="lbl">Board finish</div>
    <div id="sw">
      <button class="on" data-c="#f2f0ec" title="White (as built)"></button>
      <button data-c="#9caf88" title="Sage green"></button>
      <button data-c="#a8c3d4" title="Light blue"></button>
      <button data-c="#9b9b98" title="Grey"></button>
      <button data-c="#3c4a52" title="Charcoal"></button>
    </div>
  </div>
</div>
<div id="tip">drag to orbit &middot; scroll to zoom</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const D=__DATA__, T=THREE;
const scene=new T.Scene(); scene.background=new T.Color(0xefece6);
const renderer=new T.WebGLRenderer({antialias:true});
renderer.shadowMap.enabled=true; renderer.shadowMap.type=T.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);
const camera=new T.PerspectiveCamera(42,1,10,40000);

const cache={};
function mat(key){
  if(!cache[key]){
    const c=new T.Color(D.colors[key]||key);
    cache[key]=(key==='steel'||key==='brass')
      ? new T.MeshStandardMaterial({color:c,roughness:(key==='brass')?.28:.35,metalness:.9})
      : new T.MeshStandardMaterial({color:c,roughness:.8,metalness:0});
  }
  return cache[key];
}
/* objects tagged by group, so any part of the piece can be hidden to see past it */
const GROUPS={L:'towL',R:'towR',deck:'deck',hang:'hang'};
const tagged={}; Object.keys(GROUPS).forEach(g=>tagged[g]=[]);
function reg(o,tag){ if(tag && tagged[tag]) tagged[tag].push(o); }

function box(par,x,y,z,sx,sy,sz,m,edges,tag){
  const g=new T.Mesh(new T.BoxGeometry(sx,sy,sz),m);
  g.position.set(x+sx/2,y+sy/2,z+sz/2);
  g.castShadow=true; g.receiveShadow=true; par.add(g); reg(g,tag);
  if(edges){
    const e=new T.LineSegments(new T.EdgesGeometry(g.geometry),
      new T.LineBasicMaterial({color:0x8d7f6b,transparent:true,opacity:.45}));
    e.position.copy(g.position); par.add(e); reg(e,tag);
  }
  return g;
}

/* ---- the closet itself (from the spec) ---- */
const piece=new T.Group(); scene.add(piece);
D.parts.forEach(p=>{
  if(p.k==='rod'){
    const g=new T.Mesh(new T.CylinderGeometry(p.sy/2,p.sy/2,p.sx,20),mat('steel'));
    g.rotation.z=Math.PI/2;
    g.position.set(p.x+p.sx/2,p.y+p.sy/2,p.z+p.sz/2);
    g.castShadow=true; piece.add(g); reg(g,p.g); return;
  }
  if(p.n==='L_Bracket'){
    /* draw the real L, not its clearance envelope: horizontal arm + wall leg */
    const fm=mat('fixture');
    box(piece,p.x,p.y+p.sy-30,p.z,p.sx,30,p.sz,fm,false,p.g);
    box(piece,p.x,p.y,p.z,30,p.sy,p.sz,fm,false,p.g);
    return;
  }
  const isPull=p.n.endsWith('_Pull');
  const m=isPull?mat('brass'):mat(p.k==='fixture'?'fixture':p.m);
  box(piece,p.x,p.y,p.z,p.sx,p.sy,p.sz,m,!isPull,p.g);
});

/* ---- context: room shell + bathroom door ---- */
const ctx=new T.Group(); scene.add(ctx);
D.context.forEach(o=>{
  if(o.t==='plane'){
    const m=new T.Mesh(new T.PlaneGeometry(o.w,o.h),
      new T.MeshStandardMaterial({color:new T.Color(o.c),roughness:.95,
                                  metalness:0,side:T.FrontSide}));
    m.position.set(o.p[0],o.p[1],o.p[2]);
    m.rotation.set(o.rot[0],o.rot[1],o.rot[2]);
    m.receiveShadow=true; ctx.add(m); return;
  }
  if(o.t==='door'){
    const grp=new T.Group();
    grp.position.set(o.hinge[0],o.hinge[1],o.hinge[2]);
    grp.rotation.y=o.ang;
    const m=new T.Mesh(new T.BoxGeometry(o.s[0],o.s[1],o.s[2]),mat(o.c));
    m.position.set(o.s[0]/2,o.s[1]/2,0); m.castShadow=true; grp.add(m);
    ctx.add(grp); return;
  }
  box(ctx,o.p[0],o.p[1],o.p[2],o.s[0],o.s[1],o.s[2],mat(o.c),false);
});

/* ---- contents: props ---- */
const cnt=new T.Group(); scene.add(cnt);
D.contents.forEach(o=>{
  if(o.t==='box'){ box(cnt,o.p[0],o.p[1],o.p[2],o.s[0],o.s[1],o.s[2],mat(o.c),false,o.g); return; }
  if(o.t==='tri'){
    /* right-angled corner basket: plan polygon extruded upward. Shape (a,b)
       maps to world (a, ., -b) after the -90deg X rotation, and b is the spec
       z, so the polygon lands in the flipped scene frame automatically. */
    const s=new T.Shape();
    s.moveTo(o.v[0][0],o.v[0][1]);
    for(let i=1;i<o.v.length;i++) s.lineTo(o.v[i][0],o.v[i][1]);
    s.closePath();
    const g=new T.Mesh(new T.ExtrudeGeometry(s,{depth:o.h,bevelEnabled:false}),mat(o.c));
    g.rotation.x=-Math.PI/2;
    g.position.set(0,o.y,0);
    g.castShadow=true; g.receiveShadow=true; cnt.add(g); return;
  }
  const g=new T.Mesh(new T.CylinderGeometry(o.r,o.r*.98,o.h,24),mat(o.c));
  g.position.set(o.p[0],o.p[1]+o.h/2,o.p[2]);
  g.castShadow=true; g.receiveShadow=true; cnt.add(g);
});

/* Tower visibility is set per-object; the ctx/cnt groups gate their own
   children, so a tower shoe stays governed by BOTH its tower and Contents. */
function applyVis(){
  ctx.visible=document.getElementById('ctx').checked;
  cnt.visible=document.getElementById('cnt').checked;
  for(const g in GROUPS){
    const on=document.getElementById(GROUPS[g]).checked;
    tagged[g].forEach(o=>o.visible=on);
  }
}
['ctx','cnt',...Object.values(GROUPS)].forEach(id=>
  document.getElementById(id).addEventListener('change',applyVis));
applyVis();

/* Board finish: every melamine part (carcass, shelves, decks, drawer fronts and
   their shaker trim) shares one cached material, so recolouring it re-finishes
   the whole unit at once. Ply/hardboard drawer boxes and the rods are separate
   materials and deliberately do NOT follow. */
const sw=document.getElementById('sw');
const swBtns=[...sw.querySelectorAll('button')];
function pickFinish(btn){
  swBtns.forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  mat('melamine').color.set(btn.dataset.c);
}
swBtns.forEach(btn=>{ btn.style.background=btn.dataset.c;
                      btn.onclick=()=>pickFinish(btn); });
/* ?finish=sage | 1 | light  — so a finish can be linked to or screenshotted */
(()=>{ const q=new URLSearchParams(location.search).get('finish');
  if(!q) return;
  const i=parseInt(q,10);
  const hit=Number.isInteger(i)&&swBtns[i] ? swBtns[i]
    : swBtns.find(b=>b.title.toLowerCase().includes(q.toLowerCase()));
  if(hit) pickFinish(hit);
})();

/* ---- lighting ---- */
scene.add(new T.HemisphereLight(0xffffff,0xb9ad9a,.72));
const key=new T.DirectionalLight(0xfff4e2,.95);
key.position.set(-1800,3600,2600); key.castShadow=true;
key.shadow.mapSize.set(2048,2048);
const s=key.shadow.camera; s.left=-3000; s.right=3000; s.top=3600; s.bottom=-600;
s.near=100; s.far=12000; scene.add(key);
const fill=new T.DirectionalLight(0xdfe8ff,.3); fill.position.set(2600,1800,1800);
scene.add(fill);

/* ---- manual orbit (r128 ships no OrbitControls) ---- */
const tgt=new T.Vector3(D.W/2,D.H*0.45,-D.D*0.5);
const AZ0=1.15;   /* three-quarter view in through the open front */
let az=AZ0, pol=1.22, rad=4700, drag=false, px=0, py=0, idle=true, phase=0;

/* Fixed view presets — declared AFTER az/pol/rad exist. The scene lies along
   -Z with the open front at +Z, so az=PI/2 looks straight in, az=0 faces the
   left wall and az=PI the right. */
const VIEWS={iso:[AZ0,1.22,4700], front:[Math.PI/2,1.50,4300],
             left:[0.02,1.50,4300], right:[Math.PI-0.02,1.50,4300],
             top:[Math.PI/2,0.12,4600]};
document.querySelectorAll('#vw button').forEach(b=>{
  b.onclick=()=>{ const v=VIEWS[b.dataset.v];
    az=v[0]; pol=v[1]; rad=v[2]; idle=false; };
});
const cv=renderer.domElement;
cv.addEventListener('pointerdown',e=>{drag=true;idle=false;px=e.clientX;py=e.clientY;
  cv.setPointerCapture(e.pointerId);});
cv.addEventListener('pointerup',()=>drag=false);
cv.addEventListener('pointermove',e=>{if(!drag)return;
  az-=(e.clientX-px)*0.007;
  pol=Math.max(0.30,Math.min(1.50,pol-(e.clientY-py)*0.005));
  px=e.clientX; py=e.clientY;});
cv.addEventListener('wheel',e=>{rad=Math.max(900,Math.min(9000,rad+e.deltaY*1.7));
  e.preventDefault();},{passive:false});
function resize(){const w=innerWidth,h=innerHeight;
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.setSize(w,h); camera.aspect=w/h; camera.updateProjectionMatrix();}
addEventListener('resize',resize); resize();
(function loop(){
  requestAnimationFrame(loop);
  /* idle: gentle oscillation around the hero angle, not an unbounded spin —
     an unbounded spin drifts the opening view away within seconds */
  if(idle){ phase+=0.0035; az=AZ0+Math.sin(phase)*0.30; }
  camera.position.set(
    tgt.x+rad*Math.sin(pol)*Math.cos(az),
    tgt.y+rad*Math.cos(pol),
    tgt.z+rad*Math.sin(pol)*Math.sin(az));
  camera.lookAt(tgt);
  renderer.render(scene,camera);
})();
</script></body></html>"""

def build(spec=None, outdir=None):
    """Write the presentation render.

    MUST run after package.py's own `render` step — that step writes
    output/render.html from the skill's stock render.py and would otherwise
    clobber this one. Wired into extra_outputs so the ordering is guaranteed
    rather than remembered.
    """
    path = os.path.join(outdir, "render.html") if outdir else OUT
    html = (HTML.replace("__DATA__", DATA)
                .replace("__W__", str(NICHE_W))
                .replace("__H__", str(NICHE_H))
                .replace("__D__", str(NICHE_D)))
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  render.html  ({len(parts)} parts, {len(context)} context, "
          f"{len(contents)} props)")
    return ["render.html (presentation)"]


if __name__ == "__main__":
    build()
