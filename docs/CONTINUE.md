# Continue here

**Repo:** private `pascal-improvements` only (`origin`). Branch **`main`**.  
**Last tip when stopping:** `7b58efd` (FILER `DESTBLKS`/`SRCBLKS`).  
**Baseline tag:** `starting-point-for-changes`

## Done this session (high level)

- Compiler: `CASE ORD` INSYMBOL; COMPOPTI `OTHERWISE ERROR(301)` for unknown options
- Editor: tab-stop DIV math; `DIRTY`/`WORKNAME`/`HASNAME`/`REOPEN`/`CANDOWN`
- OS: `CANTSTRETCH` / `MAINLOOP`
- Filer: `DESTBLKS` / `SRCBLKS`
- Docs: `RENAMES.md`, `PLACEHOLDERS.md`

## Next

See **`docs/PLACEHOLDERS.md`** Tier A remainder:

1. LINKER `G91` / `L12` (comment-backed), or
2. GETCMD `GC*` renames from FINDINGS 225–227

## Remember

- Compiler rebuilds need `procbuild.USE_NS = True`
- Intentional binary divergences: probe gold is the new `acceptance/2026-09-16-*` epochs, not shipped Apple bytes
