# Identifier renames on the improvements fork

## 2026-09-16 — PASCALSYSTEM STUB48/STUB49

| Old | New | Evidence |
|-----|-----|----------|
| `STUB49` | `CANTSTRETCH` | UCSD II.0 `SYSTEM.C.TEXT` (ii0src.sdk); finding **282a** (GOTO shape); finding **165** (body) |
| `STUB48` | `MAINLOOP` | Finding **192** (PASCALSY top-level command loop). Not UCSD's `COMMAND` — Apple's proc 43 is a different routine (`TITLENORM` / finding 51c). `MAINLOOP` matches this repo's name for the same role elsewhere. |

Rename only; no intended code-byte change (identifiers are not stored in p-code). `probe_os_exact` still green against the prior acceptance compile.

## 2026-09-16 — EDITOR Apple-added globals

| Old | New | Role (from reconstruction comments) |
|-----|-----|--------------------------------------|
| `G590` | `DIRTY` | text changed since read/write |
| `G1623` | `WORKNAME` | name of the file being edited |
| `G1664` | `HASNAME` | Save can use that name |
| `G1665` | `REOPEN` | C(hange: start over with another file |
| `G1666` | `CANDOWN` | screen can scroll down |

`EDITOR(XXX,YYY: INTEGER)` left unchanged — UCSD’s own unused parameters
(never referenced in the body). Source-only; `probe_editor_whole` still green.

## 2026-09-16 — FILER volume block counters

| Old | New | Role |
|-----|-----|------|
| `G361` | `DESTBLKS` | blocks on the destination volume |
| `G362` | `SRCBLKS` | blocks on the source volume |

Source-only; `probe_filer_whole` still green (byte-identical to shipped).
