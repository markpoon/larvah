---
name: scratch
description: Removes a line from the mask so it is not learned again. Use when the person says "scratch that from the mask" or types /larvah:scratch.
---

# Scratch that from the mask

Remove one line, and anything built on it, and make sure it is not learned again.

## Steps

1. **Find the line.** Use what the person pointed at: their words, or a line just discussed. If it is not clear which line they mean, list the likely lines with their ids and ask which. If more than one matches, never guess.
2. **Remove it** with `larvahctl.py remove "<id or text>"` through the `store` skill. Because the person gave this command themselves, it needs no extra yes.
   - Anything built on the line goes with it.
   - The tool adds a limit, "Do not record again: …", so the Mender does not propose it again. (Scratching a limit adds no new limit.)
3. **Mirror to memory** if the mask also lives in Claude's memory: remove the line from the matching topic and add the limit. Read the topic back to confirm.
4. **Say what happened in one or two lines**: what was removed, anything removed with it, and the limit that was added.
5. **If this chat has the mask on**, stop following the removed line from now on.

## Do not

- Do not remove more than the person asked for.
- Do not claim the line is gone from the chat. What was already said stays said.
- Do not edit the mask in any other way.
