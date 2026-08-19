#!/usr/bin/env python3
"""Regenerate skills/ from the ONE source of truth: ../openclaw/.

CLAUDE.md 5a-3: this repo is generated, never hand-edited, so it cannot drift from the
ClawHub source. Edit ../openclaw/<brand>/SKILL.md, then run this.

What it changes, and nothing else:
  frontmatter  name/description/tags  <- naming.json (intent-first, per CLAUDE.md 7)
  body H1                             <- the intent display title
  every scavio.dev link               <- utm_source=agent-skills, campaign=<intent slug>

The technical body is copied through byte-for-byte otherwise. `verify.py` proves that.

Usage: python3 build.py [--check]    (--check exits 1 if the tree would change)
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "openclaw")
DST = os.path.join(HERE, "skills")
UTM = "utm_source=agent-skills&utm_medium=skill&utm_campaign={slug}"

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
URL = re.compile(r"https://scavio\.dev(?:/[^\s)\"'`<>\]]*)?")
AMBIGUOUS = re.compile(r":\s|^[\[\{&*!|>%@`\"']|#\s")


def set_field(fm: str, key: str, value: str) -> str:
    value = value.replace("\n", " ").strip()
    # A plain YAML scalar cannot contain ": " - quote it or the frontmatter won't parse.
    if AMBIGUOUS.search(value):
        value = '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    pat = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    if not pat.search(fm):
        raise KeyError(f"no '{key}:' in frontmatter")
    return pat.sub(f"{key}: {value}", fm, count=1)


def retag(text: str, slug: str) -> str:
    """Tag prose links only. URLs inside fenced code are left alone so the snippets
    stay clean and copy-pasteable - a curl example is not a backlink."""
    def sub(m):
        u, trail = m.group(0), ""
        while u and u[-1] in ".,;:!?":
            trail, u = u[-1] + trail, u[:-1]
        base, _, query = u.partition("?")
        if base == "https://scavio.dev":
            base += "/"           # bare domain reads better with the slash before ?
        keep = [p for p in query.split("&") if p and not p.startswith("utm_")]
        keep.append(UTM.format(slug=slug))
        return base + "?" + "&".join(keep) + trail

    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append(line)
        else:
            out.append(line if fenced else URL.sub(sub, line))
    return "\n".join(out)


def build(check: bool = False) -> int:
    names = {n["dir"]: n for n in json.load(open(os.path.join(HERE, "naming.json")))["naming"]}
    fmap = {f["dir"]: f for f in json.load(open(os.path.join(HERE, "naming.json")))["frontmatter"]}

    staged, problems = {}, []
    for d in sorted(os.listdir(SRC)):
        p = os.path.join(SRC, d, "SKILL.md")
        if not os.path.exists(p):
            continue
        n, f = names.get(d), fmap.get(d)
        if not n or not f:
            problems.append(f"{d}: missing from naming.json")
            continue

        src = open(p).read()
        m = FM.match(src)
        if not m:
            problems.append(f"{d}: unparseable frontmatter")
            continue
        fm, body = m.group(1), src[m.end():]

        fm = set_field(fm, "name", n["slug"])
        fm = set_field(fm, "description", f["description"])
        fm = set_field(fm, "tags", f["tags"])

        body, k = re.subn(r"\A(\s*)# .+$", lambda mm: f"{mm.group(1)}# {n['display']}",
                          body, count=1, flags=re.M)
        if k != 1:
            problems.append(f"{d}: no H1")
            continue

        staged[n["slug"]] = f"---\n{retag(fm, n['slug'])}\n---\n{retag(body, n['slug'])}"

    if problems:
        print("PROBLEMS:")
        for x in problems:
            print("  " + x)
        return 1

    if check:
        drift = []
        for slug, text in staged.items():
            q = os.path.join(DST, slug, "SKILL.md")
            if not os.path.exists(q) or open(q).read() != text:
                drift.append(slug)
        extra = set(os.listdir(DST)) - set(staged) if os.path.isdir(DST) else set()
        if drift or extra:
            print(f"DRIFT: {len(drift)} changed {sorted(drift)[:5]}, {len(extra)} orphaned {sorted(extra)[:5]}")
            return 1
        print(f"up to date: {len(staged)} skills")
        return 0

    if os.path.isdir(DST):
        shutil.rmtree(DST)
    for slug, text in staged.items():
        os.makedirs(os.path.join(DST, slug), exist_ok=True)
        open(os.path.join(DST, slug, "SKILL.md"), "w").write(text)
    print(f"built {len(staged)} skills into skills/")
    return 0


if __name__ == "__main__":
    sys.exit(build(check="--check" in sys.argv))
