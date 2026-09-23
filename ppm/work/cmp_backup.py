"""Compare BACKUP.CODE segments in a rebuilt codefile to ppm/BACKUP.CODE."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile

root = Path(__file__).resolve().parents[2]
shipped = CodeFile((root / "ppm" / "BACKUP.CODE").read_bytes())
built_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "ppm" / "work" / "BKLINK.CODE"
built = CodeFile(built_path.read_bytes())
want = sys.argv[2] if len(sys.argv) > 2 else None


def seg(cf, name):
    for s in cf.segments:
        if s.name == name:
            return s
    raise SystemExit(f"no segment {name}")


names = [s.name for s in shipped.segments]
if want:
    names = [want]
total_m = total_b = 0
for name in names:
    a = seg(shipped, name)
    try:
        b = seg(built, name)
    except SystemExit:
        print(f"{name}: missing in built")
        total_b += 1
        continue
    print(f"== {name} {a.length} shipped / {b.length} built  "
          f"procs {len(a.procedures)}/{len(b.procedures)} ==")
    n = min(len(a.procedures), len(b.procedures))
    matched = bad = 0
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
    if len(a.procedures) != len(b.procedures):
        print(f"proc count {len(a.procedures)} vs {len(b.procedures)}")
        bad += 1
    print(f"{matched} match, {bad} differ")
    total_m += matched
    total_b += bad
print(f"total {total_m} match, {total_b} differ")
if total_b:
    raise SystemExit(f"{total_b} differ")
print("backup-cmp-ok")
