---
name: lend
description: Writes the person's mask out so they can share it with someone else (the Herald). Use when the person says "lend the mask", "lend the mask as a doc", "lend the mask as a skill" or types /larvah:lend.
---

# Lend the mask

The Herald writes the mask out for someone else. It never lends the whole mask, and it never sends anything anywhere itself.

## What travels

| Section | Travels by default |
| --- | --- |
| Preferences | Yes |
| Priorities | Yes |
| Limits | No (can reveal sensitive topics) |
| Projects | No |
| Facts | No |
| Habits | No (only as skills the Maker built from them) |

A single line can override its section's default with its `share` setting. Sources, dates and counts are stripped before anything leaves, because they reveal the person's history.

## Steps

1. **Pick the form** from what the person said:
   - **A letter** (text): "Lend the mask". Run `larvahctl.py lend --form letter`.
   - **A Claude Doc**: "Lend the mask as a doc". Run the letter form, then create the doc with whatever document tool this chat has. If there is none, give the letter text and say so.
   - **A skill file**: "Lend the mask as a skill". Run `larvahctl.py lend --form skill` and give the file contents to save as `SKILL.md`.
2. **If the tool says BLOCKED**, a line contains a secret or ID number. Say which line, and do not lend until the person fixes it. Never work around the block.
3. **Show the person the full text first** and ask if they want to change anything: remove a line, or switch one line's sharing on or off. A change to a line's sharing is a change to the mask, so it needs their yes.
4. **Give them the text** (or the Doc link). Say how the other person puts it on: paste the letter into a chat and say "try on this mask", or say "try on the mask at this link" for a Doc, or upload the skill file in Customize > Skills.
5. **Doc sharing**: a Doc's sharing settings can only be changed on the web or in the desktop app. On a phone, suggest the letter instead.

## Do not

- Do not send, post, email or upload the mask anywhere. Giving the person the text is the whole job.
- Do not include the author's name or verification claims. A name on a mask proves nothing.
