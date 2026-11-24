---
name: mend
description: Brings the proposed changes to the person's mask for approval, and saves a line the person wants to add. Use when the person says "mend the mask", "add this to the mask", "save this to the mask" or types /larvah:mend.
---

# Mend the mask

The only way anything enters the mask. The Mender proposes, the person signs, and only then is anything written.

## Two ways in

- **The person states a line** ("add this to the mask: do five rounds of review"). Treat it as one proposed line, kind `stated`. Go to step 3.
- **A full mending** ("mend the mask", `/larvah:mend`). Start at step 1.

## Steps

1. **Collect** only what is newer than the last mending, from the sources this venue allows and the person has switched on:
   - the current chat (preferences stated, corrections);
   - past-chat search, if available;
   - Claude's memory (facts already on file; one import at setup);
   - in Claude Code only: sessions, GitHub repos, and the queues of claude-reflect or claude-smart if installed.
   Where agents are available, the **Mender** agent can do the collecting and drafting; otherwise do it here. A scheduled run only writes `mending.md` into the mask folder and never saves.
2. **Propose** lines from the person's own words and repeated actions. Mark each `stated` or `observed`. Skip secrets, ID and account numbers, and any sensitive topic (health, money, identity, politics) the person has not allowed in Limits. A habit needs at least three sightings across at least two weeks before it is proposed.
3. **Check each line before showing it.** Run `larvahctl.py add` *without* `--approved`: it refuses secrets and any line that would make Claude stop flagging mistakes, risks or disagreements, and reports duplicates. Report refused lines with the reason. Never reword a refused line to get past the check.
4. **Merge** against the mask: drop duplicates; where the person has contradicted an older line, propose the new one as replacing the old (`--supersede <id>`), never as a deletion.
5. **Present** at most ten numbered changes in plain words, each with its section, kind and a short reason. Example:
   1. Preferences, stated: "Do three rounds of review before answering." Replaces "five rounds".
6. **Wait for the person's signature.** Something like "yes to 1 and 3". Silence, a thumbs-up on a different topic or "sounds good" about the idea is not a signature for a specific change; ask again.
7. **Write only what was signed**, through the `store` skill with `--approved`, one line per signed change. Mirror to Claude's memory topics if the mask lives there too, and read them back.
8. **Report** what was written, what was refused and what is still waiting.

## After a load

When `don` finds differences between Claude's memory and the mask, they arrive here as a list. Show them as numbered changes and wait for a signature. If there are none, say nothing.

## Rules

- **Nothing unsigned.** Never pass `--approved` without a yes to that exact change in this chat.
- One line per line. If a change needs a paragraph, suggest a skill instead.
- Observed lines stay out of use until the person confirms them. Inferred lines are never written to be worn.
- Never record: passwords, keys, ID and account numbers.
