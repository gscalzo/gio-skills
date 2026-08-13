#!/usr/bin/env python3
"""Validate gio-skills package surfaces without external dependencies.

Checks that every skill under skills/ is a portable Agent Skill, that the
Claude Code plugin manifests parse and agree with each other, and that the
cross-references between the skills hold (the detector and humanizer both
lean on the shared ai-writing-patterns catalog).

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
versions: dict[str, str] = {}

for skill_dir in skill_dirs:
    name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        fail(f"{name}: missing SKILL.md")
        continue
    text = skill_path.read_text()

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

    if not re.search(r"(?m)^description:", frontmatter):
        fail(f"{name}: frontmatter has no description field")

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

    if name != CATALOG and f"../{CATALOG}/SKILL.md" not in text:
        fail(f"{name}: must point at the shared catalog via ../{CATALOG}/SKILL.md")

# --- Version agreement ------------------------------------------------------

all_versions = set(versions.values()) | ({plugin_version} if plugin_version else set())
if len(all_versions) > 1:
    fail(f"version mismatch across package: { {k: v for k, v in versions.items()} }, plugin.json={plugin_version!r}")

# --- Catalog integrity ------------------------------------------------------

catalog_path = SKILLS_DIR / CATALOG / "SKILL.md"
if catalog_path.exists():
    catalog_text = catalog_path.read_text()
    numbers = [int(n) for n in re.findall(r"(?m)^### ([0-9]+)\. ", catalog_text)]
    if numbers != list(range(1, len(numbers) + 1)):
        fail(f"{CATALOG}: pattern numbering is not contiguous from 1: {numbers}")
    count_claims = {
        int(n) for n in re.findall(r"\b([0-9]{2,3}) (?:numbered )?patterns\b", catalog_text)
    }
    for other in skill_dirs:
        other_path = other / "SKILL.md"
        if other.name == CATALOG or not other_path.exists():
            continue
        for claim in re.findall(r"\b([0-9]{2,3}) (?:numbered )?patterns\b", other_path.read_text()):
            count_claims.add(int(claim))
    readme = ROOT / "README.md"
    if readme.exists():
        for claim in re.findall(r"\b([0-9]{2,3}) (?:numbered )?patterns\b", readme.read_text()):
            count_claims.add(int(claim))
    if numbers and count_claims and count_claims != {len(numbers)}:
        fail(
            f"pattern-count claims {sorted(count_claims)} disagree with the "
            f"catalog's {len(numbers)} numbered patterns"
        )

# --- Result -----------------------------------------------------------------

if errors:
    for message in errors:
        print(f"FAIL {message}", file=sys.stderr)
    sys.exit(1)

label = ", ".join(f"{name} v{versions[name]}" for name in sorted(versions))
print(f"gio-skills package is valid ({label})")
