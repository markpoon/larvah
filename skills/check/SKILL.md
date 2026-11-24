---
name: check
description: Shows what the mask is doing right now. Use when the person says "check the mask" or types /larvah:check.
---

# Check the mask

Report, in **at most ten lines**, what is in force and where it came from.

## What to report

1. **Is the mask on in this chat?** If it was put on, say how: the person said "don the mask", or the Dresser put it on at the start.
2. **Which core lines and scenes are loaded**, and how many lines each. Get the numbers from `larvahctl.py check` through the `store` skill, or from memory if there are no file tools.
3. **The budget**: loaded size against the 600-token core and 3,000-token scene limits. Say plainly if something is over.
4. **Which sources were used and which were skipped**, for example "workshop file: read; Claude's memory: not available in this chat".
5. **Lines waiting**: observed lines that need the person's confirmation, and lines that are never worn (inferred).
6. **Overrides**: if Claude's own rules or Anthropic's rules overrode a line in this chat, name the line and say so.
7. **Anything unavailable**: if the organisation switched off memory, skills or plugins, or the tool could not run, say plainly which piece is missing.

## Rules

- Keep it to ten lines or fewer. Plain words, no tables.
- Change nothing. Checking is read-only.
- If you could not check something, say that. Do not guess a number.
