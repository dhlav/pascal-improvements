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

FILER + LINKER comment-backed globals done. Next: GETCMD `GC*` from FINDINGS 225–227.

### Tier B — FINDINGS map exists; need careful GETCMD.* → English names

`PASCALSYSTEM.text` still uses `GC05`…`GC24` inside `GETCMD` even where
FINDINGS already equate them to `GETCMD.N` (esp. **225–227**):

| ID | FINDINGS / comment lead | Notes |
|----|-------------------------|--------|
| `GC05` | GETCMD.5 — segment-number / `SEGINFO` reader | Function; exact in binary |
| `GC07`–`GC18` | GETCMD.11 nested family (lib list / associate path) | Nested; renumber risk if moved |
| `GC21` | (in GETCMD body region) | Confirm before rename |
| `GC22`, `GC24` | compile/link finish helpers near `RUNWORKFILE` | Often already described in prose |

**Do not invent** names here: promote only when FINDINGS gives a stable
English name (e.g. `SYSASSOC` already replaced `GETCMD.3`). Prefer a
dedicated pass: one helper → one commit → optional OS recompile if you
want acceptance source synced (offsets unchanged ⇒ bytes should match).

Also leftover locals: `L54`, `L396`, `L696` in PASCALSYSTEM — treat as
Tier C unless comments pin them.

### Tier C — listed as “no ancestor” (memory / finding 291–294 leftovers)

| File | IDs | Status |
|------|-----|--------|
| `LINKER.text` | `LK2`, `LK3`, `LK17`, `LK51`, `L45` | Apple additions; keep until body match (`G29`/`G91`/`L12` renamed) |
| `LIBRARY.text` | `G131`, `LB6`, `LB15` (+ older note `M2`/`M3` if still present) | same |
| `LIBMAP.text` | `L85` | same |
| `FILER.text` | `FL56`, `L12`, `L14`, `L29` | Apple / local; `FL56` is a procedure |

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
5. **LINKER/LIBRARY/LIBMAP** leftovers only if an ancestor body turns up.
6. **ASSMBLER / natives** as dedicated naming campaigns, not drive-by renames.

## Counts snapshot (unique IDs, 2026-09-16)

| File | Placeholders (unique) |
|------|------------------------|
| ASSMBLER | ~112 `G*` |
| PASCALSYSTEM | 16 `GC*` + 3 `L*` |
| EDITOR | 17 `L*` + `XXX`/`YYY` |
| LINKER | 2 `G*` + 4 `LK*` + 2 `L*` |
| FILER | 2 `G*` + 1 `FL*` + 3 `L*` |
| LIBRARY | 1 `G*` + 2 `LB*` |
| LIBMAP | 1 `L*` |
| TURTLEGR native | ~54 `L*` |
| LONGINTS native | ~49 `L*` |
