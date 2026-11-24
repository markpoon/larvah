# Larvah: a stage mask for Claude

Nov 21, 2026 · @Mark Poon

Larvah is a plugin for Claude. It keeps a written mask of how you want Claude to work with you, and when you say "don the mask", Claude works under it. There is one mask, and it is either on or off. You approve every change to the mask, and nothing leaves Claude. This tab is the current plan. The household draft that came before it is kept in the file `Household draft.md`.

## The theme

The plugin uses a theatre theme, and every command can be spoken out loud. You are the director. Claude is the actor, and the mask is what Claude puts on when it works for you. Claude's own customs and Anthropic's rules are the house rules: they bind everyone in the building and are not open to negotiation, so your mask is written inside those limits.

Every spoken phrase contains the word "mask", so an everyday "check" or "try" never switches anything on or off by accident.

| Plan part | Theatre name | What it does |
| --- | --- | --- |
| The plugin | **Larvah** | Your stage mask for Claude |
| You | The director | You approve every change to the mask |
| Claude | The actor | Works under the mask when you ask |
| Claude's memory | The prop room | Your mask is kept there |
| Anthropic's rules and Claude's own customs | The house rules | Binding on everyone; the mask works inside them |
| The profile | **The mask** | Your written ways of working |
| One entry | **A line** | One line of the mask |
| Always-on rules | **Core lines** | Loaded whenever the mask is on |
| A kind of work, with its own rules | **A scene** | Loaded only when that work comes up |
| History and evidence | **The archive** | Searched, never loaded |
| Picking which scenes to load | **Prompter** | Brings the right lines forward at the right moment |
| The updater | **Mender** | Proposes changes to the mask for your approval |
| A full rebuild | **Remake** | Rebuilds the mask from scratch |
| The builder | **Maker** | Notices repeated duties and drafts a skill or agent to handle them |
| Which plugin goes first | **Priorities** | Settles overlaps between installed plugins |
| Token budget | **The budget** | What the mask may spend per chat |
| Start-up hook | **Dresser** | Puts the mask on when a session starts |
| Per-message hook | **Stagehand** | Keeps the mask on through a long session |
| Always-on project | **The green room** | Your standing project, where the mask is always on |
| Sharing out | **Herald** | Writes your mask out for someone else |
| Sharing in | **Doorkeeper** | Screens someone else's mask before Claude tries it on |
| Venues: chat, Cowork, Claude Code | **The stage, the wings, the workshop** | Daily dealings; work that continues while you're away; where the records are kept |

## Scope

Once installed, Larvah is self-contained: skills, commands, agents and hooks, with no MCP servers and nothing running outside Claude. The baseline is a person in the phone app, where only a plugin's skills load ([platform support](https://claude.com/docs/plugins/platform-support)).

| Venue | Where | What works |
| --- | --- | --- |
| **The stage** | Chat on phone, web and desktop | Don, doff, check and scratch; the mending across past chats; the green room; the Maker later |
| **The wings** | Cowork on phone or desktop | The Mender and the Maker as agents on a weekly cloud schedule; the Dresser puts your mask on automatically |
| **The workshop** | Claude Code | Local sources such as sessions and repos, a git copy of the mask, and readers for claude-reflect and claude-smart |

Every phase is built and tested first on the stage, in the phone app. Organization owners can switch off memory, skills or plugins for their organization, so `check` says plainly when a piece is unavailable. Your own setup is the workshop, which is built last.

## The mask

The mask is a set of one-line lines in six sections. Every line records where it came from and how sure it is, and only lines you stated or confirmed are ever worn.

| Section | Holds | Example line |
| --- | --- | --- |
| **Preferences** | How you want Claude to work | Do five rounds of review before answering a question |
| **Limits** | What Claude must not do or raise | Don't raise a topic unless I do |
| **Projects** | Active work, with pointers | Palimpsest, repo `markpoon/palimpsest` |
| **Facts** | Stable facts that change answers | Toronto time zone; MacBook Air and Mac Mini |
| **Habits** | Repeated behavior, with counts | Schedules overnight runs to finish unbuilt work |
| **Priorities** | Which installed plugin goes first | Brainstorming: superpowers, not agentic-council |

Each line in the mask's full form:

```yaml
- id: pref-iterate
  section: preferences
  text: Do five rounds of review before answering a question.
  kind: stated          # stated | observed | inferred
  scene: [always]       # or coding, writing, research ...
  share: yes            # may it travel when you lend the mask
  source: chat 2026-11-21
  confirmed: 2026-11-21
```

Three rules keep the mask honest:

- **Only stated or confirmed lines are worn.** Observed ones wait for your confirmation. Inferred ones are never worn; they exist only for the Maker to test.
- **One line per line.** A line that needs a paragraph is really a skill, and the Maker should propose one.
- **Nobody edits YAML on a phone.** You change the mask in words, such as "change the review rule to three rounds".

### Core lines, scenes and the archive

The mask can grow large without making every chat more expensive. Only the core lines and the scene you're working in are loaded.

| Level | Holds | Loaded | Budget |
| --- | --- | --- | --- |
| **Core lines** | Rules that always apply, plus the list of scenes | Whenever the mask is on | Up to 600 tokens |
| **Scenes** | Rules, priorities and short examples for one kind of work | When that work comes up, at most two at a time | Up to 3,000 tokens each |
| **The archive** | Evidence, longer examples, history | Never; searched when a question needs it | No set limit |

The list of scenes works like skill descriptions: one line each, so the Prompter can pick the right scene from the task alone. You can also name one, as in "don the mask for coding". Likely scenes for you are coding, storytelling for Palimpsest, research, and planning and agents.

### Where the mask is kept

The mask lives in Claude's own records, so one public plugin serves everyone and ships no personal data.

| Store | Capacity | Loads only what's needed? | Edit on a phone | Catch |
| --- | --- | --- | --- | --- |
| Memory, one topic per scene | A size cap per topic: about 48 KB in my own sessions, which may differ for others | Yes: topic names are always visible, and contents are read only when needed | Yes, by asking | Memory filters what it stores, and Anthropic can change how it works |
| A personal mask skill | Large: a short SKILL.md plus one reference file per scene | Yes: the description loads first, and reference files only when used | No; a change means a new upload | Larvah builds the file and you upload it |
| A Claude Doc, one tab per scene | Large | Yes, if a skill can read a single tab | Yes, directly | Untested: whether a skill in chat can read a Doc |
| Past-chat search | Your whole history | Yes, by search | Not needed | The archive only |
| A git repo | Unlimited | Yes | No | The workshop only |

The recommended mix: memory holds the core lines, the list of scenes, and small scenes that change often. A personal mask skill holds large scenes that have stopped changing. Past-chat search serves as the archive. When a scene outgrows memory or settles, the Mender proposes moving it into the next version of the mask skill.

## Putting the mask on and off

On the stage you call on Larvah by saying so, and Claude applies the matching skill. A plugin's commands load as skills in chat, and Claude applies them when they fit, so every phrase includes the word "mask".

| Say | Or type | What happens |
| --- | --- | --- |
| "Don the mask" or "Don the mask for coding" | `/larvah:don` | Claude puts on your mask: the core lines plus the right scenes |
| "Doff the mask" | `/larvah:doff` | The mask comes off for the rest of the chat. Text already in the chat stays, so a clean slate means a new chat |
| "Check the mask" | `/larvah:check` | Up to ten lines: what's in force, which scenes are loaded, which sources were used and which were skipped |
| "Scratch that from the mask" | `/larvah:scratch` | Removes a line and anything built on it, and adds a limit so it isn't learned again |
| "Mend the mask" | `/larvah:mend` | The Mender's proposed changes, numbered, for you to approve |
| "Remake the mask" | `/larvah:remake` | A full rebuild of the mask from scratch |
| "Lend the mask" | `/larvah:lend` | The Herald writes your mask out to share |
| "Try on this mask" | `/larvah:try` | Someone else's mask, screened by the Doorkeeper, for this chat only |

Where each part runs ([platform support](https://claude.com/docs/plugins/platform-support)):

| Part | The stage | The wings | The workshop |
| --- | --- | --- | --- |
| Skills and commands | Loads | Loads | Loads |
| The Dresser (start-up hook) and the Stagehand (per-message hook) | Ignored | Loads | Loads |
| The Mender and the Maker as agents | Ignored | Loads | Loads |

So on the stage your mask goes on once per chat, or stays on in **the green room**: a project whose instructions hold your core lines, so every chat there starts with the mask on. In the wings and the workshop, the Dresser puts your mask on at every start, resume and compaction. The Stagehand stays off unless your mask starts to slip in long sessions.

## The Mender and the mending

The Mender reads only the sources the venue allows and you switch on, then brings a mending: numbered proposed changes to the mask. Nothing enters the mask until you sign off, for example by replying "yes to 1 and 3".

| Source | What it can learn | Venue |
| --- | --- | --- |
| The current chat | Preferences you state, corrections | All |
| Past-chat search | Preferences you repeat, corrections across chats | All |
| Claude's memory | Facts already on file | All, one import at setup |
| Claude Code sessions | Commands you repeat, tools you approve | The workshop |
| Your GitHub repos | Active projects, languages, how often you push | The workshop |
| claude-reflect's queue and claude-smart's database, if installed | Corrections those plugins have already caught | The workshop |

Each mending:

1. **Collects** only material newer than the last mending.
2. **Proposes** lines from your own words and repeated actions, marking each as stated or observed. It skips secrets, ID and account numbers, and any sensitive topic you haven't allowed.
3. **Merges** against the mask: it removes duplicates, updates counts and dates, and marks an older line as superseded when you contradict it, instead of deleting it.
4. **Presents** the changes in plain words, at most ten at a time.
5. **Waits** for your signature.

**After a load.** Once Claude's memory has loaded in the chat and Larvah has confirmed it, Larvah copies those parameters and compares them with the mask. If nothing differs, it says nothing. If anything differs, it shows the changes in plain words and waits for your approval. Nothing enters the mask until you sign off.

On the stage the mending runs when you ask for it. In the wings it runs weekly as a scheduled task. **Remake the mask** runs the same steps over your whole history and proposes a fresh mask as one set of changes.

## The Maker and new staff

The Maker looks for duties you repeat, checks the staff you already have, and proposes a new member only when nobody existing covers the duty. It drafts; you decide. A habit qualifies once it has been seen at least three times across at least two weeks.

For each one, the Maker stops at the first step that fits:

1. **Already staffed?** Add a line that points at the existing skill or plugin, or propose an edit to it.
2. **A fixed procedure for one kind of task?** Draft a skill.
3. **Needs its own context, tools or a long run?** Draft an agent, which works in the wings and the workshop.
4. **Must happen every time?** Draft a hook, for the wings and the workshop.
5. **Needs a timetable?** Draft a scheduled task.

Every proposal comes with its evidence, the draft, one test case, and what it costs to run. Drafting is handed to tools you already have, such as superpowers' `writing-skills`, so the Maker stays small. On the stage a draft arrives as a card you can save. The Maker never installs, enables or schedules anything itself. It edits only the staff it drafted, and it proposes retiring any of them that go unused for 60 days.

**Priorities** are the Maker's other job. Your installed plugins overlap: brainstorming exists in both superpowers and agentic-council, testing strategy in both engineering and agentic-council, and charts in both data and dataviz. The Priorities section of the mask names the winner of each overlap, and the Maker flags new overlaps whenever you install a plugin. It is an instruction to Claude, not a switch: Larvah can't turn other plugins off.

## Lending the mask

You can lend your mask to someone else, but never all of it. A lent mask carries only the sections about how Claude should work, and the person receiving it tries it on before keeping anything.

| Section | Travels by default | Why |
| --- | --- | --- |
| Preferences | Yes | How you like Claude to work, which is the useful part to share |
| Priorities | Yes | Which plugin wins each overlap |
| Limits | No | Can reveal sensitive topics |
| Projects | No | Your work, names and repos |
| Facts | No | Facts about you |
| Habits | No | Your history; it travels only as skills the Maker built from it |

Any line can override its section's default. Sources, dates and counts are stripped before anything leaves, because they reveal your history.

**The Herald** writes your mask out in one of three forms, all of which work from a phone:

| Form | Say | The other person | Best for |
| --- | --- | --- | --- |
| A letter (text) | "Lend the mask" | Pastes it into a chat with "try on this mask" | Sending in a message |
| A Claude Doc | "Lend the mask as a doc" | Opens the link and says "try on the mask at this link" | Reading first, and receiving your later updates |
| A skill file | "Lend the mask as a skill" | Uploads it in Customize > Skills | A mask worn often |

A Doc's sharing settings can only be changed on the web or in the desktop app, so a phone-only person sends the letter.

**The Doorkeeper** stands at the door when someone else's mask arrives:

1. **Shown in full.** Every line is shown in plain words before it's worn.
2. **Refused, not trimmed.** Lines that would make Claude stop flagging mistakes or risks, hide things from you, use tools or data, send anything anywhere, or claim extra permissions are refused.
3. **No impersonation.** A mask can't name a real person for Claude to imitate.
4. **Its own budget.** A borrowed mask gets 400 tokens by default, so it can't crowd out yours.
5. **No proof of authorship.** The author's name on a mask is a claim, not something Larvah can verify.

Then you choose: try it on for this chat only, try it on alongside your own (your lines win any conflict), or keep chosen lines, as in "keep 2 and 4". Kept lines stay tagged with where they came from.

Why the Doorkeeper matters: wearing someone else's mask puts Claude under their influence, and that is the risk the Doorkeeper screens for.

## The house rules

You control what the Mender may read, what your mask may contain, and when the mask is on. Each control is a line in the mask or a single phrase, never a hidden switch.

| Control | Where | Default |
| --- | --- | --- |
| Which sources the Mender reads | Plugin settings, one per source | As in the Mender's table |
| Sensitive topics (health, money, identity, politics) | Limits, one topic at a time; memory's own sensitive-topics setting also applies | None allowed |
| Never recorded | Built in: passwords, keys, ID and account numbers | Fixed |
| What gets worn | Your signature on each mending | Nothing unsigned |
| On or off | Don, doff, check | Off, except in the green room |
| Size | The budget | Core lines 600 tokens; scenes up to 3,000 each, at most two at a time |
| Forgetting | "Scratch that" removes the line, anything built on it, and adds a limit | On request |

Three limits are deliberate:

- **The mask is instructions, not permissions.** It can't unlock a folder or a tool. Those approvals still happen where they always do.
- **Some lines are never written.** The Mender refuses any line that would make Claude stop flagging mistakes, risks or disagreements. A director well served is told the truth.
- **The house rules come first.** Claude's own customs and Anthropic's rules apply whatever the mask says. Larvah works inside them, and `check` says when one of them overrode a line.

Platform memory and its settings carry on as before. Larvah keeps its mask in memory but never rewrites other memory topics.

## Other plugins

Several plugins already learn from their people, but none keeps a mask you put on and take off, with every line approved, that works in chat on a phone. Larvah borrows their best ideas and depends on none of them. It is meant to be your only memory-related plugin, so don't run it on top of the plugins below: each one stores its own rules, and nothing decides which wins.

| Plugin | What it does | What Larvah borrows | Why not just use it |
| --- | --- | --- | --- |
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | Catches corrections such as "no, use X" and applies them to CLAUDE.md after review; proposes skills from repeated patterns | Corrections as a cheap signal; a review queue | Writes to CLAUDE.md, which is always on and only in Claude Code |
| [claude-smart](https://github.com/ReflexioAI/claude-smart) | Learns preferences and skills at the end of each session | Learning from what worked, not only corrections | Needs a local backend; not supported in Cowork |
| [self-improving-agent](https://www.skills.sh/alirezarezvani/claude-skills/self-improving-agent) | Curates what auto-memory captured | Separating capturing from curating, which is the Mender's job | Claude Code project files only |
| [autoskill](https://skills.sh/nicknisi/claude-plugins/autoskill) | Proposes edits to skills that were active when you corrected Claude | Improve existing staff before drafting new | Coding sessions only |
| [skilltrace](https://github.com/Lover0ne/skilltrace) | Turns finished work into skills without asking | A warning | Unasked new staff are the sprawl Larvah avoids |
| [mystique](https://awesome.ecosyste.ms/projects/github.com%2Fmtking2%2Fmystique) | A switchable role re-added every turn by a hook | The Stagehand | Roles written by hand, not learned |

**Names.** The earlier name check, on Nov 21, found that **seneschal** is already taken by [an AI pipeline orchestrator built on Claude](https://github.com/Fishy49/seneschal), so it's out, and that **rusui** turned up no matches. The theatre names were checked on Nov 23. [TTigger/mask](https://github.com/TTigger/mask) is an existing Claude Code project with the same name: a framework that turns a source into a switchable persona. On Nov 24 the plugin was renamed **Larvah**, a deliberate misspelling of the old word for a mask (Latin *larva*), because "Larva" was already in use on GitHub and "Mask" overlapped TTigger/mask. A GitHub name search found one unrelated repository called larvah. The commands and the mask itself keep their theatre names. The search found no plugin or agent named Stagehand, Prompter, Mender or Dresser, but the search was shallow, and Maker, Herald and Doorkeeper were not checked. "Stagehand" is also the name of a browser-automation library, which may cause confusion. The helper names sit under the plugin's prefix, as in `larvah:mender`, so common words such as dresser and prompter shouldn't clash. Re-check every name before publishing.

## Roadmap

The roadmap has 5 phases and 4 gates. Phase 0 is the memory test in [TESTING.md](TESTING.md).

There are no dates yet. Each phase starts when the gate before it passes, and Phase 0 is small enough to do in one sitting.

## Risks, open questions and tests

The biggest risk is depending on memory, which Larvah doesn't control and Anthropic can change. That is why Phase 0 tests memory storage before anything else is built.

| Risk | What goes wrong | Mitigation |
| --- | --- | --- |
| Memory changes how it stores things | The mask is reshaped or partly refused | Phase 0 test; a Doc or mask-skill fallback |
| Hooks and agents are ignored on the stage | The mask needs a phrase in every chat | The green room; skills work everywhere |
| The mask slips in long chats | Behavior slides back to default | The Dresser re-applies it after compaction; the Stagehand if needed |
| The mask bloats | Chats cost more and the mask blurs | Budgets, one-line lines, scenes loaded on demand |
| The Mender learns one-offs | The mask fits a moment, not you | Three sightings and your signature before a habit is worn |
| Lines go stale | Advice based on old facts | The Mender proposes retiring anything unconfirmed for 90 days |
| New staff sprawl | Too many small skills | Check existing staff first; retire after 60 days unused |
| A borrowed mask carries harm | Hidden instructions | The Doorkeeper |
| A secret slips into the mask | Exposure through memory or sharing | The never-record list, plus a scan before anything is written or lent |

Open questions for you:

- [ ] Which scenes to start with: coding, storytelling, research, planning?
- [ ] Should the green room be created during setup, or left for you to make?
- [ ] Are the theatre names right? (The plugin name is settled: Larvah.)

How we'll know it helps:

- **Canary check.** One test line asks for a fixed code word. Ask for it after starting, resuming and compacting a chat. If it's missing, the mask isn't reaching Claude.
- **Blind pairs.** Ten prompts typical of your work, each answered with and without your mask, asked from your phone. You pick the better answer without knowing which is which. Larvah stays only if it wins clearly.
- **Fewer corrections.** Count how often you correct format, length or approach in a week, before and after.
- **Size check.** `check` reports the loaded size against the budget.

## Seed lines and sources

Lines you stated in this chat, which the first mending will propose:

| Line | Kind | Scene |
| --- | --- | --- |
| Do five rounds of iteration before answering a question | stated | always |
| In verbose mode, describe each step, the reasoning and the alternatives considered | stated | on request |
| Double-check findings before reporting them | stated | research |
| Check the web and think it through before naming things | stated | naming |
| When describing what Claude knows about you, say which sources were checked and which weren't | observed, needs your OK | always |

Sources for the platform facts, checked Nov 21: [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude), [Plugin feature support across platforms](https://claude.com/docs/plugins/platform-support), [Chat search and memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context), [Get started with Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork), [Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference), [Publish to the directory](https://claude.com/docs/directory/publish).
