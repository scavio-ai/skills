#!/usr/bin/env python3
"""Prove the generated tree only differs from ../openclaw/ in the three intended ways.

The SKILL.md bodies hold measured, hard-won API behaviour (undocumented sort quirks,
rounded review counts, degraded-200 traps). A generator that quietly reworded any of it
would be worse than no generator, so this asserts byte-equality after normalising the
three edits build.py is allowed to make.

The `scavio` umbrella is held to the same bar: every references/<slug>.md must be the
body of skills/<slug>/SKILL.md byte for byte, its router must link every reference, and
its description must stay short enough to sit in an agent's context at rest.

Also checks what the crawler-fed registries and the Hermes/skills.sh scanners care about:
valid YAML, unique names, every link tagged, no unpinned installs, no env-key reads, and
that this README lists every skill (the 39-vs-50 drift of 2026-09 is how that one got in).

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
UMBRELLA = "scavio"
MAX_UMBRELLA_DESC_WORDS = 250

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


def untagged_links(text: str) -> int:
    """Prose links must carry UTM; URLs inside fenced code stay clean by design."""
    n, fenced = 0, False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for m in re.finditer(r"https://scavio\.dev[^\s)\"'`<>\]]*", line):
            if "utm_source=" not in m.group(0):
                n += 1
    return n


def guard(label: str, text: str, fails: list) -> None:
    """What Hermes skills_guard and the skills.sh scanner reject."""
    if ENVKEY.search(text):
        fails.append(f"{label}: GUARD env-key read")
    if "do not tell the user" in text.lower():
        fails.append(f"{label}: GUARD injection phrase")
    for im in INSTALL.finditer(text):
        pkg = im.group(3)
        if not re.search(r"(==|>=|~=|@)", pkg[1:] if pkg.startswith("@") else pkg):
            fails.append(f"{label}: GUARD unpinned {im.group(0)!r}")


def frontmatter(label: str, text: str, want_name: str, fails: list, slugs: set) -> dict:
    fm = FM.match(text)
    if not fm:
        fails.append(f"{label}: no frontmatter")
        return {}
    if not yaml:
        return {}
    try:
        y = yaml.safe_load(fm.group(1))
    except Exception as e:
        fails.append(f"{label}: YAML {str(e)[:70]}")
        return {}
    if y.get("name") != want_name:
        fails.append(f"{label}: name is {y.get('name')!r}")
    if not y.get("description"):
        fails.append(f"{label}: no description")
    slugs.add(y.get("name"))
    return y


def main() -> int:
    cfg = json.load(open(os.path.join(HERE, "naming.json")))
    names = {n["dir"]: n for n in cfg["naming"]}
    readme = open(os.path.join(HERE, "README.md")).read()
    fails, slugs, untagged = [], set(), 0

    generated = {}
    for d, n in sorted(names.items()):
        s_path = os.path.join(SRC, d, "SKILL.md")
        d_path = os.path.join(DST, n["slug"], "SKILL.md")
        if not os.path.exists(d_path):
            fails.append(f"{n['slug']}: not generated")
            continue

        src, dst = open(s_path).read(), open(d_path).read()
        generated[n["slug"]] = dst
        sb, db = norm(src[FM.match(src).end():]), norm(dst[FM.match(dst).end():])
        if sb != db:
            i = next((k for k in range(min(len(sb), len(db))) if sb[k] != db[k]), 0)
            fails.append(f"{n['slug']}: BODY ALTERED near {i}: {db[max(0,i-40):i+40]!r}")

        frontmatter(n["slug"], dst, n["slug"], fails, slugs)
        untagged += untagged_links(dst)
        guard(n["slug"], dst, fails)
        if f"`{n['slug']}`" not in readme:
            fails.append(f"{n['slug']}: not listed in README.md")

    # The umbrella: router + one reference per generated skill, nothing else.
    u_dir = os.path.join(DST, UMBRELLA)
    u_path = os.path.join(u_dir, "SKILL.md")
    if not os.path.exists(u_path):
        fails.append(f"{UMBRELLA}: not generated")
    else:
        u = open(u_path).read()
        y = frontmatter(UMBRELLA, u, UMBRELLA, fails, slugs)
        words = len(str(y.get("description", "")).split())
        if words > MAX_UMBRELLA_DESC_WORDS:
            fails.append(f"{UMBRELLA}: description is {words} words (max {MAX_UMBRELLA_DESC_WORDS})")
        untagged += untagged_links(u)
        guard(UMBRELLA, u, fails)
        if f"`{UMBRELLA}`" not in readme:
            fails.append(f"{UMBRELLA}: not listed in README.md")

        ref_dir = os.path.join(u_dir, "references")
        have = set(os.listdir(ref_dir)) if os.path.isdir(ref_dir) else set()
        for slug, skill in generated.items():
            ref = f"{slug}.md"
            if f"(references/{ref})" not in u:
                fails.append(f"{UMBRELLA}: router does not link references/{ref}")
            if ref not in have:
                fails.append(f"{UMBRELLA}: missing references/{ref}")
                continue
            want = skill[FM.match(skill).end():].lstrip("\n")
            if open(os.path.join(ref_dir, ref)).read() != want:
                fails.append(f"{UMBRELLA}: references/{ref} differs from skills/{slug}/SKILL.md body")
        for extra in sorted(have - {f"{s}.md" for s in generated}):
            fails.append(f"{UMBRELLA}: orphan references/{extra}")
        # Hermes skills_guard rejects a community skill with more than 50 files. The
        # umbrella is 1 + one reference per platform, so it crosses that line at 50
        # platforms and Hermes users are pointed at the per-platform skills instead
        # (README, "Umbrella or per-platform"). Reported, not failed, so the count is
        # visible whenever the tree is rebuilt.
        print(f"{UMBRELLA}: {1 + len(have)} files (Hermes cap 50; per-platform skills are the Hermes path)")

    if untagged:
        fails.append(f"{untagged} scavio.dev link(s) missing UTM")
    if yaml and len(slugs) != len(names) + 1:
        fails.append(f"duplicate names: {len(slugs)} unique of {len(names) + 1}")

    print(f"skills: {len(names)} + {UMBRELLA} | bodies byte-identical | unique names: {len(slugs)} | untagged links: {untagged}")
    if fails:
        print(f"\nFAILURES ({len(fails)}):")
        for f in fails[:20]:
            print("  " + f)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
