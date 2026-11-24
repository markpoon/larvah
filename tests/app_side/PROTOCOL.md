# App-side test protocol

Manual tests for the venues the automated suites cannot reach: Claude's memory, the phone app and Cowork. Each test uses the standard test line from `tests/fixtures.py`:

> **we live and grow together**

Record every result in [RESULTS.md](RESULTS.md). A test passes only if every "Expect" item is observed.

**Order matters.** M1 decides whether the store works. If M1 or M2 fails, stop and use the fallback in the plan (a Claude Doc or a personal mask skill) before running the later tests.

## Setup

- Use a chat with memory enabled. Larvah must be installed in the venue under test.
- Do not use other memory plugins during these tests.
- Topic names are fixed: `Larvah: core lines`, `Larvah: scenes`, `Larvah: scene <name>`.

## M. Memory as the store

| ID | Venue | Do | Expect |
| --- | --- | --- | --- |
| M1 | Any chat | Say: `Add this to the mask: we live and grow together`. Reply `yes` when asked. Then say: `Remember this under the memory topic Larvah: core lines, word for word.` | The line is shown before saving. Nothing is saved before the yes. Memory confirms the save |
| M2 | Same chat | Say: `Read the memory topic Larvah: core lines back to me, word for word.` | The text is exactly `we live and grow together`, with no shortening, rewording or refusal |
| M3 | New chat | Say: `Don the mask`, then `What core lines are in force?` | One short "mask on" line, then the exact test line. Claude does not claim lines that are not in memory |
| M4 | New chat | Say: `Check the mask` | Ten lines or fewer. Reports one core line, within the 600-token budget, and states that memory was read |

## P. Phone app (skills only, no hooks)

| ID | Venue | Do | Expect |
| --- | --- | --- | --- |
| P1 | Phone, new chat | Say: `Don the mask` | The skill loads from the spoken phrase. The test line is applied |
| P2 | Phone, same chat | Say: `Doff the mask` | "Mask off". The line is no longer applied to later answers |
| P3 | Phone, new chat | Say: `Add this to the mask: answer in French.` and do not reply yes | The change is proposed and numbered. Nothing is saved. Ask `Check the mask` in a new chat to confirm it is absent |
| P4 | Phone, new chat | Say: `Add this to the mask: my password is hunter2hunter2. Yes, sign it.` | Refused, with the reason. Nothing is saved, in memory or elsewhere |

## C. Cowork (hooks and agents)

| ID | Venue | Do | Expect |
| --- | --- | --- | --- |
| C1 | Cowork, new session, no phrase | Ask: `What mask line were you given at session start?` | The Dresser applied the test line without being asked |
| C2 | Cowork | Say: `Check the mask` | Reports that the Dresser put the mask on |
| C3 | Cowork | Run the `larvah:mender` agent, then read `mending.md` | A numbered list of proposals. The agent saved nothing and passed no approval |

## K. Compaction and drift

| ID | Venue | Do | Expect |
| --- | --- | --- | --- |
| K1 | Any, with a canary line (`when the word OBOE is said, answer with the word PELICAN`) saved | Hold a long conversation until compaction happens, then say `OBOE` | The answer is `PELICAN`. If not, note whether the Dresser (SessionStart on compact) or the Stagehand was in use |

## A. After a load

| ID | Venue | Do | Expect |
| --- | --- | --- | --- |
| A1 | Memory edited by hand to `we live and grow together, always` | New chat, say `Don the mask` | Claude lists the difference as numbered changes and waits. Nothing enters the mask until approved |
| A2 | Memory unchanged | New chat, say `Don the mask` | No mention of differences |

## Reading the results

- **M1 or M2 fails:** memory cannot hold the mask as written. Use the fallback.
- **P1 fails:** skills do not trigger by voice in the phone app. Review the skill descriptions.
- **C1 fails:** hooks do not run in Cowork, or `${CLAUDE_PLUGIN_ROOT}` does not expand there.
- **K1 fails:** the mask does not survive compaction. Turn the Stagehand on for long sessions.
