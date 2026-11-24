# App-side results

One row per run. Result is PASS, FAIL or SKIP. Put what was observed in Notes, especially for a FAIL.

| Date | ID | Venue and version | Result | Notes |
| --- | --- | --- | --- | --- |
| | M1 | | | |
| | M2 | | | |
| | M3 | | | |
| | M4 | | | |
| | P1 | | | |
| | P2 | | | |
| | P3 | | | |
| | P4 | | | |
| | C1 | | | |
| | C2 | | | |
| | C3 | | | |
| | K1 | | | |
| | A1 | | | |
| | A2 | | | |

## Reported, not yet itemised

| Date | Venue | Result | Source and caveat |
| --- | --- | --- | --- |
| 2026-11-24 | Another chat (app, not inspected) | Reported success | Reported by Mark. Test IDs and the chat's output were not provided, so no row above is marked PASS. Itemise by pasting the chat's replies or naming the IDs |

## Automated layers (for comparison, not app side)

| Date | Layer | Result | Notes |
| --- | --- | --- | --- |
| 2026-11-24 | Unit and end-to-end (`tests/`) | PASS, 52 of 52 | Local, Python 3.9.6. CI also green on Ubuntu 24.04 and macOS, Python 3.9 and 3.12 |
| 2026-11-24 | Headless Claude (`tests/headless/`) | PASS, 7 of 7 | Claude Code 2.1.311 on macOS, `claude -p` with the plugin loaded |
| 2026-11-24 | Plugin validation | PASS | `claude plugin validate .` |
