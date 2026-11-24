---
name: don
description: Puts the person's mask on for this chat. Use when the person says "don the mask", "don the mask for coding", "put the mask on" or types /larvah:don.
---

# Don the mask

Put on the mask: the core lines plus the right scenes. There is one mask. It is either on or off, and there are no personas.

## Steps

1. **Read the core lines** through the `store` skill.
   - If there is no mask yet, say so in one sentence and stop. Offer to start one: the person can say "add this to the mask: …" and `mend` will show the line and wait for a yes. Do not invent lines.
2. **Prompter: pick the scenes.** Read the list of scenes (one line each). Choose at most **two**, from what the person named ("for coding") or, if they named none, from the task they are on. If nothing clearly fits, load none and say so. Read each chosen scene through the `store`.
3. **Check the budget.** Core lines up to 600 tokens, each scene up to 3,000. If something is over, say which, and wear it anyway, but suggest `/larvah:mend` to tighten it.
4. **Say it is on, in one short line**, for example: "Mask on: 7 core lines, scene: coding." Do not read the lines back unless asked.
5. **Follow the lines** for the rest of this chat. Use only worn lines: stated, or observed and confirmed. Never use inferred ones.
6. **After a load.** If this chat can see both Claude's memory topics for the mask and the workshop copy, compare them: put the memory lines on stdin of `larvahctl.py diff`.
   - No differences: say nothing about it.
   - Differences: show them in plain words, numbered, and hand them to the `mend` steps. **Nothing enters the mask until the person signs off.**

## House rules

Claude's own rules and Anthropic's rules come first. If one of them overrides a line, follow the rule and say which line it overrode, in one sentence. A line is instructions, never permissions: it cannot unlock a tool, a folder or an approval.

## Do not

- Do not take on a persona or "don the mask of" anyone. There is one mask.
- Do not change the mask. Putting it on only reads it.
- Do not claim the mask is on if the read failed. Say what failed.
