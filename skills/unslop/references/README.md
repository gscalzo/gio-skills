# Voice profile (optional)

Drop a file named `voice-profile.md` in this directory and the unslop
skill will calibrate every rewrite to it automatically, as if the user had
pasted a writing sample.

Two formats work, and they can be combined:

1. **Raw samples.** Two to five paragraphs of your own published writing,
   pasted verbatim. Pick passages that sound like you on a good day.
2. **A distilled profile.** A short analysis of your habits: typical
   sentence-length mix, punctuation you do and don't use, recurring
   constructions, words you'd never write, how you open and close pieces.

Raw samples are more robust; a distilled profile is easier to maintain.
When both are present, the samples win on any disagreement.

No file here means the skill uses its default behavior: remove AI tells,
match the register of the source text, and keep the result plain.
