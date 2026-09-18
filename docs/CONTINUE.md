# Continue here

**Repo:** private `pascal-improvements` only (`origin`). Branch **`main`**.  
**Baseline tag:** `starting-point-for-changes`  
**Tip at last stop:** `2f21e90` (then this CONTINUE update)

## Done on this fork (high level)

- Compiler: `CASE ORD` INSYMBOL; COMPOPTI `OTHERWISE ERROR(301)` for unknown options
- Editor: tab-stop DIV math; `DIRTY`/`WORKNAME`/`HASNAME`/`REOPEN`/`CANDOWN`
- OS: `CANTSTRETCH` / `MAINLOOP`; GETCMD `GC*` → role names
- Filer/Linker/Library/LibMap: comment-backed renames; Filer `OTHERWISE` unknown command
- ASSMBLER: all 112 `G*` renamed
- Natives: TURTLEGR, LONGINTS, ASMFORMAT, BOOTII, BOOTPD — all `Lxxxx` cleared
- Docs: `RENAMES.md`, `PLACEHOLDERS.md`, `CLARITY-SCAN.md`, `CONTINUE.md`

## Parked

- **`128K.APPLE` / `src/native/interp/`** (~800 `L*`) — user will introduce **John Brooks** material later; do **not** rename this mine for now.

## What’s left (excluding parked interp)

- **Optional naming polish:** EDITOR locals `L1`…`L559`; leave `XXX`/`YYY` (UCSD unused)
- **Leave alone:** PASCALSYSTEM `L54`/`L396`/`L696` (FINIT address tricks); COMPINIT string `XXX`
- **Optional clarity/behavior:** more menu `OTHERWISE`; ASSMBLER hash idiom; richer comments
- **Not a rename backlog:** placeholder mines outside interp are effectively finished

## Remember

- Compiler rebuilds need `procbuild.USE_NS = True`
- Intentional binary divergences: probe gold is `acceptance/2026-09-16-*` / `2026-09-17-*`, not shipped Apple bytes
- Label renames across `.PROC`s must be **file-unique** (FILLIT data ≠ HIRES `STOREXY`)
