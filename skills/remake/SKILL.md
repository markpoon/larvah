---
name: remake
description: Rebuilds the person's mask from scratch from their whole history, as one set of changes for approval. Use when the person says "remake the mask" or types /larvah:remake.
---

# Remake the mask

A full rebuild. It runs the same steps as `mend`, but over the person's whole history and against an empty mask, and proposes a fresh mask as one set of changes.

## Steps

1. **Say what this does** in two lines: it reads everything the venue allows, proposes a fresh mask, and replaces the old one only after sign-off. The old mask is backed up first.
2. **Collect** from every allowed source, with no "newer than" cutoff: the current chat, past-chat search, Claude's memory, and in Claude Code the sessions, repos and plugin queues the person has switched on.
3. **Propose** a fresh set of lines, following steps 2 to 5 of the `mend` skill: stated or observed only, no secrets or ID numbers, no sensitive topics the person has not allowed, nothing that makes Claude stop flagging mistakes or risks. Run each line through `larvahctl.py add` without `--approved` first.
4. **Compare with the old mask** and say what is new, what is gone and what is unchanged, so the person can see what a remake costs them.
5. **Present** the set in numbered groups of ten, and **wait for a signature** per group ("yes to all of the first ten", "yes to 11 and 14").
6. **Apply** only after sign-off:
   1. `larvahctl.py backup`, then show the backup path;
   2. `larvahctl.py reset --approved` (this keeps settings and scenes);
   3. add the signed lines with `larvahctl.py bulk --approved`, JSON on stdin.
7. **Mirror to memory** if the mask also lives there, then read it back.
8. **Report** what was written and where the backup is.

## Rules

- No backup, no reset. If the backup fails, stop and say so.
- Nothing unsigned goes in. A remake that nobody signed changes nothing.
- Do not delete the backup.
