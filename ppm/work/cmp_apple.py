"""Which known interpreter is the patched disk's SYSTEM.APPLE?"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.disk import PascalDisk

root = Path(__file__).resolve().parents[2]
star = PascalDisk.from_file(
    root / "ppm" / "Pascal Profile Manager - Program Patched - 680-0251-A.dsk")
apple = star.read_file("SYSTEM.APPLE")
print(f"patched SYSTEM.APPLE {len(apple)} bytes")
for p in sorted((root / "evidence" / "disks").glob("*.dsk")):
    d = PascalDisk.from_file(p)
    for e in d.directory():
        if "APPLE" not in e.name:
            continue
        data = d.read_file(e.name)
        if len(data) != len(apple):
            print(f"  {p.name} {e.name} len {len(data)}")
            continue
        n = sum(x != y for x, y in zip(data, apple))
        print(f"  {p.name} {e.name} differ {n}")
