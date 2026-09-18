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

## 2026-09-17 — ASSMBLER first G* batch (24 ids)

I.5 correspondences recorded in FINDINGS **263c** (adopted on this fork)
plus roles pinned in ASSMBLER source comments. Source-only;
`probe_assembler_whole` still green. **~88 unique `G*` remain.**

| Old | New | Basis |
|-----|-----|-------|
| `G11` | `ASMCH` | I.5 `CH` (CH taken); scanner current char |
| `G62` | `ADVANCE` | I.5 `ADVANCE` |
| `G6` | `SPCLSTIX` | I.5 `SPCIALSTKINDEX` |
| `G685` | `SPECSTK` | I.5 `SPECIALSTK` |
| `G622` | `RELOCATE` | I.5 `RELOCATE` |
| `G72` | `SRCBUF` | I.5 `BUFFER` (BUFFER collides) |
| `G71` | `MACBUFP` | macro text buffer pointer (`MACP`) |
| `G406` | `STRCONST` | string constant being built (`PSTRING`) |
| `G29` | `NUMVAL` | numeric constant (`PCONST`) |
| `G13` | `CURFIVE` | current `FIVEREC` / reloc record |
| `G70` | `DEFGATE` | gates `.DEF`/`.REF` helper |
| `G14` | `EXPRVAL` | expression value |
| `G15` | `EXPRCLS` | expression class |
| `G60` | `NAMEDSRC` | source is operator-named file |
| `G64` | `DOSYMDMP` | enable `SYMTBLDUMP` |
| `G27` | `MACLEVEL` | macro nesting level |
| `G661` | `MACBUFS` | array of macro buffers |
| `G659` | `CHSOURCE` | which source feeds `ASMCH` (0/1/2) |
| `G65` | `FOLDCAS` | fold case / collapse blanks |
| `G58` | `INMACDEF` | suppress fold while defining a macro |
| `G67` | `DLEZERO` | DLE blank-count was zero |
| `G539` | `LINEBUF` | listing line buffer |
| `G42` | `LOCLBASE` | local-label block base |
| `G44` | `LOCLTOP` | local-label block top |

## 2026-09-17 — ASSMBLER second G* batch (20 ids)

FINDINGS **262** / **263c** and ASSMBLER comments. **~68 unique `G*` remain.**

| Old | New | Basis |
|-----|-----|-------|
| `G3` | `CURSYM` | current `ASMREC` while walking symbol chains |
| `G7` | `MACBPOS` | index into macro body (CHSOURCE 0) |
| `G8` | `LINEPOS` | column in `LINEBUF` |
| `G10` | `CURROP` | current opcode (`OPREC`) |
| `G22` | `LOCCTR` | location counter |
| `G28` | `MACPPOS` | index into macro actual-parameter text |
| `G37` | `ERRCOL` | saved column for `USERINFO.ERRSYM` |
| `G38` | `SAVBLK` | saved block for work-file error path |
| `G39` | `FILEBLK` | `BLOCKREAD` block counter |
| `G41` | `SRCPOS` | index into source window (`CHSOURCE` 2) |
| `G43` | `LOCLCUR` | local-label frontier (with `LOCLBASE`/`LOCLTOP`) |
| `G52` | `EMITMODE` | mode written into `CURFIVE` |
| `G59` | `EXPRADV` | I.5 `EXPRSSADVANCE` |
| `G68` | `NOPRINT` | with print-suppression `LAND` vs `G12` |
| `G673` | `LOCLLVLS` | per-level local-label bases |
| `G1094` | `DEFSYM` | symbol being `.DEF`/`.REF`'d |
| `G1443` | `KEYTAB` | keyword name table |
| `G1608` | `SRCWIN` | source window buffer |
| `G2136` | `EMITBUF` | code emit buffer |
| `G2147` | `PATCHBUF` | patch / alternate code buffer |
