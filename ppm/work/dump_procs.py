"""Side-by-side p-code of two FILEHAND procedures. Generated scratch."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.pcode import disassemble

root = Path(__file__).resolve().parents[2]
shipped = CodeFile((root / "ppm" / "FILER.CODE").read_bytes())
built = CodeFile((root / "ppm" / "work" / "FILEHAND.CODE").read_bytes())


def seg(cf, name):
    for s in cf.segments:
        if s.name == name:
            return s
    raise SystemExit(f"no segment {name}")


a = seg(shipped, "FILEHAND")
b = seg(built, "FILEHAND")
want = [int(x) for x in sys.argv[1:]] or [47, 2]


def insns(segm, n):
    p = segm.procedures[n - 1]
    body = segm.data[p.code_start:p.code_end]
    # decode against the segment so jump targets resolve
    got, exact = disassemble(segm.data, p.code_start, p.code_end, p.jtab)
    return p, got, exact


for n in want:
    pa, ia, ea = insns(a, n)
    pb, ib, eb = insns(b, n)
    print(f"=== proc {n} shipped {pa.code_end-pa.code_start}b "
          f"{len(ia)} ins exact={ea}  built {pb.code_end-pb.code_start}b "
          f"{len(ib)} ins exact={eb} ===")
    limit = 40 if n == 47 else 10**9
    for i, ins in enumerate(ia[:limit]):
        print(f"S {i:3d} {ins.text}")
    if n == 47:
        print("--- built head ---")
        for i, ins in enumerate(ib[:limit]):
            print(f"B {i:3d} {ins.text}")
    else:
        ta = [i.text for i in ia]
        tb = [i.text for i in ib]
        import difflib
        for line in difflib.unified_diff(ta, tb, fromfile="shipped",
                                          tofile="built", lineterm="", n=3):
            print(line)
    print()
