"""Build the hard-disk image the HD acceptance tier mounts.

The floppy tier's four volumes (BOOT128, APPLE2, WORK, WORK2) fold onto one
2MB Pascal hard-disk volume here, on the Hard Disk Controller card in slot 5
(`-s5 hdc`, `-s5h1` only -- `-s5h2` is not used):

  SYSHD  (`build/disks/HD1.hdv`)  boots the machine, carries every system
         tool Apple shipped -- SYSTEM.APPLE/PASCAL (128K), EDITOR, FILER,
         LIBRARY, MISCINFO, CHARSET, SYNTAX, ASSMBLER, COMPILER, LINKER,
         LIBRARY.CODE, LIBMAP.CODE, 6502.OPCODES, 6502.ERRORS -- plus
         BINDER.CODE and SET40COLS.CODE off APPLE3 (1.1 binaries Apple
         never rebuilt for 1.3, PLAN.md item 3 -- carried over as shipped
         so they can be run and compared, not yet reconstructed) -- and
         also carries the same reconstructed source mkworkdisk.py puts on
         WORK.dsk, and where compiler/assembler/linker output lands.

**This was two volumes (SYSHD + WORKHD) briefly.** A single UCSD Pascal
volume claims *all* currently-free contiguous space for a new file at
creation and shrinks it back down on a clean close -- so `SYSTEM.ASSMBLER`
creating its own `%LINKER.INFO` scratch file and the output codefile on the
*same* volume raced for that one free run, and the second file got "I/O
error: no room on volume" even with thousands of blocks free (finding: HD
acceptance session, 2026-08-26). This is not a bug in this repo's tooling --
it is exactly the situation the Apple II Pascal manual describes and gives
the fix for (ch. 3 "File Size Specification", ch. 5 "Allocating File
Space"): a single-drive system must give the output codefile an explicit
size, `NAME.CODE[*]` (second-largest contiguous area, or half the largest,
whichever is more) rather than the `[0]` default (the entire largest area).
`emucompile.ps1`/`emuassemble.ps1`/`emulink.ps1` type the `[*]` suffix on
every codefile they create for exactly this reason -- it is not optional on
this one-volume layout the way it would be with system tools and output on
separate volumes.

**A Pascal volume is limited to 77 files regardless of size** (`cp2`'s own
manual) -- the directory is four fixed 512-byte blocks of 26-byte entries,
78 slots, the first of which is the volume itself. 2MB of space does not
relax that. The 15 system tools plus this module's own FILES list plus
whatever a session's compiler/assembler/linker runs add on top of it (each a
new .CODE, plus a stray .TEXT from testing) needs watching against that
ceiling far sooner than against space -- `main()` checks it after every
build and fails loudly rather than let cp2's own directory-full error be the
first anyone hears of it.

Two things a 5.25" floppy volume never has to worry about, and a hard disk
always does:

  * **a2pascal/disk.py and diskwrite.py do not reach this size.** They assume
    the 35-track/16-sector DOS-order geometry of a 143,360-byte volume; a 2MB
    hard-disk image is a flat run of 512-byte blocks with no track/sector
    skew at all, a different (simpler) format this repo has no reader for.
    So this shells out to CiderPress II's `cp2.exe`, which understands the
    Pascal directory format at any size, instead.
  * **volume names must be distinct from any other volume online at once.**
    `cp2 create-disk-image ... pascal` always names a fresh volume
    `NEWDISK`; two same-named volumes online at once left the Filer unable
    to tell them apart -- `A(ssem` searched `NEWDISK:` for `SYSTEM.ASSMBLER`
    and silently found the *other* one, empty, volume (finding: HD
    acceptance session, 2026-08-26). Not a live concern with only one HD
    volume mounted, but renamed off `NEWDISK` here regardless, since nothing
    stops a floppy or a second hard disk called `NEWDISK` from also being
    online in the same session.

Requires `C:\\CiderPress2\\cp2.exe` (CiderPress II) and boots via SmartPort
firmware, which AppleWin only defaults to for `-model apple2ee` (the
*enhanced* //e) -- `apple2e` still uses the older v2 HDC firmware and never
gets past the `Apple //e` splash. See `runemu.py --hd`.

Writes build/disks/HD1.hdv.
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a2pascal.srcfmt import WIDTH, expand_tabs, over_width
from a2pascal.textfile import encode_text

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "disks"
CP2 = Path(r"C:\CiderPress2\cp2.exe")
BOOT128 = OUT / "BOOT128.dsk"
APPLE2 = ROOT / "evidence" / "disks" / "Apple II Pascal 1.3 APPLE2_ 680-0284-A.dsk"

HD1 = OUT / "HD1.hdv"
MAX_FILES = 77   # cp2's own ceiling for a Pascal volume, any size
APPLE3 = ROOT / "evidence" / "disks" / "Apple II Pascal 1.3 APPLE3_ 680-0290-A.dsk"

# Shipped codefiles Apple never rebuilt for 1.3 (finding 99c/PLAN.md item 3)
# -- carried over from APPLE3 as-is so they can be run and compared, not
# reconstructed source. Copied with cp2's own "copy" so the bytes are
# whatever the evidence disk has, untouched by this repo's tools.
EVIDENCE_CODEFILES = ["BINDER.CODE", "SET40COLS.CODE", "SETUP.CODE"]

# Same list mkworkdisk.py puts on WORK.dsk -- see that module for why each
# one is here and why the names are what they are.
FILES = [
    ("SEARCH.TEXT", ROOT / "src" / "native" / "SEARCH.TEXT"),
    ("SKEL13.TEXT", ROOT / "analysis" / "reconstruction" / "skeleton-1.3.text"),
    # SKEL11 dropped: 1.1 is archived; srcskel.py only emits the 1.3 skeleton.
    ("LINEFEED.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "LINEFEED.text"),
    ("FORMATTR.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "FORMATTER.text"),
    ("FMTNATIV.TEXT", ROOT / "src" / "native" / "FORMATTR.TEXT"),
    # LIBMAPT, not LIBMAP: Apple's own shipped LIBMAP.CODE is already on
    # this volume (a system tool, copied in with APPLE2 above) and the
    # compiler writes its output beside the source, so compiling under
    # LIBMAP's own name would overwrite it.
    ("LIBMAPT.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "LIBMAP.text"),
    # SET40T, not SET40COLS: Apple's own shipped SET40COLS.CODE is already
    # on this volume (EVIDENCE_CODEFILES above) and the compiler writes
    # its output beside the source, so compiling under SET40COLS' own
    # name would overwrite it.
    ("SET40T.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "SET40COLS.text"),
    # LIBRARYT, not LIBRARY: Apple's own shipped LIBRARY.CODE is already
    # on this volume (a system tool, copied in with APPLE2 above) and the
    # compiler writes its output beside the source, so compiling under
    # LIBRARY's own name would overwrite it.
    ("LIBRARYT.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "LIBRARY.text"),
    # BINDERT, not BINDER: Apple's own shipped BINDER.CODE is already on
    # this volume (EVIDENCE_CODEFILES above) and the compiler writes its
    # output beside the source, so compiling under BINDER's own name
    # would overwrite it.
    ("BINDERT.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "BINDER.text"),
    # SETUPT, not SETUP: Apple's own shipped SETUP.CODE is already on
    # this volume (EVIDENCE_CODEFILES above) and the compiler writes its
    # output beside the source, so compiling under SETUP's own name
    # would overwrite it.
    ("SETUPT.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "SETUP.text"),
    # PASCALSY, not SYSTEM.PASCAL: the OS reconstruction. The volume boots
    # from its own SYSTEM.PASCAL, so compiling under that name would
    # overwrite the running system. The shipped binary this is compared
    # against is 128K.PASCAL on APPLE3, not the 64K SYSTEM.PASCAL.
    ("PASCALSY.TEXT", ROOT / "src" / "pascal" / "os" / "1.3" /
     "PASCALSYSTEM.text"),
    # Its one include, `(*$I USESFIO.TEXT*)` (finding 280). An include
    # with no volume opens on the prefix, which is this boot volume, so it
    # lives here even when PASCALSY.TEXT is compiled from WORKHD.
    ("USESFIO.TEXT", ROOT / "src" / "pascal" / "os" / "1.3" / "USESFIO.text"),
    # ASSMBLER.TEXT compiles to ASSMBLER.CODE, which does not collide with
    # the shipped SYSTEM.ASSMBLER beside it -- a volume filename is 15
    # characters, and only Pascal IDENTIFIERS stop at 8.
    ("ASSMBLER.TEXT", ROOT / "src" / "pascal" / "programs" / "1.3" /
     "ASSMBLER.text"),
    # Not part of the disk set -- the two halves of the remote console
    # (findings 210/211). They live here so the bootstrap survives a
    # rebuild: `emuremote.py` needs REDIRIO.CODE on the volume before it
    # can drive anything, and the only way to get a codefile onto SYSHD is
    # to compile it there. REMTEST is the transport-only diagnostic, kept
    # alongside so that when the channel goes quiet there is something
    # that isolates which half broke.
    ("REDIRIO.TEXT", ROOT / "tools" / "remote" / "REDIRIO.text"),
    ("REMTEST.TEXT", ROOT / "tools" / "remote" / "REMTEST.text"),
]


def cp2(*args: str) -> str:
    r = subprocess.run([str(CP2), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit(f"cp2 {' '.join(args)} failed:\n{r.stdout}{r.stderr}")
    return r.stdout


def main() -> int:
    if not CP2.exists():
        raise SystemExit(f"{CP2} not found -- CiderPress II is required "
                         "for hard-disk images (a2pascal only reads/writes "
                         "5.25\" floppy geometry)")
    if not BOOT128.exists():
        raise SystemExit("build/disks/BOOT128.dsk has not been built "
                         "(python tools/mkbootdisk.py)")
    OUT.mkdir(parents=True, exist_ok=True)

    HD1.unlink(missing_ok=True)
    cp2("create-disk-image", str(HD1), "2M", "pascal")
    cp2("move", str(HD1), ":", "SYSHD")
    cp2("copy", str(BOOT128), str(HD1))
    cp2("copy", str(APPLE2), str(HD1))
    cp2("copy", str(APPLE3), *EVIDENCE_CODEFILES, str(HD1))

    scratch = OUT / "hd-scratch"
    scratch.mkdir(exist_ok=True)
    for name, path in FILES:
        if not path.exists():
            raise SystemExit(f"{path} has not been generated")
        text = expand_tabs(path.read_text(encoding="ascii", errors="replace"))
        text = text[:-1] if text.endswith("\n") else text
        long = over_width(text.split("\n"))
        if long:
            raise SystemExit(
                f"{name}: {len(long)} lines exceed {WIDTH} columns "
                f"{long[:5]} -- fix the generator, not the disk")
        tmp = scratch / name
        tmp.write_bytes(encode_text(text))
        cp2("add", "--raw", "--no-strip-ext", "--strip-paths", str(HD1),
            str(tmp))
        cp2("set-attr", str(HD1), "type=PTX", name)
    shutil.rmtree(scratch)

    out = cp2("catalog", str(HD1))
    if '"SYSHD"' not in out:
        raise SystemExit(f"{HD1.name} did not come up named SYSHD:\n{out}")
    nfiles = sum(1 for line in out.splitlines()[2:] if line.strip())
    if nfiles > MAX_FILES:
        raise SystemExit(f"{HD1.name}: {nfiles} files, over the {MAX_FILES} "
                         "a Pascal volume can hold regardless of size")
    print(out, end="")
    print(f"{nfiles}/{MAX_FILES} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
