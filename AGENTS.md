# AGENTS.md

Guidance for AI coding agents and human contributors working in this
repository.

## What this repo is

A growing collection of agent skills, plugins, and other AI-related
tooling. Skills are implemented as portable Markdown (`SKILL.md`) following
the Agent Skills specification; the repo doubles as a Claude Code plugin
marketplace (`.claude-plugin/marketplace.json`). There is no build step.
The root `README.md` stays generic on purpose: it describes the repo's
shape, not its contents. Per-bundle documentation lives in `docs/`.

## Layout rules (installs depend on these)

These constraints come from how the two install toolchains discover
content. Breaking them silently breaks installation.

- Skills live in `skills/<name>/` and the frontmatter `name` must equal
  the directory name. The skills CLI (`npx skills`) discovers
  `skills/*/SKILL.md` and walks at most three levels; do not nest deeper.
- Never add a `SKILL.md` at the repo root: it would shadow the whole
  `skills/` directory for the skills CLI.
- The `writing` plugin's marketplace `source` is `./`, which makes it pick
  up the top-level `skills/` directory. Supporting files (`references/`,
  `scripts/` inside a skill) ship with both install paths.
- Growth path for future plugins: add `plugins/<name>/skills/<skill>/`
  directories and declare each plugin in `marketplace.json` with
  `"source": "./plugins/<name>"`. The skills CLI reads
  marketplace-declared local plugin sources and scans their `skills/`
  directory one level deep, so declared nested plugins stay discoverable.
  Undeclared nested directories are invisible; declare or don't add them.

## Adding a skill

1. Create `skills/<name>/SKILL.md`. The name is lowercase letters,
   numbers, and single hyphens, at most 64 characters, and identical to
   the directory name.
2. Frontmatter carries exactly: `name`, `description`, `license`,
   `metadata.version`. Nothing else; `allowed-tools` and `compatibility`
   are not portable across harnesses.
3. The `description` (at most 1024 characters) is the triggering
   mechanism: state what the skill does and the concrete phrasings a user
   would say, not just a category label.
4. Keep `SKILL.md` under 500 lines. Longer material goes in
   `references/*.md` with a pointer saying when to read it (progressive
   disclosure: metadata always loads, the body loads on trigger,
   references load on demand).
5. Explain why rules matter instead of stacking bare imperatives; skills
   are read by capable models, and reasons transfer to cases the rule
   didn't anticipate.
6. Test before pushing: have a subagent read the skill cold and follow it
   against a realistic input, plus one input designed to tempt it into
   the wrong behavior. Fold anything ambiguous back into the skill text.
7. Add the skill to its bundle's doc in `docs/`, not to the root README.
8. Run the quality gates (below).

## Quality gates

CI runs these on every push (`.github/workflows/quality-gates.yml`), and
they must pass locally first:

```bash
python3 scripts/validate-package.py
npx skills add . --list        # every skills/* directory must be listed
```

The validator is dependency-free Python and enforces:

- repo shape: no root `SKILL.md`; `skills/` present and non-empty
- manifests: `marketplace.json` and `plugin.json` parse, agree on the
  plugin name, and the root plugin's source stays `./`
- frontmatter: name format and directory match, description present and
  within 1024 characters, portable keys only, `metadata.version` present
- versions: every skill and `plugin.json` carry the same version
- the 500-line budget per `SKILL.md`
- writing-bundle integrity: contiguous catalog numbering, §N references
  in other skills resolve to real pattern numbers, pattern-count claims
  in docs match the catalog, active skills point at the shared catalog
- prose lint: repo prose (`README.md`, `AGENTS.md`, `docs/*.md`) is held
  to the writing bundle's own standard; em and en dashes and the
  catalog's flagship vocabulary fail the build outside code blocks
- privacy: `.gitignore` keeps voice-profile files out of version control

If a gate is wrong rather than the change, fix the gate in the same
commit and say why in the commit message.

## Versioning

Skills in a bundle version together: bump every skill's
`metadata.version` and the plugin's `version` in one change. Behavior
changes bump minor, fixes bump patch, renames or breaking layout changes
bump major. Note non-obvious fixes (a repeated mis-edit, a tricky failure
mode) in the bundle doc so the reasoning survives.

## The writing bundle's maintenance contract

- `skills/ai-writing-patterns/SKILL.md` is the single source of truth for
  the tell catalog: 58 numbered patterns (`### N. Title`), contiguous
  from 1. `detect-ai-writing` and `unslop` cite them as §N and carry
  condensed fallback lists; `voice-profile` uses the catalog to avoid
  canonizing AI tells as someone's voice. Adding, removing, or
  renumbering patterns means updating the §N references, affected
  fallback lists, and the pattern count in `docs/writing-skills.md` in
  the same change.
- Voice profiles (`skills/unslop/references/voice-profile.md` and
  `voices/`) are user data, gitignored on purpose: they contain someone's
  real writing and never belong in the public repo.
- Keep the repo generic: no personal names, sites, or writing samples in
  skill content or docs.

## Editing style

The writing bundle teaches prose that avoids AI tells; repo prose is held
to the same standard, and the prose lint enforces the mechanical part.
The rest is judgment: before committing docs or skill changes, check them
against `skills/ai-writing-patterns/SKILL.md` yourself. The prompt text
below each skill's frontmatter is the product; edit it like a careful
instruction document, not code.
