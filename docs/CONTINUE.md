# Continue here

**Repo:** private `pascal-improvements` only (`origin`). Branch **`main`**.  
**Baseline tag:** `starting-point-for-changes`

## Done on this fork (high level)

- Compiler: `CASE ORD` INSYMBOL; COMPOPTI `OTHERWISE ERROR(301)` for unknown options
- Editor: tab-stop DIV math; `DIRTY`/`WORKNAME`/`HASNAME`/`REOPEN`/`CANDOWN`
- OS: `CANTSTRETCH` / `MAINLOOP`
- Filer: `DESTBLKS` / `SRCBLKS`
- Linker: `WORDHEAP` / `INTRLINK` / `HOSTSLOT`
- GETCMD: all `GC*` → role names (`SEGOFENT`, `USELIB`, `AFTERCMP`, …)
- LINKER/LIBRARY/FILER: `CLOSEINS`/`QUITLINK`/`STRIPDLE`/`CHECKVER`/…
- ASSMBLER: **all 112 `G*` renamed** (no `G*` left in ASSMBLER.text)
- Clarity scan: `docs/CLARITY-SCAN.md`; FILER `OTHERWISE` unknown command
- TURTLEGR: **all `Lxxxx` renamed** to unique role names
- LONGINTS: **all 109 `Lxxxx` renamed** (`POP2LI`, `ZRESULT`, …)
- LIBMAP `MAPIX`, LIBRARY `SEGIX`
- ASMFORMAT/BOOTII/BOOTPD: absolute `Lxxxx` → `F*`/`B*`/`P*`
- Docs: `RENAMES.md`, `PLACEHOLDERS.md`, `CONTINUE.md`, `CLARITY-SCAN.md`

## Next

**`128K.APPLE` interpreter** ~800 `L*` labels (John Brooks 1.4 candidate),
or more clarity / behavior improvements.

## Remember

- Compiler rebuilds need `procbuild.USE_NS = True`
- Intentional binary divergences: probe gold is the new `acceptance/2026-09-16-*` epochs, not shipped Apple bytes
