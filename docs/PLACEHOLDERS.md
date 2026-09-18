# Remaining placeholders (improvements fork inventory)

Date: 2026-09-16. Rule (unchanged): rename only with **body-for-body
ancestor evidence**, or — for Apple-only slots — with a role already
pinned in FINDINGS / source comments (as with EDITOR `G590`→`DIRTY`).
Invented descriptive names without that bar are out of scope.

Already done on this fork: see `docs/RENAMES.md`.

---

## Ranked next work

### Tier A — comment-backed, small (ready to rename like EDITOR G*)

| File | ID | Comment / role | Suggested name |
|------|-----|----------------|----------------|
| `FILER.text` | ~~`G361`~~ | ~~blocks on destination~~ | **done → `DESTBLKS`** |
| `FILER.text` | ~~`G362`~~ | ~~blocks on source~~ | **done → `SRCBLKS`** |
| `LINKER.text` | ~~`G91`~~ | ~~heap pointers count words~~ | **done → `WORDHEAP`** |
| `LINKER.text` | ~~`L12`~~ | ~~linking an intrinsic unit~~ | **done → `INTRLINK`** |
| `LINKER.text` | ~~`G29`~~ | ~~host segment's slot~~ | **done → `HOSTSLOT`** |

FILER + LINKER comment-backed globals done. GETCMD `GC*` renamed 2026-09-17.

### Tier B — GETCMD GC* (done)

All `GC05`…`GC24` → role-based English names (STRONG INFERENCE from
FINDINGS 225–228). Full table in `docs/RENAMES.md`. Leftover locals
`L54`, `L396`, `L696` in PASCALSYSTEM — tier C unless comments pin them.

### Tier C — listed as “no ancestor” (memory / finding 291–294 leftovers)

| File | IDs | Status |
|------|-----|--------|
| `LINKER.text` | — | LK*/L45 renamed 2026-09-17 |
| `LIBRARY.text` | `M2` | loop index only; `G131`/`LB*`/`M3` renamed |
| `LIBMAP.text` | `L85` | loop index for upshift |
| `FILER.text` | — | FL56/L12/L14/L29 renamed 2026-09-17 |

### Tier D — large ancestor mines (separate projects)

| Area | Scale | Ancestor |
|------|-------|----------|
| `ASSMBLER.text` | **~112 unique `G*`** (many uses) | UCSD I.5 assembler (not II.0 in-tree) |
| `TURTLEGR.TEXT` | ~54 `Lnnnn` labels | UCSD turtle_graphics mirror (unmined) |
| `LONGINTS.TEXT` | ~49 `Lnnnn` | pascalio / longint native |
| `ASMFORMAT` / `BOOTII` / `BOOTPD` | dozens of `L*` | native / boot |
| `128K.APPLE` interp | ~800 `L*` | John Brooks 1.4 (external) |

### Tier E — leave alone

| ID | Why |
|----|-----|
| `EDITOR` `XXX`,`YYY` | UCSD unused params; documented in source |
| `EDITOR` `L10`…`L559` | mostly locals / labels; low value unless a whole-procedure rename |

---

## Suggested order on this fork

1. ~~**FILER `G361`/`G362`**~~ done (`DESTBLKS`/`SRCBLKS`).
2. ~~**LINKER `G91`/`L12`**~~ done (`WORDHEAP`/`INTRLINK`).
3. ~~**LINKER `G29`→`HOSTSLOT`**~~ done.
4. ~~**GETCMD `GC*`**~~ done (role-based names; see RENAMES.md).
5. ~~**LINKER/LIBRARY/FILER leftovers**~~ done (comment-backed batch).
6. **ASSMBLER / natives** as dedicated naming campaigns, not drive-by renames.
7. Optional: LIBMAP `L85` / LIBRARY `M2` (loop indices — low value).

## Counts snapshot (unique IDs, 2026-09-16)

| File | Placeholders (unique) |
|------|------------------------|
| ASSMBLER | ~112 `G*` |
| PASCALSYSTEM | 3 `L*` (GC* renamed) |
| EDITOR | 17 `L*` + `XXX`/`YYY` |
| LINKER | 4 `LK*` + 1 `L*` (G*/L12 renamed) |
| FILER | 1 `FL*` + 3 `L*` (G361/G362 renamed) |
| LIBRARY | 1 `G*` + 2 `LB*` |
| LIBMAP | 1 `L*` |
| TURTLEGR native | ~54 `L*` |
| LONGINTS native | ~49 `L*` |
