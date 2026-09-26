"""Stage ppm/src/BACKUP.TEXT onto WORKHD.

P13's prompt set is a character constant whose value is ESC
(byte 27). encode_text rejects that byte, so this helper
swaps it for a tilde while encoding and puts ESC back into
the text file the compiler reads. CHR(27) compiles to
SGS+UNI; the constant folds into one LDC.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from a2pascal.srcfmt import expand_tabs, over_width, WIDTH
from a2pascal.textfile import encode_text

CP2 = Path(r"C:\CiderPress2\cp2.exe")
HD2 = ROOT / "build" / "disks" / "HD2.hdv"
SRC = ROOT / "ppm" / "src" / "BACKUP.TEXT"
NAME = "BACKUP.TEXT"
MARK = b"'\x1b'"
STAND = b"'~'"


def cp2(*args: str, allow_fail: bool = False) -> str:
    r = subprocess.run([str(CP2), *args], capture_output=True, text=True)
    if r.returncode and not allow_fail:
        raise SystemExit(f"cp2 {' '.join(args)} failed:\n{r.stdout}{r.stderr}")
    return r.stdout


def main() -> None:
    if not HD2.exists():
        raise SystemExit("build/disks/HD2.hdv missing; python tools/mkworkhd.py")
    raw = SRC.read_bytes().replace(b"\r\n", b"\n")
    n = raw.count(MARK)
    if n != 1:
        raise SystemExit(f"{NAME}: {n} ESC character constants, need 1")
    if b"'~'" in raw:
        raise SystemExit(f"{NAME}: already contains a '~' character constant")
    text = expand_tabs(raw.replace(MARK, STAND, 1).decode("ascii"))
    text = text[:-1] if text.endswith("\n") else text
    long = over_width(text.split("\n"))
    if long:
        raise SystemExit(f"{NAME}: {len(long)} lines exceed {WIDTH} columns")
    payload = encode_text(text)
    m = payload.count(STAND)
    if m != 1:
        raise SystemExit(f"encoded {NAME}: {m} stand-ins, need 1")
    payload = payload.replace(STAND, MARK, 1)
    cp2("delete", str(HD2), NAME, allow_fail=True)
    staging = Path(tempfile.mkdtemp(prefix="stage-backup-"))
    tmp = staging / NAME
    tmp.write_bytes(payload)
    cp2("add", "--raw", "--no-strip-ext", "--strip-paths", str(HD2), str(tmp))
    cp2("set-attr", str(HD2), "type=PTX", NAME)
    shutil.rmtree(staging, ignore_errors=True)
    print(f"{NAME} staged on WORKHD with ESC in P13")


if __name__ == "__main__":
    main()
