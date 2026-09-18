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
- Docs: `RENAMES.md`, `PLACEHOLDERS.md`, `CONTINUE.md`

## Next

**Natives** (TURTLEGR/LONGINTS `L*` labels), or a **clarity scan**
(TAB/ODD/silent CASE), or low-value loop indices (`L85`/`M2`).

## Remember

- Compiler rebuilds need `procbuild.USE_NS = True`
- Intentional binary divergences: probe gold is the new `acceptance/2026-09-16-*` epochs, not shipped Apple bytes
