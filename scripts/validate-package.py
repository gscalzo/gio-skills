#!/usr/bin/env python3
"""Validate gio-skills package surfaces without external dependencies.

The repo's quality gate. Enforces:
- repo shape (no root SKILL.md; skills/ present and populated)
- manifest sanity (marketplace.json / plugin.json parse and agree)
- portable frontmatter per skill (name/description constraints, version)
- the 500-line SKILL.md budget
- writing-bundle integrity (catalog numbering, resolvable paragraph-sign
  references, pattern-count claims, shared-catalog pointers)
- prose lint on repo docs (the bundle's own standard, applied to itself)
- privacy (.gitignore keeps voice profiles out of version control)

Run from anywhere: python3 scripts/validate-package.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATALOG = "ai-writing-patterns"
CATALOG_CONSUMERS = {"detect-ai-writing", "unslop"}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


# --- Repo shape -------------------------------------------------------------

if (ROOT / "SKILL.md").exists():
    fail(
        "A root-level SKILL.md shadows the skills/ directory for the skills CLI "
        "(npx skills finds only the root file). Remove it."
    )

if not SKILLS_DIR.is_dir():
    print("skills/ directory is missing", file=sys.stderr)
    sys.exit(1)

skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
if not skill_dirs:
    fail("skills/ contains no skill directories")

# --- Plugin manifests -------------------------------------------------------

try:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
except (OSError, json.JSONDecodeError) as exc:
    plugin = {}
    fail(f".claude-plugin/plugin.json unreadable: {exc}")

try:
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
except (OSError, json.JSONDecodeError) as exc:
    marketplace = {}
    fail(f".claude-plugin/marketplace.json unreadable: {exc}")

if plugin and marketplace:
    listed = {entry.get("name") for entry in marketplace.get("plugins", [])}
    if plugin.get("name") not in listed:
        fail(
            f"plugin.json name {plugin.get('name')!r} is not listed in "
            f"marketplace.json plugins {sorted(listed)}"
        )
    for entry in marketplace.get("plugins", []):
        if entry.get("name") == plugin.get("name") and entry.get("source") != "./":
            fail(
                "the root plugin's marketplace source must be './' so the "
                "plugin picks up the top-level skills/ directory"
            )

plugin_version = str(plugin.get("version", ""))

# --- Individual skills ------------------------------------------------------

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
NAME_FORMAT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
versions: dict[str, str] = {}
skill_texts: dict[str, str] = {}


def extract_description(frontmatter: str) -> str | None:
    """Return the description value, handling both inline and block scalars."""
    lines = frontmatter.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^description:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value not in ("|", ">", "|-", ">-"):
            return value
        block: list[str] = []
        for continuation in lines[i + 1 :]:
            if continuation.strip() == "" or continuation.startswith((" ", "\t")):
                block.append(continuation.strip())
            else:
                break
        return " ".join(part for part in block if part)
    return None


for skill_dir in skill_dirs:
    name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        fail(f"{name}: missing SKILL.md")
        continue
    text = skill_path.read_text()
    skill_texts[name] = text

    match = FRONTMATTER.match(text)
    if not match:
        fail(f"{name}: SKILL.md must start with YAML frontmatter")
        continue
    frontmatter = match.group(1)

    declared = re.search(r"(?m)^name:\s*(\S+)\s*$", frontmatter)
    if not declared:
        fail(f"{name}: frontmatter has no name field")
    elif declared.group(1) != name:
        fail(f"{name}: frontmatter name {declared.group(1)!r} != directory name")
    if not NAME_FORMAT.match(name) or len(name) > 64:
        fail(
            f"{name}: skill names are lowercase letters, digits, and single "
            "hyphens, at most 64 characters"
        )

    description = extract_description(frontmatter)
    if not description:
        fail(f"{name}: frontmatter has no (or an empty) description field")
    elif len(description) > 1024:
        fail(f"{name}: description is {len(description)} chars; the spec caps it at 1024")

    for nonportable in ("compatibility:", "allowed-tools:"):
        if re.search(rf"(?m)^{re.escape(nonportable)}", frontmatter):
            fail(f"{name}: remove nonportable frontmatter key {nonportable[:-1]}")

    version = re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', frontmatter)
    if version:
        versions[name] = version.group(1)
    else:
        fail(f"{name}: metadata.version is missing")

    if len(text.splitlines()) > 500:
        fail(f"{name}: SKILL.md exceeds the 500-line portability budget")

    if name in CATALOG_CONSUMERS and f"../{CATALOG}/SKILL.md" not in text:
        fail(f"{name}: must point at the shared catalog via ../{CATALOG}/SKILL.md")

# --- Version agreement ------------------------------------------------------

all_versions = set(versions.values()) | ({plugin_version} if plugin_version else set())
if len(all_versions) > 1:
    fail(
        f"version mismatch across package: {versions}, plugin.json={plugin_version!r}"
    )

# --- Catalog integrity ------------------------------------------------------

DOC_FILES = [ROOT / "README.md", ROOT / "AGENTS.md", *sorted((ROOT / "docs").glob("*.md"))]

catalog_text = skill_texts.get(CATALOG, "")
if catalog_text:
    numbers = [int(n) for n in re.findall(r"(?m)^### ([0-9]+)\. ", catalog_text)]
    if numbers != list(range(1, len(numbers) + 1)):
        fail(f"{CATALOG}: pattern numbering is not contiguous from 1: {numbers}")
    max_pattern = len(numbers)

    for name, text in skill_texts.items():
        if name == CATALOG:
            continue
        for start, end in re.findall(r"§(\d+)(?:-(\d+))?", text):
            for ref in filter(None, (start, end)):
                if not 1 <= int(ref) <= max_pattern:
                    fail(
                        f"{name}: reference to pattern {ref} does not resolve "
                        f"(catalog has 1-{max_pattern})"
                    )

    count_claims: set[int] = set()
    claim_sources = [t for n, t in skill_texts.items()] + [
        p.read_text() for p in DOC_FILES if p.exists()
    ]
    for source in claim_sources:
        for claim in re.findall(r"\b([0-9]{2,3}) (?:numbered )?patterns\b", source):
            count_claims.add(int(claim))
    if numbers and count_claims and count_claims != {max_pattern}:
        fail(
            f"pattern-count claims {sorted(count_claims)} disagree with the "
            f"catalog's {max_pattern} numbered patterns"
        )
elif CATALOG not in skill_texts:
    fail(f"the shared catalog skill {CATALOG} is missing")

# --- Prose lint on repo docs ------------------------------------------------

FENCE = re.compile(r"^(```|~~~)")
PROSE_BANS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"—"), "em dash"),
    (re.compile(r"–"), "en dash"),
    (re.compile(r"\bdelve", re.IGNORECASE), "catalog vocabulary: delve"),
    (re.compile(r"\btapestry\b", re.IGNORECASE), "catalog vocabulary: tapestry"),
    (re.compile(r"\btestament to\b", re.IGNORECASE), "catalog vocabulary: testament to"),
    (re.compile(r"\bIn today's\b", re.IGNORECASE), "catalog opener: In today's"),
    (re.compile(r"\bLet's dive\b", re.IGNORECASE), "catalog signposting: Let's dive"),
    (re.compile(r"\bit's worth noting\b", re.IGNORECASE), "catalog filler: it's worth noting"),
    (re.compile(r"\bload[- ]bearing\b", re.IGNORECASE), "banned phrase: load-bearing"),
]

for doc in DOC_FILES:
    if not doc.exists():
        continue
    in_fence = False
    for lineno, line in enumerate(doc.read_text().splitlines(), start=1):
        if FENCE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for pattern, label in PROSE_BANS:
            if pattern.search(line):
                fail(f"{doc.relative_to(ROOT)}:{lineno}: prose lint: {label}")

# --- Privacy ----------------------------------------------------------------

gitignore = ROOT / ".gitignore"
if not gitignore.exists():
    fail(".gitignore is missing (it must exclude voice profiles)")
else:
    ignored = gitignore.read_text()
    for required in ("skills/unslop/references/voice-profile.md", "skills/unslop/references/voices/"):
        if required not in ignored:
            fail(f".gitignore no longer excludes {required}")

tracked_profiles = [
    p
    for p in (SKILLS_DIR / "unslop" / "references").glob("voice*")
    if p.name not in ("README.md",) and not p.is_dir()
]
profile_dir = SKILLS_DIR / "unslop" / "references" / "voices"
if profile_dir.exists() and any(profile_dir.iterdir()):
    fail("skills/unslop/references/voices/ contains files; profiles must stay local")
if tracked_profiles:
    fail(f"voice profile files present in the repo: {[str(p) for p in tracked_profiles]}")

# --- Result -----------------------------------------------------------------

if errors:
    for message in errors:
        print(f"FAIL {message}", file=sys.stderr)
    sys.exit(1)

label = ", ".join(f"{name} v{versions[name]}" for name in sorted(versions))
print(f"gio-skills package is valid ({label})")
