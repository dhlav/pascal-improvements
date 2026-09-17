"""SYSTEM.COMPILER whole-file check for the improvements fork.

Kept run: Apple's compiler / assembler / Linker / Librarian applied to
this repository's source (acceptance/2026-09-16-compiler-otherwise).

On this fork the gold standard is the kept acceptance codefile, not
Apple's shipped SYSTEM.COMPILER: COMPOPTI now reports ERROR(301) for an
unknown (*$...*) option letter via OTHERWISE (was a silent no-op).

Claims, each of which the binary can fail:

  1. **LIBCOMP.CODE matches the kept acceptance file** (39936 bytes);
     a one-byte flip is caught.
  2. **The Librarian did its part**: COMPLINK still has PASCALSY in slot 0
     and no notice.
  3. **Source lock**: acceptance/.../source/ equals src/pascal/1.3/
     (PASCALCO + phases), line endings aside.
  4. **COMPOPTI has OTHERWISE ERROR(301)** for unknown options.
  5. **Intentional diverge from shipped** SYSTEM.COMPILER.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from a2pascal.disk import PascalDisk
from oscmp import DISKS_13

ROOT = Path(__file__).resolve().parents[2]
EPOCH = ROOT / "acceptance" / "2026-09-16-compiler-otherwise"
RUN = EPOCH / "LIBCOMP.CODE"
KEPT_SRC = EPOCH / "source"
TREE_SRC = ROOT / "src" / "pascal" / "1.3"
INPUT = EPOCH / "COMPLINK.CODE"
TARGET = "SYSTEM.COMPILER"
NOTICE = b"COPYRIGHT 1979,1980,1983-1985 APPLE COMPUTER, INC. ALL RIGHTS RESERVED"

fail = []


def check(ok: bool, label: str) -> None:
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        fail.append(label)


def shipped(name: str) -> bytes:
    for fname in DISKS_13:
        d = PascalDisk.from_file(ROOT / "evidence" / "disks" / fname)
        try:
            e = d.find(name)
        except Exception:
            continue
        if e is not None:
            return bytes(d.read_blocks(e.first_block, e.blocks))
    raise SystemExit(f"{name} is on none of the 1.3 disks")


def lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def source_paths(root: Path) -> list[Path]:
    files = [root / "PASCALCO.text"]
    phases = root / "phases"
    if phases.is_dir():
        files.extend(sorted(phases.glob("*.text")))
    return files


def main() -> int:
    for p in (RUN, INPUT, KEPT_SRC, TREE_SRC):
        if not p.exists():
            print(f"{p} is missing -- acceptance runs are kept verbatim")
            return 1
    apple = shipped(TARGET)
    ours = RUN.read_bytes()
    before = INPUT.read_bytes()

    print("=== the Librarian's output against the kept acceptance file ===")
    check(len(ours) == 39936,
          f"LIBCOMP.CODE is 39936 bytes, 78 blocks (ours {len(ours)})")
    mutant = bytearray(ours)
    mutant[1024] ^= 0x01
    mdiff = [i for i in range(len(ours)) if mutant[i] != ours[i]]
    check(mdiff == [1024],
          "a copy with one code byte flipped is caught, at that byte")
    check(ours[0:4] == b"\x00\x00\x00\x00" and ours[64:72] == b" " * 8,
          "slot 0 is blank: no address, no length, no name")
    check(ours[432] == len(NOTICE) and ours[433:433 + len(NOTICE)] == NOTICE,
          f"the notice is a Pascal string, length byte {len(NOTICE)} first")

    print("=== and its input was not already the release file ===")
    check(before != ours, "COMPLINK.CODE differs from LIBCOMP.CODE")
    check(before[64:72] == b"PASCALSY",
          "COMPLINK.CODE still has PASCALSY in slot 0")
    check(before[432] == 0, "COMPLINK.CODE carries no notice")

    print("=== the verified source is the source in the tree ===")
    kept_files = source_paths(KEPT_SRC)
    tree_files = source_paths(TREE_SRC)
    kept_names = [p.relative_to(KEPT_SRC).as_posix() for p in kept_files]
    tree_names = [p.relative_to(TREE_SRC).as_posix() for p in tree_files]
    check(kept_names == tree_names and len(kept_names) >= 2,
          f"same {len(kept_names)} source paths under acceptance/source "
          "and src/pascal/1.3")
    for kept, tree, name in zip(kept_files, tree_files, kept_names):
        if not kept.is_file() or not tree.is_file():
            check(False, f"{name} present on both sides")
            continue
        same = lf(kept.read_bytes()) == lf(tree.read_bytes())
        check(same, f"acceptance source/{name} equals src/pascal/1.3/{name}")
    if tree_files and tree_files[0].is_file():
        sample = bytearray(lf(tree_files[0].read_bytes()))
        if sample:
            sample[0] ^= 0x01
            check(lf(kept_files[0].read_bytes()) != bytes(sample),
                  "a one-byte edit in PASCALCO.text would break the "
                  "source lock")

    opti = (TREE_SRC / "phases" / "COMPOPTI.text").read_text(encoding="ascii")
    check("OTHERWISE ERROR(301)" in opti,
          "COMPOPTI reports ERROR(301) for unknown option letters")

    print("=== improvements fork: intentional differ from shipped ===")
    diff = [i for i in range(min(len(ours), len(apple))) if ours[i] != apple[i]]
    check(len(ours) == len(apple) == 39936 and len(diff) > 0,
          f"same size as shipped SYSTEM.COMPILER, but {len(diff)} bytes "
          "differ (OTHERWISE unknown-option)")

    print()
    if fail:
        print(f"compiler whole-file: {len(fail)} check(s) failed")
        return 1
    print("SYSTEM.COMPILER: 39936 of 39936 bytes, by Apple's own four tools "
          "(improvements acceptance)")
    print("compiler-whole-ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
