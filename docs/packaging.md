# Packaging: how this repo serves two toolchains

Why the layout looks the way it does, and what each install toolchain
actually does. Sources: the `vercel-labs/skills` CLI source code and
README, the Agent Skills specification (agentskills.io), the Claude Code
plugin docs (code.claude.com/docs), and probes run against the real CLI
while designing this repo.

## The skills CLI (`npx skills`)

Discovery rules, verified against the CLI's source and by direct testing:

- A `SKILL.md` at the repo root is treated as the repo's single skill and
  shadows everything else. A multi-skill repo must not have one.
- The `skills/` directory is a first-class container, walked up to three
  levels deep, so `skills/<name>/SKILL.md` and category layouts like
  `skills/<category>/<name>/SKILL.md` both work. Walking stops below a
  discovered skill.
- The repo root itself is scanned one level deep, so
  `<name>/SKILL.md` at top level is also found (the anthropics/skills
  layout).
- Directories like `.claude/skills/` and arbitrary nested paths are
  checked only as agent-specific containers or through a fallback
  recursive search that runs when nothing was found in standard places.
  Do not rely on the fallback.
- If `.claude-plugin/marketplace.json` exists, plugins with a local
  `source` (starting with `./`) get their `skills/` directory scanned one
  level deep as well. This is what keeps the `plugins/<name>/`
  layout discoverable, provided each plugin is declared in the
  marketplace manifest.
- Skills are deduplicated by frontmatter `name`; first discovered wins.
- The CLI requires only `name` and `description` in frontmatter; a skill
  missing either is skipped with a warning.
- On install, the whole skill directory is copied (or symlinked to a
  canonical copy under `.agents/skills/`), including `references/` and
  `scripts/`. Sibling relative paths like `../ai-writing-patterns/`
  survive when skills are installed together.
- Listing on skills.sh needs no submission: public repos surface through
  the CLI's install telemetry, and repo pages live at
  `skills.sh/<owner>/<repo>`.

## Claude Code plugins

- `.claude-plugin/marketplace.json` at the repo root declares the
  marketplace: `name`, `owner`, and a `plugins` array. Each plugin entry
  needs `name` and `source`; a relative source must start with `./` and
  resolves against the repo root.
- A plugin's skills load by default from the `skills/` directory under
  its source, so `"source": "./"` picks up the top-level `skills/`
  directory. A `skills` field with explicit paths adds to that scan; the
  documented pattern for several plugins sharing one root is to list each
  plugin's subdirectories explicitly.
- `plugin.json` is optional; when present it carries the version and
  package metadata. Skills are invoked as `/<plugin>:<skill>`.
- Installed plugins are copied to a cache, so a plugin cannot reference
  files outside its own directory.

## Spec constraints every skill here follows

From the Agent Skills specification:

| Field | Constraint |
|---|---|
| `name` | Required. Max 64 chars, lowercase letters, digits, single hyphens, must equal the directory name. |
| `description` | Required. Non-empty, max 1024 chars; it is the trigger mechanism. |
| `license` | Optional. |
| `metadata` | Optional string-to-string map; the version lives at `metadata.version`. |
| `compatibility`, `allowed-tools` | Legal per spec but not portable across harnesses; this repo forbids them. |

Keep `SKILL.md` under 500 lines; move depth into `references/` files that
load on demand.

## Why this repo's layout

One copy of each skill has to serve both toolchains. The layout has two
parts. The root plugin (`writing`) keeps its skills in root `skills/`, with
its marketplace entry rooted at `./`. Every other bundle is a nested plugin
under `plugins/<name>/` with its own `.claude-plugin/plugin.json` and
`skills/` directory, declared in the marketplace with
`"source": "./plugins/<name>"`. `apple-apps` is the current example. Both
parts are discovered first-class: the skills CLI scans root `skills/` and
the `skills/` directory of each declared local plugin source.

Probes against the real CLI confirmed the failure modes this avoids: a
root `SKILL.md` hides the whole `skills/` directory, and nested paths with
no marketplace declaration are invisible. A new skill therefore goes in
the `skills/` directory of the bundle it belongs to and versions with that
bundle.

`scripts/validate-package.py` encodes all of this, including a failure for
any `plugins/<name>/` directory with no matching marketplace entry. CI runs
it plus a discovery check (root and nested bundles) and plugin validation
on every push.
