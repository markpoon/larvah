# Larvah

Larvah is a plugin that carries a written mask between Claude and the person it works with. The mask is a short, approved record of the terms of the interface: preferences, limits, projects, facts, habits and priorities. Larvah is the conduit. It proposes terms, the person accepts or rejects each one, and the accepted terms are worn by Claude until the mask is taken off.

The mask has two states, on and off. Every change to it needs the person's explicit approval, and nothing leaves Claude: there are no servers, and nothing is sent anywhere.

*Larvah* is a respelling of the Latin *larva*, a mask.

## How the interface is negotiated

1. **Propose.** Larvah (or the person) puts forward a line, marked as stated, observed or inferred.
2. **Approve.** The line is shown as written. Nothing is saved without a yes to that exact line.
3. **Wear.** Stated lines, and observed lines the person has confirmed, are applied by Claude. Inferred lines are never applied.
4. **Revise.** Lines can be scratched, replaced or rebuilt. A scratched line adds a limit so it is not proposed again.

## Commands

Each command is a spoken phrase and a slash command. Every phrase contains "mask", so an ordinary "check" or "try" does not trigger anything.

| Say | Type | Effect |
| --- | --- | --- |
| "Don the mask" / "Don the mask for coding" | `/larvah:don` | Applies the core lines and the matching scenes |
| "Doff the mask" | `/larvah:doff` | Removes the mask for the rest of the chat |
| "Check the mask" | `/larvah:check` | Reports in ten lines or fewer: what is in force, the budget, sources used and skipped |
| "Scratch that from the mask" | `/larvah:scratch` | Removes a line and anything built on it, and adds a limit against recording it again |
| "Mend the mask" / "Add this to the mask: …" | `/larvah:mend` | Lists proposed changes, numbered, for approval. The only path that saves anything |
| "Remake the mask" | `/larvah:remake` | Rebuilds the mask from the full history, after a backup |
| "Lend the mask" | `/larvah:lend` | Writes the mask out for sharing (letter, Doc or skill file) |
| "Try on this mask" | `/larvah:try` | Screens another person's mask before it is worn |

## Components

| Part | Location | Function |
| --- | --- | --- |
| Skills | `skills/` | The eight commands above, plus an internal `store` skill that reads and writes the mask |
| Mender (agent) | `agents/mender.md` | Proposes changes to the mask; never writes to it |
| Maker (agent) | `agents/maker.md` | Drafts skills, agents or hooks for repeated duties; never installs them |
| Dresser (hook) | `hooks/`, `scripts/dresser.sh` | Applies the mask at session start in Cowork and Claude Code |
| Stagehand (hook) | `hooks/`, `scripts/stagehand.sh` | Restates the core lines each message; off by default |
| `larvahctl` | `scripts/larvahctl.py` | Worn-line rules, secret scan, refusals, budgets, lending and screening |
| Prompter, Doorkeeper, Herald | inside `don`, `try`, `lend` | Scene selection, screening of borrowed masks, and writing the mask out |

Only skills load in the phone app. Hooks and agents run in Cowork and Claude Code.

## Storage

- **File copy** (Claude Code and any chat with file tools): `~/.claude/larvah/mask.json`. `LARVAH_HOME` selects another folder.
- **Claude's memory** (phone app): topics named `Larvah: core lines`, `Larvah: scenes` and `Larvah: scene <name>`. No other memory topic is read or changed.

The file copy is JSON, so the tool needs only Python 3.

Larvah is intended as the only memory-related plugin in use. It is not designed to run alongside other memory plugins.

## Constraints

- **Approval gate.** `larvahctl` writes only with `--approved`, which skills pass only after a yes to that exact change. Agents and scheduled runs never pass it.
- **Worn lines.** Only stated lines, and observed lines that have been confirmed, are applied.
- **Never recorded.** Passwords, keys, card numbers and ID numbers.
- **Never written.** Any line that would stop Claude from flagging mistakes, risks or disagreements.
- **Precedence.** Claude's own rules and Anthropic's rules apply whatever the mask says. A line is an instruction, not a permission.
- **Budgets.** Core lines 600 tokens, scenes 3,000 each (at most two at a time), a borrowed mask 400.

## Install and test

```bash
git clone https://github.com/markpoon/larvah
claude --plugin-dir ./larvah
```

Example: `add this to the mask: do five rounds of review before answering`, approve the change, then `don the mask`.

```bash
cd larvah && python3 -m unittest discover -s tests
```

[TESTING.md](TESTING.md) describes the test framework, what has been verified and the app-side tests still to run. The design is in [Larvah plan.md](Larvah%20plan.md).

## License

[MIT](LICENSE), © 2026 Mark Poon.

## Naming

- **Larvah:** the plugin, from *larva*, Latin for a mask.
- **The mask:** the written record that is put on and taken off.
- **Theatre terms:** the helper parts (Mender, Maker, Dresser, Stagehand, Prompter, Doorkeeper, Herald) are named for stage roles.

The plain name "mask" is already used by other projects, including a persona-switching framework, so the plugin uses a distinct spelling.
