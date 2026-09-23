"""Compare the two ProFile Manager disks, then each file to ppm/.

Read-only. Prints a report.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.disk import PascalDisk, format_date

root = Path(__file__).resolve().parents[2]
ppm = root / "ppm"
prog = PascalDisk.from_file(ppm / "Pascal Profile Manager - Program - 680-0251-A.dsk")
star = PascalDisk.from_file(ppm / "Pascal Profile Manager - Program Patched - 680-0251-A.dsk")


def files(disk):
    return {e.name: e for e in disk.directory()}


def body(data):
    try:
        cf = CodeFile(data)
    except Exception as ex:
        return None, str(ex)
    return cf, None


def runs(a, b):
    n = min(len(a), len(b))
    out = []
    i = 0
    while i < n:
        if a[i] != b[i]:
            j = i
            while j < n and a[j] != b[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out, len(a) - n, len(b) - n


fp, fs = files(prog), files(star)
print(f"normal  {prog.volume().name}  {len(fp)} files")
print(f"patched {star.volume().name}  {len(fs)} files")
print()
names = sorted(set(fp) | set(fs))
print(f"{'name':<18} {'normal':>8} {'patched':>8}  note")
for name in names:
    a, b = fp.get(name), fs.get(name)
    sa = f"{a.size}" if a else "-"
    sb = f"{b.size}" if b else "-"
    if a and b:
        da, db = prog.read_file(name), star.read_file(name)
        note = "identical" if da == db else f"DIFFER {sum(x!=y for x,y in zip(da,db))} bytes"
        if len(da) != len(db):
            note += f"  len {len(da)}/{len(db)}"
    elif a:
        note = "only on normal"
    else:
        note = "only on patched"
    print(f"{name:<18} {sa:>8} {sb:>8}  {note}")

print("\n== differing codefiles, by segment ==")
for name in names:
    if name not in fp or name not in fs:
        continue
    da, db = prog.read_file(name), star.read_file(name)
    if da == db:
        continue
    ca, ea = body(da)
    cb, eb = body(db)
    print(f"\n{name}")
    if ca is None or cb is None:
        rs, extra_a, extra_b = runs(da, db)
        print(f"  not both codefiles ({ea}; {eb}); {len(rs)} runs, tail {extra_a}/{extra_b}")
        for i, j in rs[:8]:
            print(f"  {i}..{j-1} ({j-i}b)")
        continue
    na = {s.name: s for s in ca.segments}
    nb = {s.name: s for s in cb.segments}
    print(f"  segments normal {sorted(na)} patched {sorted(nb)}")
    for nm in sorted(set(na) | set(nb)):
        if nm not in na or nm not in nb:
            print(f"  {nm}: only on one side")
            continue
        sa, sb = na[nm], nb[nm]
        xa, xb = sa.data[:sa.length], sb.data[:sb.length]
        flag = "MATCH" if xa == xb else "DIFF"
        print(f"  {flag} {nm} {len(xa)}/{len(xb)} ver {sa.version}/{sb.version} "
              f"num {sa.number}/{sb.number} kind {sa.segkind_raw}/{sb.segkind_raw}")
        if xa != xb:
            rs, ea, eb_ = runs(xa, xb)
            print(f"       {len(rs)} runs, {sum(j-i for i,j in rs)} bytes, tail {ea}/{eb_}")

print("\n== disk files vs ppm/ binaries ==")
pairs = [
    ("PPM.CODE", ppm / "PPM.CODE"),
    ("FILER.CODE", ppm / "FILER.CODE"),
    ("SYSTEM.STARTUP", ppm / "PPM.SYS.STARTUP"),
    ("ATTACH.DATA", ppm / "PPM.ATTCH.DATA"),
    ("ATTACH.DRIVERS", ppm / "PPM.ATTCH.DRVRS"),
    ("SYSTEM.ATTACH", root / "attach" / "SYSTEM.ATTACH"),
]
for disk, label in ((prog, "normal"), (star, "patched")):
    print(f"\n{label}")
    have = files(disk)
    for dname, path in pairs:
        if dname not in have or not path.exists():
            print(f"  {dname}: missing disk={dname in have} local={path.exists()}")
            continue
        da, db = disk.read_file(dname), path.read_bytes()
        if da == db:
            print(f"  {dname}: identical to {path.name} ({len(da)})")
        else:
            n = sum(x != y for x, y in zip(da, db))
            print(f"  {dname}: DIFFER {n} bytes in {min(len(da),len(db))}, "
                  f"len {len(da)}/{len(db)} vs {path.relative_to(root)}")

print("\n== reconstructed codefiles vs the normal disk ==")
recons = [
    ("PPM.CODE", "PASCALPR", ppm / "work" / "PPMLINK.CODE"),
    ("FILER.CODE", "FILEHAND", ppm / "work" / "FILEHAND.CODE"),
    ("SYSTEM.LIBRARY", "CHAINSTU", ppm / "work" / "lib12" / "CHAIN12.CODE"),
]
for dname, segname, path in recons:
    if not path.exists():
        print(f"{dname} {segname}: no {path.name}")
        continue
    disk_cf, _ = body(prog.read_file(dname))
    our_cf, err = body(path.read_bytes())
    if our_cf is None:
        print(f"{path.name}: {err}")
        continue
    def one(cf, name):
        for s in cf.segments:
            if s.name.startswith(name):
                return s
        return None
    a, b = one(disk_cf, segname), one(our_cf, segname)
    if a is None or b is None:
        print(f"{segname}: disk {a is not None} ours {b is not None} "
              f"ours segs {[s.name for s in our_cf.segments]}")
        continue
    xa, xb = a.data[:a.length], b.data[:b.length]
    n = sum(x != y for x, y in zip(xa, xb))
    print(f"{segname}: disk {len(xa)} ver {a.version} vs {path.name} {len(xb)} ver {b.version} "
          f"differ {n} bytes, tail {len(xa)-len(xb)}")
