"""Inventory BACKUP.CODE: segments, strings, calls, lifts, natives."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from a2pascal.codefile import CodeFile
from a2pascal.lift import lift, render
from a2pascal.m6502 import disassemble as dis6502
from a2pascal.pcode import disassemble

root = Path(__file__).resolve().parents[2]
cf = CodeFile((root / "ppm" / "BACKUP.CODE").read_bytes())
out_dir = root / "ppm" / "work"


def strings_in(seg, p):
    ins, _ = disassemble(seg.data, p.code_start, p.code_end, p.jtab)
    found = []
    for i in ins:
        if i.mnemonic in ("LSA", "LPA") and i.operands:
            found.append((i.mnemonic, i.operands[0] if isinstance(i.operands[0], str)
                          else i.operands))
        t = i.text
        if "LSA" in t or "LPA" in t:
            if "'" in t:
                found.append(("LIT", t[t.find("'"):]))
    return found


def calls_in(seg, p):
    ins, _ = disassemble(seg.data, p.code_start, p.code_end, p.jtab)
    out = []
    for i in ins:
        if i.mnemonic in ("CXP", "CGP", "CLP", "CIP", "CBP"):
            out.append((i.mnemonic, i.operands))
    return out


lines = []
lines.append(f"copyright {cf.copyright!r}")
lines.append(f"file {len(cf.data)} bytes")
d = cf.data[:512]
lines.append(f"textaddr/segsused @0x120: {d[0x120:0x140].hex()}")
lines.append("")
for seg in cf.segments:
    lines.append(
        f"SEGMENT {seg.number} {seg.name} kind={seg.segkind} "
        f"mtype={seg.mtype} ver={seg.version} len={seg.length} "
        f"block={seg.block} nproc={len(seg.procedures)}"
    )
    for p in seg.procedures:
        kind = "NATIVE" if p.is_native else "pcode"
        lines.append(
            f"  p{p.number:3d} {kind:6s} lex={p.lex_level} "
            f"param={p.param_size:4d} data={p.data_size:5d} "
            f"body={max(0, p.code_end - p.code_start):5d}"
        )
    lines.append("")

lines.append("== strings ==")
for seg in cf.segments:
    for p in seg.procedures:
        if p.is_native:
            continue
        ss = strings_in(seg, p)
        if not ss:
            continue
        for kind, s in ss:
            lines.append(f"  {seg.name}.{p.number} {kind} {s}")

lines.append("")
lines.append("== calls ==")
cxp = Counter()
for seg in cf.segments:
    for p in seg.procedures:
        if p.is_native:
            continue
        for m, ops in calls_in(seg, p):
            key = f"{seg.name}.{p.number} {m} {ops}"
            lines.append(f"  {key}")
            if m == "CXP":
                cxp[(ops[0], ops[1])] += 1

lines.append("")
lines.append("== CXP summary (seg,proc) count ==")
for (s, n), c in sorted(cxp.items()):
    name = next((x.name for x in cf.segments if x.number == s), f"seg{s}")
    lines.append(f"  CXP {s},{n}  {name}.{n}  x{c}")

(out_dir / "BACKUP.inv.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

pas = [
    "BACKUP.CODE -- lifted to pseudo-Pascal",
    "",
    "Storage is named as it is addressed: G<n> global word n,",
    "L<n> local word n. release='' so compiler names are not applied.",
    "",
]
for seg in cf.segments:
    pas.append("=" * 70)
    pas.append(f"SEGMENT {seg.number} {seg.name}")
    pas.append("=" * 70)
    pas.append("")
    for p in seg.procedures:
        if p.is_native:
            pas.append(f"procedure {seg.name}.{p.number};  {{ NATIVE }}")
            pas.append("")
            continue
        try:
            blocks = lift(seg, p, cf, release="")
            hdr = (
                f"procedure {seg.name}.{p.number}"
                f"(args {p.param_size // 2} words);  "
                f"{{ locals {p.data_size // 2} words, lex {p.lex_level} }}"
            )
            pas.append(render(blocks, hdr))
        except Exception as ex:
            pas.append(f"procedure {seg.name}.{p.number};  {{ lift failed: {ex} }}")
        pas.append("")
        pas.append("")

(out_dir / "BACKUP.pas.txt").write_text("\n".join(pas), encoding="utf-8")

nat = ["BACKUP.CODE native procedures", ""]
for seg in cf.segments:
    for p in seg.procedures:
        if not p.is_native:
            continue
        body = seg.data[p.enter_ic:p.content_end if p.content_end > 0 else p.enter_ic + 64]
        nat.append(f"=== {seg.name}.{p.number} enter={p.enter_ic} "
                   f"content_end={p.content_end} bytes={len(body)} ===")
        ins, exact = dis6502(body, 0, len(body))
        for i in ins:
            nat.append(f"  {i.text}")
        nat.append(f"  exact={exact} reloc={ {k: len(v) for k, v in p.reloc.items()} }")
        nat.append("")
(out_dir / "BACKUP.native.txt").write_text("\n".join(nat), encoding="utf-8")

print("wrote BACKUP.inv.txt, BACKUP.pas.txt, BACKUP.native.txt")
print("inv lines", len(lines), "pas chars", sum(len(x) for x in pas))
