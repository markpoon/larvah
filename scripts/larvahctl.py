#!/usr/bin/env python3
"""larvahctl: the small tool behind the Larvah plugin.

It keeps the mask as one JSON file (the workshop copy) and does the jobs that
should be exact and repeatable: reading worn lines, scanning for secrets,
refusing lines that hide risks, counting the budget, lending, screening and
the two hooks (Dresser and Stagehand).

It never decides what goes into the mask. Anything that writes needs the
--approved flag, which the skills only pass after the person has said yes.

Python 3.9 compatible, standard library only.
"""
from __future__ import annotations

import argparse
import datetime
import difflib
import json
import math
import os
import re
import shutil
import sys

SECTIONS = ["preferences", "limits", "projects", "facts", "habits", "priorities"]
PREFIX = {
    "preferences": "pref",
    "limits": "limit",
    "projects": "proj",
    "facts": "fact",
    "habits": "habit",
    "priorities": "prio",
}
# Sections that travel when the mask is lent (a line can override with share).
SHARE_DEFAULT = {
    "preferences": True,
    "priorities": True,
    "limits": False,
    "projects": False,
    "facts": False,
    "habits": False,
}
KINDS = ["stated", "observed", "inferred"]
DEFAULT_SETTINGS = {
    "auto_don": True,       # the Dresser puts the mask on at session start
    "stagehand": False,     # the Stagehand reminder is off unless needed
    "budget_core": 600,
    "budget_scene": 3000,
    "budget_borrowed": 400,
}

# ---------------------------------------------------------------- storage


def larvah_home() -> str:
    return os.environ.get("LARVAH_HOME") or os.path.join(
        os.path.expanduser("~"), ".claude", "larvah"
    )


def mask_path() -> str:
    return os.path.join(larvah_home(), "mask.json")


def today() -> str:
    return datetime.date.today().isoformat()


def empty_mask() -> dict:
    return {
        "version": 1,
        "settings": dict(DEFAULT_SETTINGS),
        "scenes": {},
        "lines": [],
    }


def load(create: bool = False) -> dict:
    path = mask_path()
    if not os.path.exists(path):
        data = empty_mask()
        if create:
            save(data)
        return data
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # Fill in anything an older file lacks.
    merged = dict(DEFAULT_SETTINGS)
    merged.update(data.get("settings", {}))
    data["settings"] = merged
    data.setdefault("scenes", {})
    data.setdefault("lines", [])
    return data


def save(data: dict) -> None:
    os.makedirs(larvah_home(), exist_ok=True)
    path = mask_path()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def tokens(text: str) -> int:
    """Rough token estimate: about four characters per token."""
    return int(math.ceil(len(text) / 4.0))


# ---------------------------------------------------------------- rules

# Things that are never recorded or lent: secrets and ID numbers.
SECRET_PATTERNS = [
    ("an API key", re.compile(r"\b(?:sk|pk|rk)-[A-Za-z0-9_-]{16,}")),
    ("an AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("a Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("a Google key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}")),
    ("a private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "a password or token",
        re.compile(
            r"(?i)\b(?:pass(?:word|wd)?|pwd|secret|token|api[_ -]?key)\b\s*(?:is|=|:)\s*\S+"
        ),
    ),
    ("a social security number", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    (
        "an account or ID number",
        re.compile(
            r"(?i)\b(?:account|acct|routing|passport|sin|ssn|licen[sc]e)\s*"
            r"(?:no\.?|number|#)?\s*[:=]?\s*\d{6,}"
        ),
    ),
]
CARD_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def scan_secrets(text: str) -> list:
    """Return a list of plain-word reasons the text must not be recorded."""
    found = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            found.append(label)
    for match in CARD_RE.finditer(text):
        digits = re.sub(r"[^0-9]", "", match.group(0))
        if 13 <= len(digits) <= 19 and luhn_ok(digits):
            found.append("a card number")
            break
    return found


# Lines that would make Claude stop telling the truth about mistakes or risks.
HIDING_PATTERNS = [
    re.compile(
        r"(?i)\b(?:stop|don'?t|do not|never|quit|avoid)\b[^.\n]{0,30}"
        r"\b(?:flag|flagging|mention|mentioning|warn|warning|point out|pointing out|"
        r"tell me about|raise|raising|report|reporting)\b[^.\n]{0,60}"
        r"\b(?:mistake|mistakes|error|errors|risk|risks|disagreement|disagreements|"
        r"problem|problems|bug|bugs|concern|concerns)\b"
    ),
    re.compile(r"(?i)\b(?:always agree|never disagree|never push back|don'?t push back)\b"),
    re.compile(r"(?i)\b(?:hide|conceal)\b[^.\n]{0,40}\b(?:from me|from the user|from the person)\b"),
    re.compile(r"(?i)\bwithout (?:telling|informing|asking) (?:me|the user|the person)\b"),
]

# Extra things the Doorkeeper refuses in someone else's mask.
FOREIGN_PATTERNS = [
    (
        "sends something somewhere",
        re.compile(
            r"(?i)\b(?:send|email|e-mail|post|upload|forward|transmit|submit)\b[^.\n]{0,50}"
            r"\b(?:to|at|via)\b"
        ),
    ),
    (
        "uses tools or data",
        re.compile(
            r"(?i)\b(?:use|run|call|execute|invoke|open)\b[^.\n]{0,25}"
            r"\b(?:tool|tools|bash|shell|terminal|browser|api|script|command|commands|"
            r"files?|connector)\b"
        ),
    ),
    (
        "claims extra permissions",
        re.compile(
            r"(?i)\b(?:you (?:are|have) (?:allowed|authori[sz]ed|permitted)|"
            r"permission|admin|override|bypass|ignore (?:previous|prior|all|the) )\b"
        ),
    ),
    (
        "names a real person to imitate",
        re.compile(
            r"(?i)\b(?:pretend to be|act as|impersonate|speak as|write as|"
            r"respond as|answer as)\b\s+(?:[A-Z][a-z]+ [A-Z][a-z]+)"
        ),
    ),
]


def refuse_reasons(text: str) -> list:
    """Reasons a line must never be written into the person's own mask."""
    reasons = [f"it contains {x}" for x in scan_secrets(text)]
    for pattern in HIDING_PATTERNS:
        if pattern.search(text):
            reasons.append("it would make Claude stop flagging mistakes, risks or disagreements")
            break
    return reasons


def foreign_reasons(text: str) -> list:
    """Reasons the Doorkeeper refuses a line from someone else's mask."""
    reasons = list(refuse_reasons(text))
    for label, pattern in FOREIGN_PATTERNS:
        if pattern.search(text):
            reasons.append(label)
    if re.search(r"(?i)\b(?:hide|conceal|secretly|quietly)\b", text):
        reasons.append("hides things from you")
    # Preserve order, drop repeats.
    seen = []
    for r in reasons:
        if r not in seen:
            seen.append(r)
    return seen


# ---------------------------------------------------------------- lines


def is_worn(line: dict) -> bool:
    """Only stated lines, or observed lines you have confirmed, are worn."""
    if line.get("status", "active") != "active":
        return False
    kind = line.get("kind")
    if kind == "stated":
        return True
    if kind == "observed":
        return bool(line.get("confirmed"))
    return False  # inferred lines are never worn


def worn_lines(data: dict, scene: str = "always") -> list:
    return [
        ln
        for ln in data["lines"]
        if is_worn(ln) and scene in ln.get("scene", ["always"])
    ]


def slug(text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())[:4]
    return "-".join(words) or "line"


def new_id(data: dict, section: str, text: str) -> str:
    base = f"{PREFIX[section]}-{slug(text)}"
    taken = {ln["id"] for ln in data["lines"]}
    candidate, n = base, 2
    while candidate in taken:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def make_line(data: dict, section: str, text: str, kind: str, scene: list,
              share, source: str) -> dict:
    return {
        "id": new_id(data, section, text),
        "section": section,
        "text": text.strip(),
        "kind": kind,
        "scene": scene or ["always"],
        "share": SHARE_DEFAULT[section] if share is None else share,
        "source": source or "chat " + today(),
        "confirmed": today(),
        "status": "active",
    }


def lines_to_text(lines: list) -> str:
    return "\n".join("- " + ln["text"] for ln in lines)


# ---------------------------------------------------------------- commands


def cmd_init(args) -> int:
    data = load(create=True)
    print(f"mask file: {mask_path()} ({len(data['lines'])} lines)")
    return 0


def cmd_core(args) -> int:
    data = load()
    lines = worn_lines(data, "always")
    if not lines:
        return 0
    print(lines_to_text(lines))
    return 0


def cmd_scenes(args) -> int:
    data = load()
    for name, desc in sorted(data["scenes"].items()):
        print(f"{name}: {desc}")
    return 0


def cmd_scene(args) -> int:
    data = load()
    lines = worn_lines(data, args.name)
    if lines:
        print(lines_to_text(lines))
    return 0


def cmd_scene_set(args) -> int:
    if not args.approved:
        print(f"PROPOSED scene {args.name}: {args.description} (add --approved to write)")
        return 2
    data = load(create=True)
    data["scenes"][args.name] = args.description
    save(data)
    print(f"scene {args.name} saved")
    return 0


def cmd_check(args) -> int:
    data = load()
    s = data["settings"]
    core = worn_lines(data, "always")
    core_tokens = tokens(lines_to_text(core))
    print(f"mask file: {mask_path()}" + ("" if os.path.exists(mask_path()) else " (not created yet)"))
    by_kind = {}
    for ln in data["lines"]:
        by_kind[ln["kind"]] = by_kind.get(ln["kind"], 0) + 1
    active = [ln for ln in data["lines"] if ln.get("status", "active") == "active"]
    print(f"lines: {len(active)} active; "
          + ", ".join(f"{k} {v}" for k, v in sorted(by_kind.items())))
    waiting = [ln for ln in active if not is_worn(ln)]
    print(f"worn: {len(active) - len(waiting)}; waiting for you or never worn: {len(waiting)}")
    flag = "OVER BUDGET" if core_tokens > s["budget_core"] else "within budget"
    print(f"core lines: {len(core)} lines, about {core_tokens} of {s['budget_core']} tokens ({flag})")
    for name in sorted(data["scenes"]):
        sc = worn_lines(data, name)
        t = tokens(lines_to_text(sc))
        flag = "OVER BUDGET" if t > s["budget_scene"] else "within budget"
        print(f"scene {name}: {len(sc)} lines, about {t} of {s['budget_scene']} tokens ({flag})")
    print(f"Dresser (auto on at start): {'on' if s['auto_don'] else 'off'}; "
          f"Stagehand (reminder each message): {'on' if s['stagehand'] else 'off'}")
    return 0


def cmd_scan(args) -> int:
    text = sys.stdin.read() if args.text is None else args.text
    reasons = scan_secrets(text)
    if reasons:
        print("BLOCKED: " + "; ".join(reasons))
        return 1
    print("clean")
    return 0


def validate_new(data: dict, section: str, text: str, kind: str) -> list:
    problems = []
    if section not in SECTIONS:
        problems.append(f"unknown section '{section}'")
    if kind not in KINDS:
        problems.append(f"unknown kind '{kind}'")
    if not text.strip():
        problems.append("empty line")
    if "\n" in text.strip():
        problems.append("a line must be one line; a paragraph is really a skill")
    problems.extend(refuse_reasons(text))
    return problems


def cmd_add(args) -> int:
    data = load()
    scene = [x.strip() for x in args.scene.split(",") if x.strip()]
    problems = validate_new(data, args.section, args.text, args.kind)
    if problems:
        print("REFUSED: " + "; ".join(problems))
        return 1
    for ln in data["lines"]:
        if ln.get("status", "active") == "active" and norm(ln["text"]) == norm(args.text):
            print(f"DUPLICATE of {ln['id']}: {ln['text']}")
            return 3
    if not args.approved:
        print(f"PROPOSED [{args.section}/{args.kind}] {args.text.strip()} (add --approved to write)")
        return 2
    share = None if args.share is None else (args.share == "yes")
    line = make_line(data, args.section, args.text, args.kind, scene, share, args.source)
    if args.supersede:
        found = False
        for ln in data["lines"]:
            if ln["id"] == args.supersede:
                ln["status"] = "superseded"
                ln["superseded_by"] = line["id"]
                found = True
        if not found:
            print(f"no line with id {args.supersede}")
            return 1
    data["lines"].append(line)
    save(data)
    print(f"added {line['id']}: {line['text']}")
    return 0


def cmd_remove(args) -> int:
    """Scratch a line: remove it and anything built on it, and add a limit."""
    data = load()
    target = None
    for ln in data["lines"]:
        if ln["id"] == args.id_or_text or norm(ln["text"]) == norm(args.id_or_text):
            target = ln
            break
    if target is None:
        # allow a unique partial match
        matches = [ln for ln in data["lines"]
                   if norm(args.id_or_text) and norm(args.id_or_text) in norm(ln["text"])]
        if len(matches) == 1:
            target = matches[0]
        elif len(matches) > 1:
            print("AMBIGUOUS: " + "; ".join(f"{m['id']}: {m['text']}" for m in matches))
            return 3
    if target is None:
        print("NOT FOUND")
        return 1
    built_on = [ln for ln in data["lines"] if ln.get("built_on") == target["id"]]
    removed = [target] + built_on
    ids = {ln["id"] for ln in removed}
    data["lines"] = [ln for ln in data["lines"] if ln["id"] not in ids]
    # Add a limit so the same thing is not learned again (unless this is a limit).
    note = ""
    if target["section"] != "limits":
        limit = make_line(
            data, "limits", f"Do not record again: {target['text']}", "stated",
            ["always"], False, "scratch " + today()
        )
        limit["scratched"] = True
        data["lines"].append(limit)
        note = f"; added limit {limit['id']}"
    save(data)
    print("removed " + ", ".join(sorted(ids)) + note)
    return 0


def cmd_diff(args) -> int:
    """Compare lines read from Claude's memory (stdin, one per line) with the mask."""
    data = load()
    existing = [ln for ln in data["lines"] if ln.get("status", "active") == "active"]
    incoming = [re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", raw).strip()
                for raw in sys.stdin.read().splitlines()]
    incoming = [x for x in incoming if x]
    new, similar, same = [], [], []
    for text in incoming:
        best, best_ratio = None, 0.0
        for ln in existing:
            r = difflib.SequenceMatcher(None, norm(text), norm(ln["text"])).ratio()
            if r > best_ratio:
                best, best_ratio = ln, r
        if best is not None and best_ratio >= 0.999:
            same.append(text)
        elif best is not None and best_ratio >= 0.75:
            similar.append((text, best))
        else:
            new.append(text)
    if not new and not similar:
        print("NO DIFFERENCES")
        return 0
    for text in new:
        extra = refuse_reasons(text)
        print("NEW: " + text + (f"  [would be refused: {'; '.join(extra)}]" if extra else ""))
    for text, ln in similar:
        print(f"CHANGED?: memory says '{text}' but the mask has {ln['id']}: '{ln['text']}'")
    print(f"unchanged: {len(same)}")
    return 10


def cmd_backup(args) -> int:
    src = mask_path()
    if not os.path.exists(src):
        print("nothing to back up")
        return 1
    dst = os.path.join(larvah_home(), f"mask.{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    shutil.copy2(src, dst)
    print(dst)
    return 0


def cmd_reset(args) -> int:
    if not args.approved:
        print("PROPOSED reset (backs up first; add --approved to run)")
        return 2
    if os.path.exists(mask_path()):
        cmd_backup(args)
    old = load()
    fresh = empty_mask()
    fresh["settings"] = old["settings"]
    fresh["scenes"] = old["scenes"]
    save(fresh)
    print("mask reset; settings and scenes kept")
    return 0


def cmd_bulk(args) -> int:
    """Add many lines from JSON on stdin: [{section,text,kind,scene,share,source}]."""
    items = json.load(sys.stdin)
    data = load()
    refused, duplicate, ready = [], [], []
    for item in items:
        text = item.get("text", "")
        problems = validate_new(data, item.get("section", ""), text, item.get("kind", "stated"))
        if problems:
            refused.append((text, problems))
            continue
        if any(norm(ln["text"]) == norm(text) for ln in data["lines"]
               if ln.get("status", "active") == "active"):
            duplicate.append(text)
            continue
        ready.append(item)
    for text, problems in refused:
        print(f"REFUSED: {text} ({'; '.join(problems)})")
    for text in duplicate:
        print(f"DUPLICATE: {text}")
    if not args.approved:
        for item in ready:
            print(f"PROPOSED [{item['section']}/{item.get('kind', 'stated')}] {item['text']}")
        print("(add --approved to write)")
        return 2
    for item in ready:
        line = make_line(data, item["section"], item["text"], item.get("kind", "stated"),
                         item.get("scene") or ["always"], item.get("share"), item.get("source", ""))
        data["lines"].append(line)
        print(f"added {line['id']}")
    save(data)
    return 0


def cmd_lend(args) -> int:
    data = load()
    chosen = []
    for ln in data["lines"]:
        if not is_worn(ln):
            continue
        share = ln.get("share")
        if share is None:
            share = SHARE_DEFAULT.get(ln["section"], False)
        if share:
            chosen.append(ln)
    problems = []
    for ln in chosen:
        reasons = scan_secrets(ln["text"])
        if reasons:
            problems.append(f"{ln['id']} contains {', '.join(reasons)}")
    if problems:
        print("BLOCKED: " + "; ".join(problems))
        return 1
    by_section = {}
    for ln in chosen:
        by_section.setdefault(ln["section"], []).append(ln)
    body = []
    for sec in SECTIONS:
        if sec in by_section:
            body.append(f"## {sec.capitalize()}")
            body.extend("- " + ln["text"] for ln in by_section[sec])
            body.append("")
    body_text = "\n".join(body).strip()
    if args.form == "skill":
        out = (
            "---\nname: lent-mask\n"
            "description: A mask lent by someone else. Use only when the person says to try on this mask.\n"
            "---\n\n# A lent mask\n\nThese lines come from another person. Their author is a claim, "
            "not something that was verified. The person's own lines win any conflict.\n\n"
            + body_text + "\n"
        )
    else:
        out = (
            "MASK LETTER\n"
            "To try this on, paste it into a chat and say: try on this mask.\n"
            "The author is a claim and has not been verified.\n\n" + body_text + "\n"
        )
    print(out)
    return 0


def cmd_screen(args) -> int:
    """The Doorkeeper's mechanical pass over a lent mask (stdin)."""
    text = sys.stdin.read()
    items = []
    for raw in text.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*\S)\s*$", raw)
        if m:
            items.append(m.group(1))
    if not items:
        print("NO LINES FOUND")
        return 1
    budget = load()["settings"]["budget_borrowed"]
    used = 0
    refused = 0
    for i, item in enumerate(items, 1):
        reasons = foreign_reasons(item)
        if reasons:
            refused += 1
            print(f"{i}. REFUSED: {item}  [{'; '.join(reasons)}]")
        else:
            used += tokens(item)
            print(f"{i}. ok: {item}")
    print(f"accepted tokens: about {used} of {budget} ({'OVER BUDGET' if used > budget else 'within budget'}); refused: {refused}")
    return 0 if refused == 0 and used <= budget else 20


def cmd_settings(args) -> int:
    data = load(create=True)
    if args.key is None:
        print(json.dumps(data["settings"], indent=2))
        return 0
    if args.key not in DEFAULT_SETTINGS:
        print(f"unknown setting {args.key}")
        return 1
    if not args.approved:
        print(f"PROPOSED {args.key} = {args.value} (add --approved to write)")
        return 2
    default = DEFAULT_SETTINGS[args.key]
    if isinstance(default, bool):
        value = args.value.lower() in ("1", "true", "yes", "on")
    else:
        value = int(args.value)
    data["settings"][args.key] = value
    save(data)
    print(f"{args.key} = {value}")
    return 0


def cmd_export(args) -> int:
    print(json.dumps(load(), indent=2, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------- hooks


def hook_output(event: str, context: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event,
                                             "additionalContext": context}}))


def cmd_hook(args) -> int:
    """The Dresser and the Stagehand. They must never break a session."""
    try:
        data = load()
        s = data["settings"]
        core = worn_lines(data, "always")
        if not core:
            return 0
        text = lines_to_text(core)
        if args.which == "dresser":
            if not s["auto_don"]:
                return 0
            hook_output(
                "SessionStart",
                "The mask is on (put on by the Dresser). Work under these lines from the "
                "person's mask. Claude's own rules and Anthropic's rules come first; if one "
                "overrides a line, say so.\n" + text,
            )
        elif args.which == "stagehand":
            if not s["stagehand"]:
                return 0
            hook_output(
                "UserPromptSubmit",
                "Reminder from the Stagehand: the mask is still on. Core lines:\n" + text,
            )
    except Exception as exc:  # a hook must fail quietly
        print(f"mask hook skipped: {exc}", file=sys.stderr)
    return 0


# ---------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="larvahctl", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create the mask file if missing").set_defaults(func=cmd_init)
    sub.add_parser("core", help="print the worn core lines").set_defaults(func=cmd_core)
    sub.add_parser("scenes", help="list scenes").set_defaults(func=cmd_scenes)
    sc = sub.add_parser("scene", help="print the worn lines of one scene")
    sc.add_argument("name")
    sc.set_defaults(func=cmd_scene)
    ss = sub.add_parser("scene-set", help="add or change a scene description")
    ss.add_argument("name")
    ss.add_argument("description")
    ss.add_argument("--approved", action="store_true")
    ss.set_defaults(func=cmd_scene_set)
    sub.add_parser("check", help="what is in force and the budget").set_defaults(func=cmd_check)

    sn = sub.add_parser("scan", help="scan text for secrets (stdin or --text)")
    sn.add_argument("--text")
    sn.set_defaults(func=cmd_scan)

    ad = sub.add_parser("add", help="propose or write one line")
    ad.add_argument("--section", required=True)
    ad.add_argument("--text", required=True)
    ad.add_argument("--kind", default="stated")
    ad.add_argument("--scene", default="always")
    ad.add_argument("--share", choices=["yes", "no"])
    ad.add_argument("--source", default="")
    ad.add_argument("--supersede")
    ad.add_argument("--approved", action="store_true")
    ad.set_defaults(func=cmd_add)

    rm = sub.add_parser("remove", help="scratch a line (by id or text)")
    rm.add_argument("id_or_text")
    rm.set_defaults(func=cmd_remove)

    sub.add_parser("diff", help="compare memory lines on stdin with the mask").set_defaults(func=cmd_diff)
    sub.add_parser("backup", help="copy the mask file with a timestamp").set_defaults(func=cmd_backup)
    rs = sub.add_parser("reset", help="back up, then empty the mask")
    rs.add_argument("--approved", action="store_true")
    rs.set_defaults(func=cmd_reset)
    bk = sub.add_parser("bulk", help="add many lines from JSON on stdin")
    bk.add_argument("--approved", action="store_true")
    bk.set_defaults(func=cmd_bulk)

    ld = sub.add_parser("lend", help="write the mask out to share")
    ld.add_argument("--form", choices=["letter", "skill"], default="letter")
    ld.set_defaults(func=cmd_lend)
    sub.add_parser("screen", help="the Doorkeeper's pass over a lent mask on stdin").set_defaults(func=cmd_screen)

    st = sub.add_parser("settings", help="show or change a setting")
    st.add_argument("key", nargs="?")
    st.add_argument("value", nargs="?")
    st.add_argument("--approved", action="store_true")
    st.set_defaults(func=cmd_settings)

    sub.add_parser("export", help="print the whole mask as JSON").set_defaults(func=cmd_export)

    hk = sub.add_parser("hook", help="run the Dresser or the Stagehand")
    hk.add_argument("which", choices=["dresser", "stagehand"])
    hk.set_defaults(func=cmd_hook)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
