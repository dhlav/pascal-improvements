"""Disassemble VOLUMEMA procedures from ppm/PPM.CODE."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.pcode import disassemble

root = Path(__file__).resolve().parents[2]
cf = CodeFile((root / "ppm" / "PPM.CODE").read_bytes())
seg = next(s for s in cf.segments if s.name == "VOLUMEMA")
want = [int(x) for x in sys.argv[1:]] or [1, 3, 6, 8, 5, 4]
for n in want:
    p = seg.procedures[n - 1]
    ins, exact = disassemble(seg.data, p.code_start, p.code_end, p.jtab)
    print(f"=== p{n} {p.code_end-p.code_start}b lex {p.lex_level} "
          f"param {p.param_size} data {p.data_size} exact={exact} ===")
    for i in ins:
        print(f"  {i.text}")
    print()
