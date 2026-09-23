"""Print the differing FILEHAND body bytes. Scratch."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile

root = Path(__file__).resolve().parents[2]


def seg(cf):
    for s in cf.segments:
        if s.name == "FILEHAND":
            return s


a = CodeFile((root / "ppm" / "FILER.CODE").read_bytes())
b = CodeFile((root / "ppm" / "work" / "FILEHAND.CODE").read_bytes())
sa, sb = seg(a), seg(b)
for i, (pa, pb) in enumerate(zip(sa.procedures, sb.procedures), 1):
    ba = sa.data[pa.code_start:pa.code_end]
    bb = sb.data[pb.code_start:pb.code_end]
    if ba == bb:
        continue
    print(f"proc {i} {len(ba)}/{len(bb)}")
    n = min(len(ba), len(bb))
    for k in range(n):
        if ba[k] != bb[k]:
            def ch(v):
                return chr(v) if 32 <= v < 127 else "."
            print(f"  +{k}: {ba[k]:02X} {ch(ba[k])} -> {bb[k]:02X} {ch(bb[k])}")
    if len(ba) != len(bb):
        print(f"  length {len(ba)} vs {len(bb)}")
