# gio-skills

[![skills.sh installs](https://skills.sh/b/gscalzo/gio-skills)](https://skills.sh/gscalzo/gio-skills)

Giordano Scalzo's agent skills. Plain Markdown, portable across any harness
that reads Agent Skills (`SKILL.md`), installable with the skills CLI or as
a Claude Code plugin.

## Skills

| Skill | What it does |
|---|---|
| `unslop` | Rewrites AI-generated prose so it reads as natural human writing. No invented facts, voice calibration from samples, draft → audit → final loop. |
| `detect-ai-writing` | Analyzes text for AI fingerprints and reports a calibrated verdict with quoted evidence, counter-evidence, and false-positive guards. |
| `ai-writing-patterns` | The shared reference catalog both skills load: 58 numbered patterns across vocabulary, rhetoric, tone, structure, formatting, and near-proof fingerprints, plus the research behind them. |

The two active skills lean on the catalog as their single source of truth,
so a pattern added there is picked up by both. The catalog's
`references/research.md` collects the empirical studies (word-frequency
measurements, detector false-positive rates, what actually makes prose read
human) for when someone asks "says who?".

## Installation

### Skills CLI

```bash
npx skills add gscalzo/gio-skills
```

Install globally so the skills are available in every project:

```bash
npx skills add gscalzo/gio-skills --global
```

Pick a single skill:

```bash
npx skills add gscalzo/gio-skills --skill unslop
```

### Claude Code plugin

```
/plugin marketplace add gscalzo/gio-skills
/plugin install writing@gio-skills
```

Skills are then invoked as `/writing:unslop`, `/writing:detect-ai-writing`
and `/writing:ai-writing-patterns`.

### Manual

Copy any skill directory into wherever your harness expects skills:

```bash
git clone https://github.com/gscalzo/gio-skills.git
cp -r gio-skills/skills/unslop /path/to/your/skills/
```

`unslop` and `detect-ai-writing` look for the catalog at
`../ai-writing-patterns/SKILL.md`, so install the three together to get the
full pattern set. Each works standalone through a condensed fallback list.

## Usage

Unslop pasted text or a file:

```
/unslop

[paste your draft]
```

```
Humanize the prose in content/blog/my-post.md
```

Check a text for AI tells:

```
Does this read as AI-written? [paste text]
```

Match your own voice by pasting a sample first, or permanently by adding a
`references/voice-profile.md` inside the `unslop` skill directory (see
`skills/unslop/references/README.md`).

## What these skills will not do

They edit and they detect; they do not evade. No fake typos, no fabricated
anecdotes, no detector-tricking noise, and the detector never presents a
verdict as proof or grounds for punishment. The goal is writing a careful
human would stand behind under their own name.

## Credits and sources

The catalog merges and deduplicates, with attribution:

- [blader/humanizer](https://github.com/blader/humanizer) (MIT), itself
  built from Wikipedia's
  [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
- [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill)
- [gregorymm/humanize-text](https://github.com/gregorymm/humanize-text)
- [tropes.fyi](https://tropes.fyi)

Research citations live in
`skills/ai-writing-patterns/references/research.md`.

## Validation

```bash
python3 scripts/validate-package.py
npx skills add . --list
```

## License

MIT
