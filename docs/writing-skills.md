# The writing bundle

Skills for working with AI-generated prose, installable together as the
`writing` plugin.

| Skill | What it does |
|---|---|
| `unslop` | Rewrites AI-generated prose so it reads as natural human writing. No invented facts, voice calibration from samples or saved profiles, draft, audit, final loop. |
| `detect-ai-writing` | Analyzes text for AI fingerprints and reports a calibrated verdict with quoted evidence, counter-evidence, and false-positive guards. |
| `voice-profile` | Builds reusable voice profiles from samples of someone's real writing, so rewrites sound like a specific author, brand, or team instead of a generic clean editor. |
| `ai-writing-patterns` | The shared reference catalog the others load: 58 numbered patterns across vocabulary, rhetoric, tone, structure, formatting, and near-proof fingerprints, plus the research behind them. |

The active skills lean on the catalog as their single source of truth, so a
pattern added there is picked up everywhere. The catalog's
`references/research.md` collects the empirical studies (word-frequency
measurements, detector false-positive rates, what actually makes prose read
human) for when someone asks "says who?".

The skills look for each other by relative path (`../ai-writing-patterns`
for the catalog, `../unslop` for saved voices), so install them together to
get the full behavior. `unslop` and `detect-ai-writing` also work standalone
through a condensed fallback list.

The detector's method adapts the published techniques of the two serious
commercial detectors: GPTZero (predictability and burstiness scoring,
sentence-level classification into human, mixed, and AI, tuned confidence
bands) and Pangram (mirror comparison against a default LLM's answer to
the same brief, decode thresholds, mixed-authorship smoothing, humanizer
detection). `unslop` applies the same findings in reverse: structure and
rhythm beat word swaps, and evasion noise is treated as a defect, not a
technique. The detector-internals section of the catalog's
`references/research.md` documents what was borrowed and from where.

## Usage

Unslop pasted text or a file:

```
/unslop

[paste your draft]
```

```
Humanize the prose in content/posts/my-post.md
```

Check a text for AI tells:

```
Does this read as AI-written? [paste text]
```

## Voices

Match a specific voice by pasting a writing sample into the conversation,
or permanently with a saved profile:

```
Create a voice profile from these three posts: [paste or point at files]
```

The `voice-profile` skill analyzes the samples (rhythm, punctuation,
lexicon, temperament) and saves the profile where `unslop` reads it
automatically: `references/voice-profile.md` for the default voice, or
`references/voices/<name>.md` for named voices you can ask for by name
("rewrite this in the blog voice"). See
`../skills/unslop/references/README.md` for the format.

Voice profiles contain real writing. The repo's `.gitignore` keeps them out
of version control; keep personal profiles in a local or globally installed
copy of the skills.

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
`../skills/ai-writing-patterns/references/research.md`, which also covers
detector internals (GPTZero, Pangram), community tooling heuristics, and
the version-diff provenance method for when a draft and a final version
are both available. How the repo serves both install toolchains is
documented in `packaging.md`.
