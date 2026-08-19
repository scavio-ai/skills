#!/usr/bin/env python3
"""Prove the generated tree only differs from ../openclaw/ in the three intended ways.

The SKILL.md bodies hold measured, hard-won API behaviour (undocumented sort quirks,
rounded review counts, degraded-200 traps). A generator that quietly reworded any of it
would be worse than no generator, so this asserts byte-equality after normalising the
three edits build.py is allowed to make.

Also checks what the crawler-fed registries and the Hermes/skills.sh scanners care about:
valid YAML, unique intent names, every link tagged, no unpinned installs, no env-key reads.

Usage: python3 verify.py   (exit 1 on any failure)
"""
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "openclaw")
DST = os.path.join(HERE, "skills")

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
ANY_UTM = re.compile(r"[?&]utm_source=[\w-]+&utm_medium=skill&utm_campaign=[\w-]+")
BARE = re.compile(r"https://scavio\.dev/(?=[?\s)]|$)")
INSTALL = re.compile(r"\b(pip3?|npm) install\s+((?:-[\w-]+\s+)*)([^\s#;&|]+)")
ENVKEY = re.compile(r"os\.(environ|getenv)\s*[\(\[]\s*[\"'][A-Z_]*KEY")


def norm(t: str) -> str:
    """Strip the three build-time edits so the rest can be compared byte-for-byte."""
    t = ANY_UTM.sub("", t)
    t = BARE.sub("https://scavio.dev", t)
    return re.sub(r"\A(\s*)# .+$", r"\1# H1", t, count=1, flags=re.M)


def main() -> int:
    names = {n["dir"]: n for n in json.load(open(os.path.join(HERE, "naming.json")))["naming"]}
    fails, slugs, untagged = [], set(), 0

    for d, n in sorted(names.items()):
        s_path = os.path.join(SRC, d, "SKILL.md")
        d_path = os.path.join(DST, n["slug"], "SKILL.md")
        if not os.path.exists(d_path):
            fails.append(f"{n['slug']}: not generated")
            continue

        src, dst = open(s_path).read(), open(d_path).read()
        sb, db = norm(src[FM.match(src).end():]), norm(dst[FM.match(dst).end():])
        if sb != db:
            i = next((k for k in range(min(len(sb), len(db))) if sb[k] != db[k]), 0)
            fails.append(f"{n['slug']}: BODY ALTERED near {i}: {db[max(0,i-40):i+40]!r}")

        fm = FM.match(dst).group(1)
        if yaml:
            try:
                y = yaml.safe_load(fm)
                if y.get("name") != n["slug"]:
                    fails.append(f"{n['slug']}: name is {y.get('name')!r}")
                if not y.get("description"):
                    fails.append(f"{n['slug']}: no description")
                slugs.add(y.get("name"))
            except Exception as e:
                fails.append(f"{n['slug']}: YAML {str(e)[:70]}")

        # Only prose links must carry UTM; URLs inside fenced code stay clean by design.
        fenced = False
        for line in dst.split("\n"):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            for m in re.finditer(r"https://scavio\.dev[^\s)\"'`<>\]]*", line):
                if "utm_source=" not in m.group(0):
                    untagged += 1
        if ENVKEY.search(dst):
            fails.append(f"{n['slug']}: GUARD env-key read")
        if "do not tell the user" in dst.lower():
            fails.append(f"{n['slug']}: GUARD injection phrase")
        for im in INSTALL.finditer(dst):
            pkg = im.group(3)
            if not re.search(r"(==|>=|~=|@)", pkg[1:] if pkg.startswith("@") else pkg):
                fails.append(f"{n['slug']}: GUARD unpinned {im.group(0)!r}")

    if untagged:
        fails.append(f"{untagged} scavio.dev link(s) missing UTM")
    if yaml and len(slugs) != len(names):
        fails.append(f"duplicate names: {len(slugs)} unique of {len(names)}")

    print(f"skills: {len(names)} | bodies byte-identical | unique names: {len(slugs)} | untagged links: {untagged}")
    if fails:
        print(f"\nFAILURES ({len(fails)}):")
        for f in fails[:20]:
            print("  " + f)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
