# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

A collection of portable agent skills implemented as Markdown. Each skill
lives in `skills/<name>/SKILL.md`; the repo doubles as a Claude Code plugin
marketplace (`.claude-plugin/marketplace.json`, plugin `writing`, source
`./`). There is no build step.

## Layout rules (load-bearing)

- Skills live in `skills/<name>/` and the frontmatter `name` must equal the
  directory name. The skills CLI (`npx skills`) discovers `skills/*/SKILL.md`
  and walks at most three levels; do not nest deeper.
- Never add a `SKILL.md` at the repo root: it would shadow the whole
  `skills/` directory for the skills CLI.
- The marketplace plugin's `source` must stay `./` so the plugin picks up
  the top-level `skills/` directory. Supporting files (`references/`,
  `scripts/` inside a skill) ship with both install paths.

## The maintenance contract

- `skills/ai-writing-patterns/SKILL.md` is the single source of truth for
  the tell catalog: 58 numbered patterns (`### N. Title`), contiguous from
  1. `detect-ai-writing` and `unslop` reference them as §N and carry
  condensed fallback lists. If you add, remove, or renumber patterns,
  update the §N references in both skills, the fallback lists if affected,
  and the pattern count in `README.md` in the same change.
- Versions: each skill's `metadata.version` and `.claude-plugin/plugin.json`
  `version` are bumped together and must match.
- Keep frontmatter portable: `name`, `description`, `license`,
  `metadata.version` only. No `allowed-tools`, no `compatibility`.
- Keep every `SKILL.md` under 500 lines.
- Run `python3 scripts/validate-package.py` before pushing; it enforces all
  of the above. `npx skills add . --list` should find exactly the skills in
  `skills/`.

## Editing style

The skills teach prose that avoids AI tells; repo prose is held to the same
standard. Before committing README or skill changes, run them against
`skills/ai-writing-patterns/SKILL.md` yourself: no em dashes, no
significance inflation, no filler. The prompt text below each frontmatter
is the product; edit it like a careful instruction document, not code.
