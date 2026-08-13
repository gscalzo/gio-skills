# Research notes: the evidence behind the catalog

Empirical grounding for the pattern catalog, the detector's signal tiers,
and the humanizer's methodology. Read this when you need to justify a
verdict, calibrate confidence, or answer "says who?". Compiled August 2026.

## Word-frequency studies (why the vocabulary list is not vibes)

- **Kobak et al., "Delving into LLM-assisted writing in biomedical
  publications through excess vocabulary"** (Science Advances 2025;
  arXiv:2406.07016; word lists at github.com/berenslab/llm-excess-vocab).
  15M+ PubMed abstracts, 2010-2024, "excess word" analysis against
  pre-LLM extrapolation — no detector involved, so immune to detector
  bias. Measured 2024 frequency ratios: **"delves" ~28x expected,
  "underscores" ~10.9x, "showcasing" ~10.2x**. Found ~291 excess *style*
  words in 2024 (66% verbs, 14% adjectives) where pre-2023 excess words
  were content nouns (covid, remdesivir). Lower-bound estimate: **at least
  13.5% of 2024 PubMed abstracts were LLM-processed**, up to ~40% in some
  subcorpora.
- **Liang, Zou et al., "Quantifying large language model usage in
  scientific papers"** (Nature Human Behaviour 2025; arXiv:2404.01268).
  950,965 papers: up to **17.5% of CS abstracts LLM-modified by Feb
  2024**. Most disproportionate words: realm, intricate, showcasing,
  pivotal.
- **Juzek & Ward, "Why Does ChatGPT 'Delve' So Much?"** (COLING 2025).
  Evidence that lexical overrepresentation is driven by RLHF alignment,
  not just pretraining data.
- **Yakura et al.** (Max Planck, arXiv:2409.01754): ~280,000 academic
  YouTube videos — human *spoken* use of "meticulous", "delve", "realm",
  "adept" rose **up to 51%** in the 18 months post-ChatGPT. Implication:
  **the human baseline is drifting toward AI vocabulary, so single-word
  tells decay over time.** Durable detection rests on structure, stance,
  and specificity, not banned-word lists.

## Detector accuracy and failure (why verdicts must stay humble)

- **Liang et al., "GPT detectors are biased against non-native English
  writers"** (Patterns 2023). Seven commercial detectors vs 91 TOEFL
  essays: **average 61.3% false-positive rate on non-native essays**;
  ~97% flagged by at least one detector; near-perfect accuracy on
  US-native essays. Mechanism: limited vocabulary range = low perplexity =
  the same signal detectors read as "AI". The canonical citation for
  never accusing on statistics alone.
- **Weber-Wulff et al.** (Int. J. Educational Integrity 2023): 14 tools
  including Turnitin — "neither accurate nor reliable", all under ~80%
  accuracy; paraphrase and machine translation sharply degrade detection.
- **Institutional failures:** OpenAI killed its own classifier in 2023 at
  **26% true-positive / 9% false-positive**. Turnitin's claimed <1%
  false-positive rate drifted to ~4%; **Vanderbilt disabled it** (2023),
  noting ~750 of its 75,000 annual papers would be falsely flagged even
  at 1%. ZeroGPT scored the US Constitution **92.15% AI** (memorized
  canonical text = ultra-low perplexity).
- **Paraphrase attacks:** DIPPER (NeurIPS 2023) dropped DetectGPT from
  70.3% to 4.6% detection at 1% FPR; Sadasivan et al. (arXiv:2303.11156)
  show recursive paraphrasing drives detectors toward ~25% accuracy and
  prove convergence toward coin-flip as distributions merge. RAID (ACL
  2024): trivial edits — whitespace, homoglyphs, synonym swaps — can
  "render detectors useless".
- **The counterpoint:** Russell, Karpinska & Iyyer (ACL 2025): a majority
  vote of five annotators who *frequently use LLMs* misclassified **1 of
  300 articles (~99.7%)**, beating nearly all detectors even against
  paraphrased and deliberately "humanized" text. Their cited clues: AI
  vocabulary plus formality, cliché density, and formulaic structure —
  exactly this catalog. Trained-classifier state of the art (Pangram 4)
  reports ~1/24,300 false positives and catches ~94% of humanizer output.
  Detection is not hopeless; it is just not a one-number verdict.
- **Stylometry:** Muñoz-Ortiz et al. (AI Review 2024): humans show
  scattered sentence-length distributions (LLMs cluster in the 10-30
  token band), richer type-token ratio, more negation; LLM text skews
  positive in sentiment. GLTR (ACL 2019): exposing token-probability
  rank raised human detection from 54% to 72% — human text keeps choosing
  surprising words. HC3 corpus (Guo et al. 2023): ChatGPT answers ran
  ~39% longer than human answers to the same questions, with smaller
  vocabulary.

## What actually makes prose read human

- **Persona beats polish.** Jones & Bergen (PNAS 2025): the same model
  passed as human **73% of the time with a persona prompt** (opinions,
  informal register, slang, fallibility) versus **36% without**. Stance
  and imperfection do the heaviest lifting; stakeless balance reads as
  machine.
- **Rhythm is causal, not cosmetic.** Burstiness (sentence-length
  variance) is both a top detector feature and a top reader cue
  (Muñoz-Ortiz; GPTZero's second component).
- **Surprising precision beats elevated diction.** The GLTR result: the
  fix is not fancier synonyms but unexpected, exact ones. Synonym-rotating
  paraphrasers keep the probability profile smooth, which is why they
  fail against both trained classifiers and experienced human readers.
- **Heuristics are exploitable — which is the point.** Jakesch et al.
  (PNAS 2023, N=4,600): readers use first-person anecdote, contractions,
  and concrete detail as "human" cues, and those cues can be manufactured.
  A humanizer must therefore never fabricate experience or facts: the line
  between editing and deception is the no-fabrication rule.
- **Word-swap humanizers fail at the discourse level.** Templates, uniform
  rhythm, puffery, and stakeless stance survive paraphrase — and that is
  what expert readers catch (Russell 2025). What survives every "humanize"
  tool is what this catalog targets: say one specific thing, from one
  perspective, in uneven sentences, without templates.

## Practitioner further reading

- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup) — the field
  guide this catalog's Wikipedia-derived patterns descend from.
- Paul Graham, "Write Like You Talk" (2015) and "Writes and Write-Nots"
  (2024) — the read-it-aloud test, and writing as thinking.
- Wes Kao, "Read your writing in a robot voice"; Ann Handley, "How to
  Write Like Robots Can't" — voice and specificity as the non-replicable
  assets.
- Sam Paech's slop tooling: EQ-Bench slop score, slop-forensics (per-model
  overused-word profiles; stable enough to fingerprint model ancestry),
  antislop-sampler (bans 8,000+ slop patterns at inference; sample
  entries: "tapestry", "testament to", "barely above a whisper", and
  Elara, LLM fiction's favorite character name).
- Drew Breunig, "Using Slop Forensics to Determine Model Ancestry" (2025).
- The Verge, "You sound like ChatGPT" (2025) — the Max Planck data,
  popularized; language flattening thesis.

## Thresholds this package uses, and where they come from

- **Em dashes:** flag density above ~1 per 1,000 words (community
  convention; The Ringer and Benjamin Dreyer document the human em-dash
  tradition — never treat the mark alone as evidence).
- **Short samples:** under ~50 words, no verdict (community skills
  converge on ~40-50); under ~250 words, low confidence (GPTZero's own
  reliability floor).
- **Metadiscourse density:** ~3 calibration phrases ("notably", "it's
  important to note") per 500 words reads as stacking.
- **Structure density:** >3 headings per 300 words or 8+ bullets per 200
  words reads as scaffold.
- **Verdict humility:** detector scores are non-evidence for individual
  sanctions (Vanderbilt, Weber-Wulff, OpenAI's self-shutdown). Quoted,
  checkable patterns are the defensible standard — plus the pre-ChatGPT
  time bound (November 30, 2022).

## Ethical line

This package detects and edits; it does not evade. It never adds fake
typos, fabricated anecdotes, or statistical noise to fool a classifier
(tools built for that exist; their mechanisms — burstiness tuning,
watermark scrubbing, injected "typing patterns" — corroborate which
signals matter, and are not what these skills do). The goal is writing a
careful human would stand behind, under their own name.
