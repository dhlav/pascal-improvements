"""Compare assembled BKFORMAT.CODE blocks 1-3 to ppm/BACKUP.DATA."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
ship = (root / "ppm" / "BACKUP.DATA").read_bytes()
code_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "ppm" / "work" / "BKFORMAT.CODE"
code = code_path.read_bytes()
got = code[512:512 + 1536]
print(f"BACKUP.DATA {len(ship)}  {code_path.name} blocks 1-3 {len(got)}")
if got == ship:
    print("1536/1536 match")
    print("backup-data-ok")
    raise SystemExit(0)
n = min(len(got), len(ship))
diffs = [i for i in range(n) if got[i] != ship[i]]
print(f"{len(diffs)} differ, first +{diffs[0] if diffs else 'n/a'}")
for i in diffs[:20]:
    print(f"  +{i:04X} built={got[i]:02X} ship={ship[i]:02X}")
raise SystemExit(f"{len(diffs)} differ")
