# Clarity scan (2026-09-17)

Examine-only pass after ASSMBLER `G*` naming finished.

## Findings

| Check | Result |
|-------|--------|
| Control characters inside `'…'` literals | **None** left under `src/pascal/` |
| `ODD(…248)` tab idiom | Only **comments** in EDITOR (code already DIV form) |
| ASSMBLER `ODD(HASHTOP)` / hash LAND | Intentional bit idiom — leave alone |
| OS `CASE CH` in GETCMD | Guarded by `BADCMD` set — OTHERWISE unreachable |
| SETUP menus | Unknown keys re-prompt; `Q` exits via `UNTIL` |
| FILER `CASE CH` | Prompt set admits space with no CASE arm; other letters matched. **Hardened** with explicit `' '` no-op + `OTHERWISE` bell/message (defense if set/CASE drift). |

## Code change

`FILER.text` CALLPROC command CASE: `' '` empty arm; `OTHERWISE` writes bell + `Unknown command`.
