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
- Docs: `RENAMES.md`, `PLACEHOLDERS.md`, `CONTINUE.md`

## Next

See **`docs/PLACEHOLDERS.md`**: LINKER/LIBRARY/LIBMAP leftover `LK*`/`LB*`
(only with ancestor evidence), or start the ASSMBLER `G*` naming mine.

## Remember

- Compiler rebuilds need `procbuild.USE_NS = True`
- Intentional binary divergences: probe gold is the new `acceptance/2026-09-16-*` epochs, not shipped Apple bytes
