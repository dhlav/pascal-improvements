# 2026-09-16 — COMPOPTI OTHERWISE for unknown options

## Change
`src/pascal/1.3/phases/COMPOPTI.text`: the `CASE CH OF` option dispatch
ends with `OTHERWISE ERROR(301)` so an unknown `(*$…*)` letter is reported
(SYNTAX: "No case provided for this value") instead of silently ignored.

Also carries the earlier INSYMBOL `CASE ORD(...)` clarity change in
`PASCALCO.text`.

## Build
Splice with `procbuild.USE_NS = True`, then emuremote compile / link SEARCH /
librarian slots 1–15 on WORKHD.

## Verification
- `(*$Z+*)` → compile fails with **line 1, error 301**
- `(*$R-*)` → compiles clean
- `LIBCOMP.CODE` is 39936 bytes; **51 bytes** differ from the
  byte-identical reconstruction / shipped `SYSTEM.COMPILER`
