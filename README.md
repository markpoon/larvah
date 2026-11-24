# Larvah

*The old word for a mask, misspelled so it is only ours.*

Larvah keeps a written mask of how you want Claude to work with you. Say "don the mask" and Claude works under it; say "doff the mask" and it stops. There is one mask, it is either on or off, and you approve every change to it. Nothing leaves Claude: there are no servers, and nothing is sent anywhere.

The full design is in [Larvah plan.md](Larvah%20plan.md). 
## Say it out loud

| Say | Type | What happens |
| --- | --- | --- |
| "Don the mask" / "Don the mask for coding" | `/larvah:don` | Puts the core lines and the right scenes on |
| "Doff the mask" | `/larvah:doff` | Takes it off for the rest of the chat |
| "Check the mask" | `/larvah:check` | Up to ten lines: what is in force, the budget, sources used and skipped |
| "Scratch that from the mask" | `/larvah:scratch` | Removes a line, and anything built on it, and adds a limit so it isn't learned again |
| "Mend the mask" / "Add this to the mask: …" | `/larvah:mend` | Proposed changes, numbered, for you to sign. The only way anything is saved |
| "Remake the mask" | `/larvah:remake` | Rebuilds the mask from your whole history, after a backup |
| "Lend the mask" | `/larvah:lend` | Writes your mask out to share (letter, Doc or skill file) |
| "Try on this mask" | `/larvah:try` | Screens someone else's mask before you wear it |

Every phrase contains "mask", so an everyday "check" or "try" never fires by accident.

## What is in the box

| Part | Where | Job |
| --- | --- | --- |
| Skills | `skills/` | The eight commands above, plus an internal `store` skill that reads and writes the mask |
| Mender (agent) | `agents/mender.md` | Proposes changes to the mask; never writes to it |
| Maker (agent) | `agents/maker.md` | Drafts skills, agents or hooks for repeated duties; never installs |
| Dresser (hook) | `hooks/`, `scripts/dresser.sh` | Puts the mask on at session start in Cowork and Claude Code |
| Stagehand (hook) | `hooks/`, `scripts/stagehand.sh` | Repeats the core lines each message; off unless you switch it on |
| `larvahctl` | `scripts/larvahctl.py` | The exact work: worn lines, secret scan, refusals, budget, lending, screening |
| Prompter, Doorkeeper, Herald | inside `don`, `try`, `lend` | Picks scenes, screens other people's masks, writes yours out |

Only skills load in the phone app. Hooks and agents run in Cowork and Claude Code.

## Where the mask lives

- **The workshop copy** (Claude Code and any chat with file tools): `~/.claude/larvah/mask.json`. Set `LARVAH_HOME` to use another folder.
- **Claude's memory** (the phone app): topics named `Larvah: core lines`, `Larvah: scenes` and `Larvah: scene <name>`. Larvah never touches other memory topics.

The workshop copy is JSON, not YAML, so the tool needs nothing installed beyond Python 3.

## Rules it keeps

- **Nothing unsigned.** `larvahctl` writes only when given `--approved`, and the skills pass that only after you said yes to that exact change. Agents and scheduled runs never pass it.
- **Only stated or confirmed lines are worn.** Observed lines wait for you. Inferred lines are never worn.
- **Never recorded:** passwords, keys, card and ID numbers.
- **Never written:** a line that would make Claude stop flagging mistakes, risks or disagreements.
- **The house rules come first.** Claude's own rules and Anthropic's rules apply whatever the mask says, and a line is instructions, not permissions.
- **Budgets:** core lines 600 tokens, scenes 3,000 each (at most two at a time), a borrowed mask 400.

## Try it

Load the plugin from this folder:

```bash
git clone https://github.com/markpoon/larvah
claude --plugin-dir ./larvah
```

Then say "add this to the mask: do five rounds of review before answering", sign the change, and say "don the mask". Run the tests with:

```bash
cd larvah && python3 -m unittest discover -s tests
```

See [TESTING.md](TESTING.md) for what has been checked and the memory tests still to run.

## License

[MIT](LICENSE), © 2026 Mark Poon. Use it, change it, share it; keep the notice.

## Names

The plugin is called Larvah, a misspelling of the Latin word for a mask. The thing you put on and take off is still "the mask". A project called [TTigger/mask](https://github.com/TTigger/mask) exists (a persona-switching framework), which is why the plugin does not use the plain name.
