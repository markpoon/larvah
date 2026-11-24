---
name: store
description: Internal helper for the Larvah plugin. Reads and writes the person's mask. Use only when another Larvah skill says to use the store, never on its own.
---

# The store

This is how every Larvah skill reads and writes the mask. The other skills say *what* to do; this one says *where it lives* and *how to touch it*.

## Where the mask lives

| Place | Used when | What it holds |
| --- | --- | --- |
| **The workshop copy**: `mask.json` in `$LARVAH_HOME` (default `~/.claude/larvah/`) | Claude Code, or any chat that has Bash and file tools | The whole mask: lines, scenes, settings |
| **Claude's memory**: topics named `Larvah: core lines`, `Larvah: scenes` and `Larvah: scene <name>` | The phone app and any chat without file tools; mirrored from the workshop copy when both exist | The same lines, as plain text, one line per line |

Memory is the home on the stage. The file is the home in the workshop. When both are available, keep them the same, and write the file first.

Never touch other memory topics. Only the three topic names above belong to Larvah.

## Using the workshop copy

The tool is `scripts/larvahctl.py` in this plugin's folder. This skill sits in `skills/store`, so from this skill's base directory the tool is at `../../scripts/larvahctl.py`. Run it with `python3`.

| Job | Command |
| --- | --- |
| Create the file if missing | `larvahctl.py init` |
| Worn core lines | `larvahctl.py core` |
| List scenes | `larvahctl.py scenes` |
| Worn lines of one scene | `larvahctl.py scene <name>` |
| What is in force and the budget | `larvahctl.py check` |
| Compare lines read from memory with the mask (lines on stdin) | `larvahctl.py diff` |
| Propose one line (writes nothing) | `larvahctl.py add --section S --text "..." --kind stated --scene always` |
| Write one line after the person said yes | the same, plus `--approved` |
| Replace an older line | add `--supersede <id>` |
| Scratch a line | `larvahctl.py remove "<id or text>"` |
| Scan text for secrets | `larvahctl.py scan --text "..."` |
| Add or change a scene | `larvahctl.py scene-set <name> "<description>" --approved` |
| Back up, then empty the mask | `larvahctl.py reset --approved` |
| Add many lines from JSON on stdin | `larvahctl.py bulk --approved` |
| Write the mask out to share | `larvahctl.py lend --form letter` or `--form skill` |
| Screen a lent mask (text on stdin) | `larvahctl.py screen` |

Sections are `preferences`, `limits`, `projects`, `facts`, `habits` and `priorities`. Kinds are `stated`, `observed` and `inferred`.

## Rules that never bend

1. **No `--approved` without a yes.** Pass `--approved` only after the person has said yes to that exact change in this chat. A scheduled run or an agent never passes it.
2. **Never record secrets.** The tool refuses passwords, keys, card and ID numbers and says why. Do not work around a refusal; tell the person.
3. **Never write a line that makes Claude stop flagging mistakes, risks or disagreements.** The tool refuses these too.
4. **One line per line.** A line that needs a paragraph is really a skill; suggest one.
5. **Only worn lines are used.** Stated lines, and observed lines the person has confirmed. Inferred lines are never worn.
6. **If a command fails or no tool is available**, say so plainly and fall back to memory. Never pretend a write happened.

## Without file tools (the phone app)

Read the three memory topics directly. To save, show the exact text and wait for a yes, then ask the memory feature to remember it under the right topic name, word for word. Memory can filter what it stores, so after saving, read the topic back and tell the person if anything was dropped.
