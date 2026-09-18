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

## 2026-09-17 — LINKER flags

| Old | New | Role |
|-----|-----|------|
| `G91` | `WORDHEAP` | heap pointers count words |
| `L12` | `INTRLINK` | linking an intrinsic unit |

Source-only; `probe_linker_whole` still green (byte-identical to shipped).

## 2026-09-17 — LINKER host slot

| Old | New | Role |
|-----|-----|------|
| `G29` | `HOSTSLOT` | host segment's slot (`MAXSEG1` if none) |

(`HOSTSEG` collides with an existing name.) Source-only; linker probe still green.

## 2026-09-17 — GETCMD GC* helpers (STRONG INFERENCE names)

English names invented from FINDINGS **225–228** role prose (not recovered
UCSD identifiers). Source-only; `probe_os_exact` still green.

| Old | New | Role (FINDINGS) |
|-----|-----|-----------------|
| `GC05` | `SEGOFENT` | segment number of dictionary entry `.5` |
| `GC07` | `FIXINTR` | sanitize `INTRINSSEGS` by host `VERSION` `.7` |
| `GC08` | `CLRINTR` | clear high half of `INTRINSSEGS` `.8` |
| `GC09` | `BINDSEGS` | bind codefile segs into `SEGTABLE` `.9` |
| `GC10` | `FILLSEGS` | fill `SEGS` set from dictionary `.10` |
| `GC11` | `USELIB` | open `.LIB` / merge into `WHAT_L` `.11` |
| `GC12` | `NEEDLIBS` | `INTRINSSEGS <> WHAT_L` `.12` |
| `GC13` | `MERGELIB` | merge one library dict into `WHAT_L` `.13` |
| `GC14` | `OPENLIB` | open one library title `.14` |
| `GC15` | `SPLITLIB` | split `LIBRARY FILES:` list `.15` |
| `GC16` | `LIBKIND` | library codefile vs text list `.16` |
| `GC17` | `TOUPPER` | upshift fourteen characters `.17` |
| `GC18` | `MAKELIB` | build `vol:name.LIB` title `.18` |
| `GC21` | `TRIMLEAD` | strip leading spaces from compile title `.21` |
| `GC22` | `AFTERCMP` | after-compile cleanup / run `.22` |
| `GC24` | `NEWEXBUF` | allocate EXEC write buffer `.24` |

## 2026-09-17 — LINKER / LIBRARY / FILER leftover helpers

Comment-backed (or body+comment) roles. Source-only; linker/filer/library
probes still green.

### LINKER
| Old | New | Role |
|-----|-----|------|
| `LK2` | `CLOSEINS` | close every input file |
| `LK3` | `QUITLINK` | close everything and leave |
| `LK17` | `STRIPDLE` | drop leading DLE blank-compression from a typed name |
| `LK51` | `CHECKVER` | require 1.3 SYSTEM.PASCAL (`$BF21` = 4) |
| `L45` | `LIBAT` | `POS('.LIBRARY', TITLE)` |

### LIBRARY
| Old | New | Role |
|-----|-----|------|
| `G131` | `NOTICEIN` | the notice as typed |
| `LB6` | `BELLWAIT` | prompt with number, bell, wait for space |
| `LB15` | `IFWRERR` | interface write error prompt |
| `M3` | `OUTFULL` | set by LINKIT when the output is full |

### FILER
| Old | New | Role |
|-----|-----|------|
| `FL56` | `CHECKVER` | same 1.3 version check as the linker |
| `L29` | `SCRWIDTH` | screen width (40 if CRT width &lt; 80) |
| `L12` | `DIRSIGN` | 0 forward / 1 back when copying |
| `L14` | `VOLCONF` | volume-name confirmation in ZEROVOLUME |

Skipped: `M2`, `L85` (pure loop indices); no-ancestor leftovers none left in this batch.
