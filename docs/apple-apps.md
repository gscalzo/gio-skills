# The apple-apps bundle

Skills for starting and running native Apple apps (macOS, iPadOS, iOS) that
coding agents write most of the code for. Installable as the `apple-apps`
plugin.

| Skill | What it does |
|---|---|
| `apple-app-blueprint` | A set of decisions that worked together on an agent-built Mac app: project shape, a headless core with a CLI, local quality gates enforced by the agent's Stop hook, agent roles by model tier, a verification skill with a feature map, agent-readable code rules, and a one-command install of the latest build. |

## Layout

The bundle lives under `plugins/apple-apps/` and is declared in the
marketplace with `"source": "./plugins/apple-apps"`. The skills CLI finds it
through that declaration. See `packaging.md` for why undeclared nested
directories are invisible.

The skill keeps `SKILL.md` short and moves depth into `references/`:
architecture, quality gates, verification, agent workflow, skills, and
kickoff questions. Each reference loads on demand.

## Usage

```
Plan a new Mac app with the Apple app blueprint
```

```
Set up quality gates for my Swift project
```

The blueprint is opinionated. Treat it as a starting position to argue with,
and ask the agent to grill you on the kickoff questions before building.

## Versioning

The bundle versions on its own track: the skill's `metadata.version` and the
plugin's `version` move together, independent of the `writing` bundle.
