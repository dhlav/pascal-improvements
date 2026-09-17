# 2026-09-16 — INSYMBOL `CASE ORD` rebuild

## Change
`src/pascal/1.3/PASCALCO.text` `INSYMBOL` uses `CASE ORD(SYMBUFP^[SYMCURSOR])`
with ASCII numeric labels (TAB=9, space=32, …) instead of a literal TAB
character in quotes. Nested `<>`/`=` peek CASE also uses `ORD`.

## Build
1. Splice with `procbuild.USE_NS = True` so `(*$NS 7*)` precedes COMPINIT
   (without this, phases number 2..15 and the compiler dies at run time with
   "Unknown run-time error").
2. `emuremote --vol WORKHD compile BODY13` (shipped SYSTEM.COMPILER).
3. Link `BODY13` + kept `SEARCH.CODE` → `COMPLINK`.
4. Librarian slots 1–15 → `LIBCOMP`, Apple copyright notice.

## Result
`LIBCOMP.CODE` is **byte-identical** to
`acceptance/2026-09-12-compiler-librarian/LIBCOMP.CODE` and to shipped
`SYSTEM.COMPILER` (39936 bytes). The ORD form is a source clarity change
only; Apple's CASE-of-CHAR already jumps on ordinals.

## Smoke test
Installed this `LIBCOMP` as `SYSTEM.COMPILER` on SYSHD; compiled
`SCANTEST.TEXT` (contains a literal TAB before `I := 1`, plus `<>` `<=`
`>=` `>`). Compiled clean, 8 lines.
