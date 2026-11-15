# gio-skills

[![skills.sh installs](https://skills.sh/b/gscalzo/gio-skills)](https://skills.sh/gscalzo/gio-skills)
[![quality gates](https://github.com/gscalzo/gio-skills/actions/workflows/quality-gates.yml/badge.svg)](https://github.com/gscalzo/gio-skills/actions/workflows/quality-gates.yml)

A collection of agent skills, plugins, and other AI-related tooling. Skills
are plain Markdown following the
[Agent Skills specification](https://agentskills.io), portable across any
harness that reads `SKILL.md`, and installable with the skills CLI or as
Claude Code plugins.

## Layout

```
skills/<name>/          the root plugin's (writing) skills: SKILL.md plus
                        optional references/, scripts/, assets/
plugins/<name>/         other bundles, each with .claude-plugin/plugin.json
                        and skills/<skill>/ (for example apple-apps)
.claude-plugin/         marketplace manifest and the root plugin manifest
docs/<bundle>.md        usage guide per bundle
scripts/                validation and tooling
```

Skills describe themselves: every `skills/<name>/SKILL.md` states what the
skill does and when to use it, and each bundle has a guide under `docs/`.
To see what is currently available:

```bash
npx skills add gscalzo/gio-skills --list
```

## Installation

Everything, with the skills CLI:

```bash
npx skills add gscalzo/gio-skills          # project-local
npx skills add gscalzo/gio-skills --global # every project
npx skills add gscalzo/gio-skills --skill <name>
```

As a Claude Code plugin:

```
/plugin marketplace add gscalzo/gio-skills
/plugin install <plugin>@gio-skills
```

Installing everything also installs the `apple-apps` bundle alongside the
writing skills; pick single skills with `--skill <name>`.

Plugin skills are invoked as `/<plugin>:<skill>`. Manual installs also
work: copy a skill directory into wherever your harness expects skills.
Some skills reference sibling skills by relative path, so prefer installing
a bundle together; each bundle's doc says what belongs with what.

## Quality gates

Every push runs the gates in CI, and they are expected to pass locally
before committing:

```bash
python3 scripts/validate-package.py   # structure, frontmatter, versions,
                                      # cross-references, prose lint
npx skills add . --list               # every skill is discoverable
```

`scripts/validate-package.py` is dependency-free Python; see `AGENTS.md`
for what it enforces and for the contribution checklist.

## License

MIT
