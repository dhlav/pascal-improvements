"""Match VOLUMEMA and VMGR procedures to PASCALPR by opcode text."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.pcode import disassemble

root = Path(__file__).resolve().parents[2]
cf = CodeFile((root / "ppm" / "PPM.CODE").read_bytes())
segs = {s.name: s for s in cf.segments}


def texts(seg, p):
    ins, _ = disassemble(seg.data, p.code_start, p.code_end, p.jtab)
    out = []
    for i in ins:
        t = i.text
        # drop absolute jump targets
        if " $" in t:
            t = t.split(" $")[0]
        out.append(t)
    return tuple(out)


def index(name):
    seg = segs[name]
    return {texts(seg, p): p.number for p in seg.procedures}


pr = index("PASCALPR")
print("VOLUMEMA vs PASCALPR")
for p in segs["VOLUMEMA"].procedures:
    key = texts(segs["VOLUMEMA"], p)
    hit = pr.get(key)
    print(f"  vol p{p.number:3d} {p.code_end-p.code_start:4d}b -> "
          f"{'PASCALPR p'+str(hit) if hit else 'unique'}")

print("VMGR vs PASCALPR")
for p in segs["VMGR"].procedures:
    key = texts(segs["VMGR"], p)
    hit = pr.get(key)
    if hit:
        print(f"  vmgr p{p.number:3d} {p.code_end-p.code_start:4d}b -> PASCALPR p{hit}")
