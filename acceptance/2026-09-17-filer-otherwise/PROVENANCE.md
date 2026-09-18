# 2026-09-17 — FILER OTHERWISE for unknown commands

## Change
`CALLPROC` command `CASE CH OF` gains:
- `' ': ;` — space is in the prompt accept-set but is not a command
- `OTHERWISE` — bell + `Unknown command` (defense if accept-set / CASE drift)

## Build
`emuremote --vol WORKHD compile FILER13` then librarian `--slots 1` →
`LIBFILER.CODE` (15360 bytes; 817 bytes differ from prior byte-identical
reconstruction).
