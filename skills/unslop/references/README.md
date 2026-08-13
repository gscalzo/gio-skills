# Voice profiles (optional)

Files in this directory teach the unslop skill to write like a specific
person instead of a generic clean editor:

- `voice-profile.md` — the default voice, applied to every rewrite
  automatically.
- `voices/<name>.md` — named voices (`blog.md`, `newsletter.md`,
  `work.md`), applied when a rewrite request names them.

The easiest way to create one is the companion `voice-profile` skill: give
it a few pieces of real writing and it analyzes the rhythm, punctuation,
lexicon, and temperament, then saves the profile here in the format unslop
expects. Hand-written profiles work too; two formats are understood, alone
or combined:

1. **Raw samples.** Two to five paragraphs of the author's writing, pasted
   verbatim. Pick passages that sound like them on a good day.
2. **A distilled profile.** A short analysis of habits: sentence-length
   mix, punctuation they do and don't use, recurring constructions, words
   they'd never write, how they open and close pieces.

Raw samples win on any disagreement with the distilled notes.

Nothing here means default behavior: remove AI tells, match the register
of the source text, keep the result plain.

**Before committing a profile:** it contains someone's real writing. In a
shared or public repository, keep personal profiles out of version control
(this repo's `.gitignore` already excludes this directory's profiles) or
install the skills globally and keep profiles in the installed copy.
