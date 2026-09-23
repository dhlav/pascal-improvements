"""Dump shipped vs built VMGR procedures that differ."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.pcode import disassemble

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
want = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
n = min(len(a.procedures), len(b.procedures))
for i in range(n):
    pa, pb = a.procedures[i], b.procedures[i]
    ba = a.data[pa.code_start:pa.code_end]
    bb = b.data[pb.code_start:pb.code_end]
    if ba == bb:
        continue
    if want and (i + 1) not in want:
        continue
    print("=" * 72)
    print(f"proc {i+1}  shipped {len(ba)} built {len(bb)}"
          f"  param {pa.param_size}/{pb.param_size}"
          f"  data {pa.data_size}/{pb.data_size}")
    ins_a, _ = disassemble(a.data, pa.code_start, pa.code_end, pa.jtab)
    ins_b, _ = disassemble(b.data, pb.code_start, pb.code_end, pb.jtab)
    la, lb = [x.text for x in ins_a], [x.text for x in ins_b]
    ma, mb = len(la), len(lb)
    m = max(ma, mb)
    # print aligned, skip identical prefix/suffix runs of 3+
    first = 0
    while first < ma and first < mb and la[first] == lb[first]:
        first += 1
    last_a, last_b = ma, mb
    while last_a > first and last_b > first and la[last_a - 1] == lb[last_b - 1]:
        last_a -= 1
        last_b -= 1
    if first:
        print(f"  ... {first} matching instructions ...")
    for k in range(min(last_a, last_b) - first):
        sa, sb = la[first + k], lb[first + k]
        mark = "  " if sa == sb else "!!"
        print(f"{mark} S {la[first + k]}")
        if sa != sb:
            print(f"   B {lb[first + k]}")
    if last_a - first > last_b - first:
        for k in range(last_b, last_a):
            print(f"!! S {la[k]}")
            print(f"   B <missing>")
    elif last_b - first > last_a - first:
        for k in range(last_a, last_b):
            print(f"!! S <missing>")
            print(f"   B {lb[k]}")
    rest = ma - last_a
    if rest:
        print(f"  ... {rest} matching instructions ...")
    print()
