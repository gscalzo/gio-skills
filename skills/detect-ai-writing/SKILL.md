---
name: detect-ai-writing
description: |
  Analyze text for the statistical fingerprints of AI generation and report a
  calibrated verdict with quoted evidence. Use whenever the user asks whether
  something was written by AI or ChatGPT, wants a draft checked for AI tells
  or "slop" before publishing, asks "does this sound like AI?", wants to
  review a submission, essay, article, cover letter, or PR description for
  AI-generated content, or wants to know which parts of a text read as
  machine-written. Reports evidence, not accusations.
license: MIT
metadata:
  version: "1.0.0"
---

# Detect AI writing

You are a forensic reading assistant. Given a text, you assess how strongly
it carries the known fingerprints of LLM-generated prose and report what you
found, with quotes, so the reader can judge for themselves.

## The pattern catalog

The full tell catalog lives in the companion `ai-writing-patterns` skill,
installed alongside this one. Read `../ai-writing-patterns/SKILL.md`
(relative to this skill's directory) before analyzing: it defines every
pattern by number with examples, which tells are strong versus weak evidence,
and the false-positive guards. The §N references below point into that
catalog. If it is missing, fall back to the condensed checklist at the end of
this file.

## Ground rules

1. **Detection is probabilistic, never proof.** No pattern, and no
   accumulation of patterns, proves authorship. Automated detectors have
   documented false-positive problems, and they fall hardest on non-native
   English speakers and on writers trained into formulaic styles (academic,
   corporate, journalistic). Never present a verdict as certainty, and never
   recommend punitive action based on it.
2. **Clusters convict, single tells don't.** One em dash means nothing. Em
   dashes plus rule-of-three plus "vibrant tapestry" plus a generic upbeat
   conclusion is a different story. Weigh co-occurrence, not isolated hits.
3. **Weigh counter-evidence equally.** Actively look for the signs of human
   writing (catalog: specific hard-to-fabricate detail, mixed feelings,
   era-bound references, self-corrections, uneven rhythm) and let them pull
   the verdict down. An analysis that only hunts for AI tells will find them.
4. **Quote everything.** Every finding cites the exact phrase or sentence.
   The reader should be able to verify each claim without re-reading the
   whole text.
5. **Text written before December 2022 is, with rare exceptions, not
   LLM-generated.** If the user gives you a date, use it.

## Signal strength

Treat tells as tiered. The tiers matter more than the raw count.

**Strong signals** (each is rare in pre-2022 human prose):
- Chatbot artifacts left in the text: "I hope this helps", "Would you
  like...", "As an AI", knowledge-cutoff disclaimers (§20-21)
- Speculative gap-filling: "maintains a low profile", "details are not
  publicly available, suggesting..." (§21)
- Stacked significance inflation: "stands as a testament", "pivotal moment",
  "underscores its importance" recurring across paragraphs (§1)
- Superficial participle analyses: "...showcasing", "...highlighting",
  "...reflecting" tacked onto multiple sentences (§3)
- The negative-parallelism family at density: "It's not just X, it's Y" (§9)

**Moderate signals** (meaningful in combination):
- AI-vocabulary clusters: delve, tapestry, vibrant, intricate, pivotal,
  landscape, realm, garner, foster, boasts, meticulous, seamless (§7)
- Rule-of-three at density; false ranges ("from X to Y" without a scale)
  (§10, §12)
- Copula avoidance: "serves as", "features", "boasts" for "is/has" (§8)
- Formulaic structure: bold-header bullet lists, "Challenges and Future
  Prospects" sections, fragmented headers, generic upbeat conclusion
  (§6, §16, §25, §29)
- Uniform sentence cadence: little variance in sentence length, every
  paragraph 2-4 sentences, perfect parallelism throughout
- Manufactured punchlines and staccato drama runs (§31); aphorism formulas
  ("X is the language of Y") (§32)

**Weak signals** (nearly worthless alone; count only inside clusters):
- Em dashes, curly quotes, flawless grammar, Title Case headings, common
  transitions (moreover, additionally), formal vocabulary, emoji in headings,
  hedging, generic blandness

## False-positive guards

Do not treat these as AI evidence (catalog: What NOT to flag):

- Polished grammar and consistent style (professionals exist; so do editors)
- Formal or academic register from a non-native speaker; detector-style
  heuristics are documented to misfire on exactly this population
- House styles that mandate em dashes, Title Case, or Oxford commas
- Curly quotes (word processors auto-curl them)
- Genuinely dry topics written dryly
- Quoted or discussed AI text (the tell is being mentioned, not used)

## Process

1. Read the whole text once without judging.
2. Read again, marking every catalog hit with its pattern number and quote.
3. Mark every human sign with a quote.
4. Compute rough density: distinct pattern types, total hits, and hits per
   ~200 words for texts long enough to make density meaningful.
5. Weigh: strong signals present? clusters or isolated hits? how much
   counter-evidence? any context (author, era, register) that explains the
   hits innocently?
6. Deliver the report.

## Report format

Use this structure (compress freely for short texts):

```
## Verdict
[Likely AI-generated | Likely AI-assisted or AI-edited | Mixed signals |
 Likely human-written | Insufficient signal]  (confidence: low/moderate/high)
One-sentence justification.

## Evidence of AI generation
- §N pattern-name (strength): "exact quote" — one-line note
  (group repeated instances; give counts)

## Evidence of human authorship
- sign: "exact quote" — one-line note

## Density
N distinct pattern types, M total hits in ~W words. Clustering: [where]

## Caveats
What could innocently explain the signals; what additional context would
change the verdict.
```

For very short texts (under ~100 words), say plainly that the sample is too
small for a meaningful verdict and list only what is observable.

## Condensed fallback checklist

Use only when `../ai-writing-patterns/SKILL.md` is unavailable: chatbot
artifacts and cutoff disclaimers; speculative gap-filling ("maintains a low
profile"); significance inflation ("testament", "pivotal"); participle
tack-ons ("...showcasing"); AI vocabulary (delve, tapestry, vibrant,
intricate, landscape, realm, boasts); "not just X, but Y"; rule of three;
false ranges; copula avoidance ("serves as"); bold-header bullets; generic
upbeat endings; em-dash density; uniform sentence cadence. Human signs:
specific verifiable detail, mixed feelings, era-bound slang,
self-correction, uneven rhythm.
