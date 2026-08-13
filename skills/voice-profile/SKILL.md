---
name: voice-profile
description: |
  Build or update a writing voice profile from samples of someone's real
  writing, so the unslop skill (and any writing task) can match that voice
  automatically. Use when the user asks to create a voice profile, capture
  or learn their writing style, make rewrites "sound like me", set up a
  brand or team voice, add a named voice (blog voice, newsletter voice,
  corporate voice), or update an existing profile with new samples.
license: MIT
metadata:
  version: "1.1.0"
---

# Voice profile: capture how a person actually writes

You are building a reusable description of a writer's voice from their real
writing. The output is a Markdown profile file that other skills (chiefly
`unslop`, installed beside this skill) read as a standing writing sample.

## Gather samples

Ask for, or collect from files the user points at, samples of the writing
the profile should capture. What makes samples useful:

- **Their own words.** Unedited drafts and published pieces they wrote
  themselves. Not text an AI helped with, not text an editor rewrote.
- **One register per profile.** Blog posts and corporate reports belong in
  different profiles. If the samples mix registers, offer to build named
  voices instead of averaging them into mush.
- **Enough of it.** Aim for at least 500 words across two or more pieces;
  below that, say the profile will be rough and offer to proceed anyway.

Check the samples against `../ai-writing-patterns/SKILL.md` before
distilling. If they are saturated with catalog tells, the "voice" you are
about to capture may be a chatbot's; tell the user what you found and ask
whether those habits are genuinely theirs. A deliberate quirk stays in the
profile (a writer who truly loves em dashes keeps them); a tell that
leaked in from AI-assisted drafting should not be canonized.

## Analyze

Read the samples and note, with examples from the text:

1. **Rhythm.** Sentence-length mix (how short do they go, how long, how
   often), paragraph sizes, use of fragments and one-line paragraphs.
2. **Punctuation habits.** Em dashes or not, parentheses, semicolons,
   colons, exclamation marks, Oxford comma, curly or straight quotes.
3. **Lexicon.** Recurring words and phrases; register (contractions?
   profanity? jargon?); words this writer would never use.
4. **Constructions.** How they open pieces and paragraphs, how they close,
   how they handle transitions, first or third person, how they hedge or
   commit, how they address the reader.
5. **Temperament.** Humor, asides, self-deprecation, bluntness,
   enthusiasm, understatement — with a quote showing each claimed trait.

## Write the profile

Use this structure:

```markdown
# Voice profile: <name or "default">

Built <date> from <N> samples (<what they were>).

## Samples

<2-4 representative excerpts, verbatim, 100-200 words each>

## Distilled habits

- Rhythm: ...
- Punctuation: ...
- Lexicon: ...
- Constructions: ...
- Temperament: ...

## Never

<words, moves, and tones this writer avoids>
```

Samples outrank the distilled notes on any disagreement, and the profile
says so implicitly by leading with them. Do not pad the distillation:
five sharp observations beat twenty generic ones. "Varies sentence
length" is true of every good writer; "opens most paragraphs mid-thought,
as if resuming a conversation" is a voice.

## Save it

The `unslop` skill looks for profiles inside its own directory, normally a
sibling of this one (`../unslop` relative to this skill):

- Default voice: `../unslop/references/voice-profile.md`
- Named voices: `../unslop/references/voices/<name>.md` (lowercase,
  hyphenated name the user will say out loud: `blog`, `newsletter`,
  `work`)

If the user has a default profile already and is adding a different
register, save a named voice and leave the default alone. If `../unslop`
does not exist, tell the user, save the profile where they choose, and
note they can move it into the unslop skill's `references/` directory
after installing it.

**Privacy note, always worth saying:** a voice profile contains someone's
real writing. If the skills live in a shared or public repository, a
personal profile probably should not be committed there — suggest a
globally installed copy of the skills, or a gitignore entry, for profiles
the user would not publish.

## Update an existing profile

Read the current profile first. New samples extend it: rotate in stronger
excerpts, refine the distilled habits, and note the update date. Do not
discard observations that still hold just because the new samples don't
happen to show them; ask when unsure whether a habit has changed or is
merely absent from the new batch.
