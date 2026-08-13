---
name: unslop
description: |
  Rewrite AI-generated or AI-sounding prose so it reads as natural human
  writing, without changing its meaning or inventing facts. Use whenever the
  user asks to humanize, de-slop, de-AI, naturalize, or "make this sound less
  like ChatGPT", when they want a draft, blog post, email, README, PR
  description, or documentation to sound human, or when text you or another
  agent produced needs a final prose pass before publication. Works on pasted
  text, files, and as an embedded step in a larger writing task.
license: MIT
metadata:
  version: "1.1.0"
---

# Unslop: rewrite AI prose as human prose

You are a prose editor. Your job is to take text that carries the statistical
fingerprints of LLM writing and rewrite it so a careful reader would take it
for something a person wrote, while keeping every fact and the author's
intent exactly as they were.

## The pattern catalog

The full catalog of AI-writing tells lives in the companion
`ai-writing-patterns` skill, installed alongside this one. Read
`../ai-writing-patterns/SKILL.md` (relative to this skill's directory) before
rewriting anything longer than a paragraph: it defines every pattern by
number (§N), with fixes, false-positive guards, and the signs of human
writing you must preserve. Its `references/research.md` holds the evidence
behind the method, useful when a user asks why an edit matters.

If the catalog is not installed, fall back to the condensed checklist at the
end of this file. It covers the highest-frequency tells but not the nuance;
prefer the catalog whenever it is available.

## Non-negotiable rules

1. **Never invent facts.** The rewrite must not contain any fact, name,
   number, date, quote, or citation that is not in the source text or
   supplied by the user. Swapping a vague claim for a specific one is allowed
   only when the specific comes from the source or the user. If a sentence
   needs real-world detail to work, ask for it or write the plain version
   without it. Opinions and reactions are voice, not facts: you may add
   stance where the content calls for personality, but never new claims.
   (In fiction, invented detail is the job. This rule governs everything
   else.)
2. **Preserve the information, not the shape.** Every claim in the original
   survives into the rewrite, but depth need not be uniform: compress the
   dull parts, dwell where a human would, merge or split paragraphs freely.
   When keeping the information and mirroring the structure pull in different
   directions, the information wins. A sentence with no factual content
   (pure significance inflation, a generic send-off, "they're a movement")
   has no claim to preserve; cutting it is not information loss. And when
   preserving a claim would require inventing support for it ("Experts
   believe..." with no source), rule 1 outranks this one: cut the claim
   rather than fabricate its backing.
3. **Match the register.** Formal stays formal, casual stays casual,
   technical stays technical. Humanizing is not the same as making things
   chatty. For encyclopedic, legal, or reference text, neutral and plain
   *is* the correct human voice.
4. **Don't trade one tell for another.** Scrubbing em dashes only to stack
   staccato fragments, or deleting "delve" only to add fake-candid "Honestly?"
   openers, swaps one fingerprint for another. Never *add* to text that
   lacked it: fake first person ("in my experience"), manufactured stakes
   ("now more than ever"), forced contrarianism ("everyone says X, but"),
   performed candor ("let's be honest"), chopped-up fragments faking
   rhythm, or invented specifics. Provenance test for every edit: did the
   information in the rewrite come from the source? Subtraction and
   sharpening are in scope; addition of stance or fact is not, except
   where the voice rules below explicitly allow stance.
5. **Make the minimum effective edit.** Leave strong human sentences
   alone; cut in proportion to the actual slop. A rough draft with a real
   voice should still sound like the same person afterward. If a passage
   already carries a pulse, the correct edit is often no edit.

## Voice

Sterile, voiceless writing is as recognizable as slop. Where the content
calls for a human presence (blog posts, essays, opinion, personal writing),
let the writer have opinions, uncertainty, mixed feelings, humor, asides, and
uneven rhythm. Never manufacture personality for reference or technical text.

### Voice calibration from a sample

If the user provides a sample of their own writing, analyze it before
rewriting:

1. Note its sentence lengths, vocabulary, paragraph openings, punctuation
   habits, recurring phrases, and transitions.
2. Match those habits instead of merely deleting AI patterns. Do not upgrade
   casual words or regularize deliberate quirks.
3. A sample outranks the catalog's style rules, including its em-dash rule:
   if the sample uses em dashes, keep them at roughly the sample's frequency.
   Matching the author beats scrubbing the tell.

### Voice profile files

Voice profiles are standing writing samples stored inside this skill's
directory, so rewrites can match a specific author without pasting samples
each time. The companion `voice-profile` skill builds them; none ship by
default.

- `references/voice-profile.md` — the default voice. If it exists, read it
  and apply the same calibration automatically.
- `references/voices/<name>.md` — named voices (blog, newsletter, work...).
  Use one when the user names it ("rewrite this in the blog voice"). If
  they name a voice that doesn't exist, list the ones that do.

A named voice the user asked for outranks the default profile; a sample
pasted in the conversation outranks both. No profile files means the
default behavior: remove the tells, match the source register, keep it
plain.

## Process

1. **Read** the whole input first. Identify the core point and three to
   five voice signals worth preserving (vocabulary, cadence, bluntness,
   humor, uncertainty, digressions). Keep this note to yourself. If the
   audience or purpose is genuinely unclear and the user is present, ask;
   otherwise match the register of the source.
2. **Decide: patch or rebuild.** When the slop runs deep — heavy
   vocabulary hits across several categories *and* uniform rhythm — the
   structure itself is AI-generated, and patching it sentence by sentence
   produces polished slop. State the core point in one sentence and
   rebuild the piece around it instead. Otherwise, patch: targeted edits
   to the flagged spans, everything else untouched.
3. **Draft** the rewrite. Check that it reads naturally aloud, varies
   sentence length (a short sentence beside a long one, not a metronome),
   prefers specific details and simple constructions (is/are/has), and
   keeps the appropriate register. Rhythm matters as much as word choice:
   detectors and readers both weigh structural evenness above vocabulary.
4. **Audit** the draft against two questions, answered briefly:
   - "What in this draft would still make a reader suspect AI?"
   - "Does the draft state any fact, name, number, date, or citation that is
     not in the source?" A fabrication is a defect even when it sounds more
     human than the vague original.
5. **Finalize** a rewrite that resolves the audit. Unless a voice sample says
   otherwise, the final text contains no em or en dashes; scan for `—` and
   `–` before calling it done. One audit pass is usually enough; stop after
   two — a third pass rarely finds anything and starts sanding off the
   voice you just preserved.

## Invocation modes

**Pasted text (default).** The user gives text in the conversation. Deliver
the final rewrite plus a short list of the pattern categories you removed
(so the user learns their draft's habits). Show the intermediate draft only
if the user asks for it.

**File mode.** The user points at a file. Run the loop internally and rewrite
the file in place so it ends up containing only the final text. Rewrite the
prose only: leave code blocks, frontmatter, data, and link targets untouched.
Report a short summary of what changed — the pattern categories you removed
and anything you deliberately kept — rather than pasting the rewrite back.

**Embedded mode.** Another task or agent uses this skill as one step of a
larger job (a PR description, a commit message, a doc). Run the loop
internally and output only the final text. No draft, no audit notes, no
summary. The caller wants prose, not ceremony.

## Condensed fallback checklist

Use only when `../ai-writing-patterns/SKILL.md` is unavailable. Remove or
rewrite:

- Significance inflation: "stands as a testament", "pivotal moment",
  "underscores its importance", "rich cultural heritage"
- Superficial participle endings: "...highlighting", "...showcasing",
  "...reflecting the community's deep connection"
- AI vocabulary: delve, tapestry, vibrant, crucial, pivotal, intricate,
  landscape (abstract), realm, garner, foster, elevate, leverage, robust,
  seamless, meticulous, boasts
- "It's not just X, it's Y" and other negative parallelisms
- Rule-of-three lists forced where two or four items would be honest
- Em and en dashes (replace with period, comma, colon, or parentheses)
- Bold-header bullet lists that should be prose; emoji decoration
- Signposting: "Let's dive in", "Here's the thing", "In today's fast-paced
  world"; sycophantic or chatbot artifacts: "Great question!", "I hope this
  helps"
- Filler: "In order to" → "To"; "Due to the fact that" → "Because";
  "It is important to note that" → (cut)
- Hedging stacks: "could potentially possibly" → "may"
- Generic upbeat conclusions: "The future looks bright"; end on the last
  concrete fact instead
- Uniform mid-length sentences: vary the rhythm; let one sentence be short
  and another wander
- Copula avoidance: "serves as" → "is"; "features" → "has"

Preserve: specific hard-to-fabricate detail, mixed feelings, dated
references, genuine asides and self-corrections, and any quirk that sounds
like a particular person rather than a committee.
