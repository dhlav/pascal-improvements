"""Compare a rebuilt codefile's procedure bodies to a shipped one.

    python attach/work/cmp_attach.py ATTACHUD.CODE work/ATTACHUD.CODE
    python attach/work/cmp_attach.py SYSTEM.ATTACH work/SYSATCH.CODE SYSATCH

Bodies are the bytes from each procedure's entry to its code_end
(jtab-8). Native procedures are compared from entry to content_end.
The segment-dictionary version nibble is not part of a body.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from a2pascal.codefile import CodeFile

shipped_path = Path(sys.argv[1])
built_path = Path(sys.argv[2])
want = sys.argv[3] if len(sys.argv) > 3 else None
shipped = CodeFile(shipped_path.read_bytes())
built = CodeFile(built_path.read_bytes())


def pick(cf):
    if want:
        for s in cf.segments:
            if s.name == want:
                return s
        raise SystemExit(f"no segment {want} in {cf}")
    if len(cf.segments) != 1:
        names = ", ".join(s.name for s in cf.segments)
        raise SystemExit(f"name the segment ({names})")
    return cf.segments[0]


a = pick(shipped)
b = pick(built)
print(f"{a.name} {a.length} shipped / {b.length} built  "
      f"ver {a.version}/{b.version} kind {a.segkind}/{b.segkind}")
na, nb = len(a.procedures), len(b.procedures)
print(f"procs {na} / {nb}")
bad = 0
n = min(na, nb)
for i in range(n):
    pa, pb = a.procedures[i], b.procedures[i]
    if pa.is_native or pb.is_native:
        ba = a.data[pa.enter_ic:pa.content_end]
        bb = b.data[pb.enter_ic:pb.content_end]
        kind = "nat"
    else:
        ba = a.data[pa.code_start:pa.code_end]
        bb = b.data[pb.code_start:pb.code_end]
        kind = "p"
    ok = ba == bb
    if not ok:
        bad += 1
    flag = "MATCH" if ok else "DIFF"
    print(f"{flag} {kind} {i+1:2d}  {len(ba):5d}/{len(bb):5d}"
          f"  lex {pa.lex_level}/{pb.lex_level}"
          f"  param {pa.param_size}/{pb.param_size}"
          f"  data {pa.data_size}/{pb.data_size}")
if na != nb:
    bad += abs(na - nb)
if bad:
    raise SystemExit(f"{bad} differ")
print("attach-cmp-ok")
