import sys
sys.path.insert(0, r"C:\Users\mhorv\.claude\skills\furniture-design\scripts")
sys.path.insert(0, r"C:\projects\MasterBedRoomClosetDesign")
import assembly
from closet_spec import spec

cons = assembly.derive_connections(spec, "frameless_kd")
seen = {}
for c in cons:
    a = c["part_a"].rsplit("_", 1)[0]
    b = c["part_b"].rsplit("_", 1)[0]
    k = tuple(sorted((a, b)))
    seen[k] = seen.get(k, 0) + 1
for k, v in sorted(seen.items()):
    print(f'{v:>3}  ("{k[0]}", "{k[1]}"),')
