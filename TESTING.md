# Testing Larvah

Last updated Nov 24, 2026. Everything below was checked in Claude Code on a Mac. **Nothing has been tested in the phone app or Cowork yet**, and that includes Claude's memory as the store.

## Checked

| What | How | Result |
| --- | --- | --- |
| `larvahctl` (save, load, worn rules, secrets, refusals, scratch, supersede, budget, diff, lend, screen, remake, hooks) | `python3 -m unittest discover -s tests`, 39 tests | Pass |
| Plugin manifest and hooks | `claude plugin validate .` | Pass. The directory check still lists a missing LICENSE (see below) and a missing icon |
| Dresser hook, end to end | Fresh headless session with `--plugin-dir`, a mask holding one line that asks for the code word PELICAN, and the question "what rule were you given at session start?" | Claude quoted the rule and ended with PELICAN. The canary reached Claude |
| `check` by voice | Headless session, said "Check the mask" | The skill loaded, ran `larvahctl.py check`, and reported in under ten lines, including the file location and that memory was not checked |
| `scratch` by voice | Headless session, said "Scratch that from the mask: …" | The line was removed, the "Do not record again" limit was added, and the file was confirmed afterward |

## Not checked yet

| What | Why | How to check |
| --- | --- | --- |
| Memory as the store (the phone app) | Needs separate sessions and the phone app | Memory test below |
| `don`, `doff`, `mend`, `remake`, `lend`, `try` as full Claude conversations | `mend` and `remake` need a real "yes" from you, so they can't run headless | Try each by voice in a normal session; the tool behind each is unit-tested |
| The Mender and Maker agents | Need real sources (sessions, repos) and a scheduled run | Run `larvah:mender` in Claude Code and read `mending.md` |
| The Stagehand | Off by default | `larvahctl.py settings stagehand true --approved`, then watch for the reminder each message |
| Compaction | Needs a long session | Canary check below |
| The Doorkeeper on tricky lines | The tool catches common patterns only; the rest is Claude's judgement | Paste a lent mask with a few sneaky lines into `try` |

## Memory test (to run later, with new sessions)

This is Phase 0: can Claude's memory hold the mask?

1. **Save.** In a chat, say "Add this to the mask: when I say the word OBOE, answer with the word PELICAN." Sign it with "yes". Then ask Claude to remember it under the memory topic `Larvah: core lines`.
2. **Read back.** Ask Claude to read that memory topic back word for word. Note whether memory filtered, shortened or refused anything.
3. **Load in a new chat.** Open a new chat. Say "Don the mask", then say "OBOE". Claude should answer PELICAN.
4. **Phone app.** Repeat steps 3 on the phone with only skills loaded.
5. **Cowork.** Start a Cowork session. The Dresser should put the mask on with no phrase.
6. **Compaction.** In a long session, run enough turns to force compaction, then say "OBOE".
7. **After a load.** Change the line in memory by hand, start a new chat, and say "Don the mask". Claude should show the difference and wait for your signature, and say nothing if there is none.

If memory refuses or reshapes the lines, the fallback in the plan is a Claude Doc or a personal mask skill.

## Known gaps and judgement calls

- **License.** MIT, added Nov 24, 2026: `LICENSE` file plus `"license": "MIT"` in `plugin.json`.
- **Icon.** There is no plugin icon yet. The directory only warns about this.
- **JSON, not YAML.** The plan's example shows YAML. The workshop copy is JSON so the tool needs nothing beyond Python 3. The fields are the same.
- **Agents' write limits are by instruction.** The Mender and Maker are told to write only `mending.md` and `drafts/`, but they hold the Write tool, so the limit is not enforced by the platform. The mask itself is protected by the `--approved` flag, which the agents are told never to pass.
- **Scratch limits are worn.** A "Do not record again: …" limit is a worn core line, so it costs a few tokens of budget. That is by design in the plan, but it means scratching many lines grows the core.
- **Secret scan is pattern-based.** It catches common key formats, card numbers that pass the Luhn check, SSNs and "password is …". It is a safety net, not a guarantee.
- **The `${CLAUDE_PLUGIN_ROOT}` variable** is used in the hook commands. It worked in the headless test. Whether the phone app or Cowork expand it the same way is untested.
