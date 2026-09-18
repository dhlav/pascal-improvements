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

## 2026-09-17 — ASSMBLER third G* batch (16 ids)

Tables, files, and clear control flags. **~52 unique `G*` remain.**

| Old | New | Basis |
|-----|-----|-------|
| `G966` | `SYMTAB` | primary hash buckets of `ASMRECP` |
| `G838` | `SYMSAVE` | swap copy of `SYMTAB` |
| `G691` | `LOCLTAB` | local-label `LOCREC` table |
| `G73` | `LISTFILE` | listing `INTERACTIVE` file |
| `G1095` | `SRCFILE` | source text file |
| `G1135` | `LIFILE` | `%LINKER.INFO` `FILE OF REC8` |
| `G590` | `INFONAME` | linker-info pathname |
| `G447` | `LISTTTL` | listing page title |
| `G488` | `LINECOPY` | blank template copied into `LINEBUF` |
| `G2120` | `HEXDIGS` | `'0123456789ABCDEF'` |
| `G1575` | `KEYCODES` | keyword → token-code table |
| `G69` | `NAMEHIT` | symbol-name search found |
| `G36` | `ERRCNT` | error count |
| `G12` | `HASLIST` | `LISTNAME <> ''` / listing enabled |
| `G657` | `FREEFIVE` | free list of `FIVEP` reloc nodes |
| `G628` | `NEWREF` | newly allocated `REFP` on reloc chain |

## 2026-09-17 — ASSMBLER fourth batch (47 ids) + final gaps (4)

Clears **all** remaining `G*` in `ASSMBLER.text` (112 → 0).

### Counters / positions / flags (selected)
| Old | New | Role |
|-----|-----|------|
| `G5` | `CODEIX` | emit index into code buffer |
| `G9` | `CODEBLK` | codefile block number for `BLOCKWRITE` |
| `G16` | `WINEND` | end of live `SRCWIN` data |
| `G17` | `MACFREE` | free `MACBUFS` slot index |
| `G18` | `MINMEM` | reported minimum heap words |
| `G19` | `SAVLC` | saved location counter |
| `G20` | `CODEORG` | code origin passed to emit helper |
| `G21` | `SYMSIZE` | accumulated into `CURSYM^.A6` |
| `G23` | `PROCIDX` | procedure index counter |
| `G24`/`G25` | `LIEND`/`LIPOS` | linker-info file extent / position |
| `G26` | `SAVMACL` | saved `MACLEVEL` |
| `G31` | `FLAGCNT` | “errors flagged” count on listing |
| `G32` | `LISTLINE` | listing line counter |
| `G33` | `LINECNT` | source lines assembled |
| `G34` | `PAGENUM` | listing page number |
| `G35` | `TOTCODE` | total code size accumulator |
| `G40` | `READBLKS` | blocks returned by `BLOCKREAD` |
| `G45`–`G48` | `RELCNT4`–`RELCNT1` | reloc counts paired with `RELTAB*` |
| `G49` | `SEGBASE` | segment base (`EMITMODE` delta) |
| `G50` | `MAXCBLK` | high-water code block |
| `G51` | `MAXEMIT` | high-water `EMITMODE` |
| `G53`/`G54` | `PAGEOFF`/`PAGEBASE` | within-page offset / page base |
| `G55` | `MACFLAG` | first byte of macro buffer / mode |
| `G56` | `LISTON` | listing detail toggle |
| `G57` | `BIGEND` | endian probe (`BYTES[1]=CHR(1)`) |
| `G63` | `ABSSTART` | absolute-start / first-segment gate |
| `G66` | `HDRDONE` | listing header already emitted |
| `G658` | `DEFCLASS` | default symbol class |
| `G660` | `EXTMODE` | `.DEF`/`.REF` external mode |

### Tables / strings / heap
| Old | New | Role |
|-----|-----|------|
| `G629`–`G650` | `RELTAB4`–`RELTAB1` | `SEVEN` reloc tables |
| `G667`/`G679` | `MACBSAVE`/`MACPSAVE` | per-level macro positions |
| `G374`/`G390` | `INCTITLE`/`CURFILE` | include / current file titles |
| `G598` | `SIXSTATE` | `SIXREC` reloc/state block |
| `G2158` | `HEAPMARK` | `MARK`/`RELEASE` pointer |
| `G2159` | `SEGNAME` | 8-char name on listing banner |
| `G2163` | `ERRNAME` | first erroring symbol name |
| `G2167` | `ERRSIZES` | per-error size vector |

### Frame gaps (unused declarations kept for layout)
| Old | New |
|-----|-----|
| `G30` | `GAP30` |
| `G61` | `UNUSED61` |
| `G604` | `GAP604` |
| `G2128` | `GAP2128` |

Stale comment `LOCLTAB[G624]` → `LOCLTAB[LOCLCUR]`.

## 2026-09-17 — TURTLEGR HIRES L* → role names

UCSD `host/klebsch/turtle_graphics/main.asm.text` is stubs only (no local
labels). Renames are **STRONG INFERENCE** from branch structure in the
reconstructed Apple source. **40 labels** in `.PROC HIRES` renamed;
~81 `Lxxxx` remain in CLIP/MOVEABS/MOVEREL/FILLIT/SCREENBIT/DRAWBLOCK.

| Old | New | Role |
|-----|-----|------|
| `L000C`/`L000E` | `PAGE2`/`STOREP` | SETPAGE page-2 / store PAGE |
| `L0030`…`L004A` | `PENLT5`…`PENNONE` | SETPEN colour arms / none |
| `L0054` | `STOREXY` | save A,X,Y before HPOSN |
| `L0084`/`L0085` | `BITCNT`/`BITMOD` | bit-position loop |
| `L00A0`…`L00EB` | `PLOTLP`…`ADJRTS` | PLOT/RIGHT pixel path |
| `L00FE`…`L0157` | `LINEDN`…`RORSC2` | LINE row stepping |
| `L0182` | `BITTAB` | bit-mask table |
| `L0282`/`L0283` | `ROWMSK0`/`ROWMSK1` | row-step BIT masks |

## 2026-09-17 — TURTLEGR: remaining procs (all Lxxxx cleared)

Per-procedure offsets reused the same `Lxxxx` spellings across `.PROC`s, so
names must be **file-unique**. FILLIT’s trailing data bytes were briefly
aliased to HIRES `STOREXY` and are now `FILLCNT`/`FILLY`.

| Area | Examples |
|------|----------|
| HIRES LINE remainder | `LNST09`…`LINERTS`, `BITTAB` already done |
| CLIP / CLIPXY | `CLIPOK`, `CPYVP`, `CLPLOOP`, `OUTCODE`, `MOV5`, Cohen–Sutherland outcode arms |
| MOVEABS / MOVEREL | `MA_COPY`, `MA_PUT`, `MA_DRAW`, `MR_COPY` |
| FILLIT | `FI_VP`, `VPADJ`, `FILLP`, `FILLCNT`, `FILLY` |
| SCREENBIT | `SB_ON` |
| DRAWBLOCK | `DB_VP`, `DB_RTS`, `DB_WIDE`, `DB_J1`/`DB_J2`, `DB_MOD1`/`DB_MOD2`, … |

**No `Lxxxx` labels remain** in `TURTLEGR.TEXT`.

## 2026-09-17 — LONGINTS DECOPS: all 109 Lxxxx renamed

Klebsch `long_integer/main.asm.text` is a stub. Internal branches renamed
to unique ≤8-char names by section (RETURN/DECLEN/errors/POP2LI setup,
DAJ, DECCMP shared add/sub helpers, DAD/DSB/DMP/DDV/DCV/DCVT/DTNC/DSTR).

Examples: `RETJMP`, `ERR13`/`ERR6`, `POP2LI`, `AJTRIM`, `CMPVEC`,
`ZRESULT`, `TAKEB`, `POW2`, `DDVGO`, `TNCOVF`, `STRTYA`.

**No `Lxxxx` labels remain** in `LONGINTS.TEXT`.

## 2026-09-17 — LIBMAP / LIBRARY loop indices

| File | Old | New | Role |
|------|-----|-----|------|
| `LIBMAP.text` | `L85` | `MAPIX` | upshift index over `maptitle` |
| `LIBRARY.text` | `M2` | `SEGIX` | `FOR` segment index in link loops |

## 2026-09-17 — ASMFORMAT / BOOTII / BOOTPD absolute labels

These files use **absolute** `L<addr>` labels (not proc-relative). Renamed:

| File | Scheme | Examples |
|------|--------|----------|
| `ASMFORMAT.TEXT` | role EQUs + `F<addr>` | `DELAY`, `FORMGO`, `ERR2B`, `F3D50`, … (102) |
| `BOOTII.TEXT` | `B<addr>` | `B0800`, … (70) |
| `BOOTPD.TEXT` | `P<addr>` | `P0800`, … (23) |

**No `Lxxxx` labels remain** under `src/native/`.
