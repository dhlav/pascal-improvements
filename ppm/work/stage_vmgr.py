"""Stage ppm/src/VMGR.TEXT onto WORKHD with the shipped high-ASCII space.

V22's 'Pascal System' error string is one LSA whose byte-$A0 space
encode_text will not accept. Parked: the source keeps a normal space
and we will change it later. This helper is only for matching the
shipped LSA until then.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from a2pascal.srcfmt import expand_tabs
from a2pascal.textfile import Layout, encode_text

CP2 = Path(r"C:\CiderPress2\cp2.exe")
HD2 = ROOT / "build" / "disks" / "HD2.hdv"
SRC = ROOT / "ppm" / "src" / "VMGR.TEXT"
NAME = "VMGR.TEXT"
OLD = b"this Pascal System"
NEW = b"this Pascal" + bytes([0xA0]) + b"System"


def cp2(*args: str, allow_fail: bool = False) -> str:
    r = subprocess.run([str(CP2), *args], capture_output=True, text=True)
    if r.returncode and not allow_fail:
        raise SystemExit(f"cp2 {' '.join(args)} failed:\n{r.stdout}{r.stderr}")
    return r.stdout


def main() -> None:
    if not HD2.exists():
        raise SystemExit("build/disks/HD2.hdv missing; python tools/mkworkhd.py")
    text = expand_tabs(SRC.read_text(encoding="ascii"))
    text = text[:-1] if text.endswith("\n") else text
    payload = encode_text(text, layout=Layout.beside(SRC))
    n = payload.count(OLD)
    if n != 1:
        raise SystemExit(f"{NAME}: {n} copies of {OLD!r}, need 1")
    payload = payload.replace(OLD, NEW, 1)
    cp2("delete", str(HD2), NAME, allow_fail=True)
    staging = Path(tempfile.mkdtemp(prefix="stage-vmgr-"))
    tmp = staging / NAME
    tmp.write_bytes(payload)
    cp2("add", "--raw", "--no-strip-ext", "--strip-paths", str(HD2), str(tmp))
    cp2("set-attr", str(HD2), "type=PTX", NAME)
    shutil.rmtree(staging, ignore_errors=True)
    print(f"{NAME} staged on WORKHD with $A0 in V22")


if __name__ == "__main__":
    main()
