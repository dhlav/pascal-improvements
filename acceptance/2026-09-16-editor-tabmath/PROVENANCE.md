# 2026-09-16 — EDITOR tab-stop math (DIV form)

## Change
In `src/pascal/programs/1.3/EDITOR.text`, `SPACEOVER` and `TABBY` no longer
use UCSD's `ORD(ODD(X) AND ODD(248))` bit idiom. Equivalent clear forms:

- forward: `((X DIV 8)+1)*8-X`  (distance to next 8-column stop)
- back: `X-((X-1) DIV 8)*8`     (distance to previous stop; 8 if on one)

## Build
1. `emuremote --vol WORKHD compile EDIT13` (staged EDITOR.text)
2. Librarian remap `1:1,7:2,8:3,9:4,10:5,11:6,12:7` → `EDLIB.CODE`

## Result
`EDLIB.CODE` is 25600 bytes; **31 bytes** differ from the prior
byte-identical reconstruction / shipped `SYSTEM.EDITOR`. Probe gold is
this acceptance epoch, not Apple's disk image.
