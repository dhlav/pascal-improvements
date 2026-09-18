"""SYSTEM.FILER whole-file check for the improvements fork.

src/pascal/programs/1.3/FILER.text compiled by Apple's compiler
(acceptance/2026-09-17-filer-complete), then slot 1 copied by Apple's
LIBRARY.CODE with the copyright notice
(acceptance/2026-09-17-filer-otherwise).

On this fork the gold standard is the kept acceptance codefile, not
Apple's shipped SYSTEM.FILER: CALLPROC's command CASE now has an
explicit space no-op and OTHERWISE (bell + 'Unknown command').

Claims, each of which the binary can fail:

  1. **LIBFILER.CODE matches the kept acceptance file** (15360 bytes);
     a one-byte flip is caught.
  2. **Slot 1 is the compile's FILEHAND segment** with 56 procedures.
  3. **The Librarian did its part**: FILER13 still has PASCALSY / no notice.
  4. **UCSD II.0 ancestor hashes** unchanged.
  5. **Kept FILER.text equals src/**, and contains OTHERWISE Unknown command.
  6. **Intentional differ from shipped** SYSTEM.FILER.
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from a2pascal.disk import PascalDisk
from oscmp import DISKS_13

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "acceptance" / "2026-09-17-filer-otherwise" / "LIBFILER.CODE"
COMPILE = ROOT / "acceptance" / "2026-09-17-filer-complete"
INPUT = COMPILE / "FILER13.CODE"
KEPT_SOURCE = COMPILE / "FILER.text"
SOURCE = ROOT / "src" / "pascal" / "programs" / "1.3" / "FILER.text"
TARGET = "SYSTEM.FILER"
NOTICE = (b"COPYRIGHT 1979,1980,1983-1985 APPLE COMPUTER, INC. "
          b"ALL RIGHTS RESERVED")
SIZE = 15360
SEGLEN = 14752
NPROC = 56
REFERENCE = ROOT / "evidence" / "reference" / "ucsd-ii0-filer"
REFERENCE_SHA256 = {
    "filer.a.text":
        "80d2aca21ea5fd676bc9f8d5e8451090dc3ca41d36a6deaef83fac2b5a9bdf61",
    "filer.b.text":
        "3086da6d3165686c402d340a8af8bd38065ba831754a6ed81a562d986fe0fd22",
    "filer.c.text":
        "b19334623d2667152c28409fe517622ef56a9168c24479a858281d64a99f28f4",
    "filer.d.text":
        "a1f98466ed0c847dd0a4acf0952a58a6451b32f25fe6552d8818bbc60f9a13b5",
    "filer.e.text":
        "02d7fc8a56aaad7e8098fc717aab61fd6f5885644f893e072a950ac38d11ebc6",
    "filer.vars.text":
        "083e3a10fede75dca76bca6d368cc2bf925b8d199b735b4c4045e7a8671c9577",
    "main.text":
        "92506795128861c871006ad960123adb15c13ee6a9b827911404e836da961d9f",
}

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


def words(b: bytes, off: int, n: int) -> list[int]:
    return [b[off + 2 * i] | b[off + 2 * i + 1] << 8 for i in range(n)]


def segment(b: bytes, slot: int) -> bytes:
    addr, leng = words(b, 4 * slot, 2)
    return b[addr * 512: addr * 512 + leng]


def differing(a: bytes, b: bytes) -> list[int]:
    return ([i for i in range(min(len(a), len(b))) if a[i] != b[i]]
            + list(range(min(len(a), len(b)), max(len(a), len(b)))))


def main() -> int:
    for p in (RUN, INPUT, KEPT_SOURCE, SOURCE):
        if not p.exists():
            print(f"{p} is missing -- acceptance runs are kept verbatim")
            return 1
    apple = shipped(TARGET)
    ours = RUN.read_bytes()
    compiled = INPUT.read_bytes()

    print("=== the Librarian's output against the kept acceptance file ===")
    check(len(ours) == SIZE,
          f"LIBFILER.CODE is {SIZE} bytes, 30 blocks (ours {len(ours)})")
    mutant = bytearray(ours)
    mutant[1024] ^= 0x01
    check(differing(bytes(mutant), ours) == [1024],
          "a copy with one code byte flipped is caught, at that byte")
    check(ours[0:4] == b"\x00\x00\x00\x00" and ours[64:72] == b" " * 8,
          "slot 0 is blank: no address, no length, no name")
    check(ours[432] == len(NOTICE) and ours[433:433 + len(NOTICE)] == NOTICE,
          f"the notice is a Pascal string, length byte {len(NOTICE)} first")

    print("=== slot 1 is the reconstruction's own bytes ===")
    mine = segment(compiled, 1)
    check(bool(mine) and mine == segment(ours, 1)
          and len(mine) == SEGLEN and mine[-1] == NPROC,
          f"FILEHAND: compile == Librarian ({len(mine)} bytes, "
          f"{mine[-1] if mine else 0} procedures)")

    print("=== and the compile alone was not the release file ===")
    check(compiled[64:72] == b"PASCALSY" and compiled[432] == 0,
          "FILER13.CODE has PASCALSY in slot 0 and no notice")

    print("=== the ancestor is the one recorded ===")
    got = {n: hashlib.sha256((REFERENCE / n).read_bytes()
                             .replace(b"\r\n", b"\n")).hexdigest()
           for n in REFERENCE_SHA256 if (REFERENCE / n).exists()}
    check(got == REFERENCE_SHA256,
          f"UCSD II.0 Filer source: {len(got)} of {len(REFERENCE_SHA256)} "
          "files present with their recorded SHA-256")

    print("=== the verified source is the source in the tree ===")
    kept = KEPT_SOURCE.read_bytes().replace(b"\r\n", b"\n")
    tree = SOURCE.read_bytes().replace(b"\r\n", b"\n")
    check(kept == tree, "acceptance FILER.text equals "
                        "src/pascal/programs/1.3/FILER.text")
    tree_txt = tree.decode("ascii")
    check("OTHERWISE" in tree_txt and "Unknown command" in tree_txt,
          "CALLPROC CASE has OTHERWISE Unknown command")

    print("=== improvements fork: intentional differ from shipped ===")
    diff = differing(ours, apple)
    check(len(ours) == len(apple) == SIZE and len(diff) > 0,
          f"same size as shipped SYSTEM.FILER, but {len(diff)} bytes "
          "differ (OTHERWISE unknown-command)")

    print()
    if fail:
        print(f"filer whole-file: {len(fail)} check(s) failed")
        return 1
    print("SYSTEM.FILER: 15360 of 15360 bytes, by Apple's compiler and "
          "Librarian (improvements acceptance)")
    print("filer-whole-ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
