"""Compare VMGR procedure bodies in a rebuilt codefile to ppm/PPM.CODE."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile

root = Path(__file__).resolve().parents[2]
shipped = CodeFile((root / "ppm" / "PPM.CODE").read_bytes())
built_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "ppm" / "work" / "PPMLINK.CODE"
built = CodeFile(built_path.read_bytes())


def seg(cf, name):
    for s in cf.segments:
        if s.name == name:
            return s
    raise SystemExit(f"no segment {name}")


a = seg(shipped, "VMGR")
b = seg(built, "VMGR")
print(f"segment {a.length} shipped / {b.length} built")
print(f"data {a.procedures[0].data_size} shipped / {b.procedures[0].data_size} built")
na, nb = len(a.procedures), len(b.procedures)
print(f"procs {na} shipped / {nb} built")
n = min(na, nb)
bad = 0
matched = 0
for i in range(n):
    pa, pb = a.procedures[i], b.procedures[i]
    ba = a.data[pa.code_start:pa.code_end]
    bb = b.data[pb.code_start:pb.code_end]
    ok = ba == bb
    if ok:
        matched += 1
    else:
        bad += 1
    flag = "MATCH" if ok else "DIFF"
    print(f"{flag} proc {i+1:3d}  {len(ba):5d} / {len(bb):5d}"
          f"  lex {pa.lex_level}/{pb.lex_level}"
          f"  param {pa.param_size}/{pb.param_size}"
          f"  data {pa.data_size}/{pb.data_size}")
    if not ok:
        nshow = min(len(ba), len(bb))
        at = next((k for k in range(nshow) if ba[k] != bb[k]), nshow)
        print(f"       first diff at +{at}")
if na != nb:
    print(f"proc count {na} vs {nb}")
    bad += 1
print(f"{matched} match, {bad} differ")
if bad:
    raise SystemExit(f"{bad} differ")
print("vmgr-cmp-ok")
