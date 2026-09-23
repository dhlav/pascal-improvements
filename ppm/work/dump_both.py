"""Dump one VMGR procedure from shipped and built."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.pcode import disassemble

root = Path(__file__).resolve().parents[2]
shipped = CodeFile((root / "ppm" / "PPM.CODE").read_bytes())
built = CodeFile((root / "ppm" / "work" / "PPMLINK.CODE").read_bytes())


def seg(cf, name):
    for s in cf.segments:
        if s.name == name:
            return s
    raise SystemExit(f"no segment {name}")


def dump(cf, n, tag):
    s = seg(cf, "VMGR")
    p = s.procedures[n - 1]
    ins, exact = disassemble(s.data, p.code_start, p.code_end, p.jtab)
    print(f"=== {tag} p{n} {p.code_end-p.code_start}b lex {p.lex_level} "
          f"param {p.param_size} data {p.data_size} enter {p.enter_ic} "
          f"exact={exact} ===")
    for i in ins:
        print(f"  {i.text}")
    print()


n = int(sys.argv[1])
dump(shipped, n, "SHIP")
dump(built, n, "BUILT")
