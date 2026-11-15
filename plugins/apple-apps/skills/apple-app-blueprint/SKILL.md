---
name: apple-app-blueprint
description: |
  Opinionated blueprint for starting and running a native Apple app (macOS, iPadOS, iOS) built mostly by coding agents: project shape, headless core with a CLI, local quality gates enforced by the agent's Stop hook (CRAP, complexity, duplication, dead code, mutation, performance budgets), agent roles by model tier, a verification skill with a feature map, agent-readable code rules, and a one-command install of the latest build. Use when the user says "new Mac app", "new iOS app", "start a SwiftUI project", "set up quality gates for Swift", "CRAP metric for Swift", "plan an Apple app", "grill me on this app", or wants to reuse the blueprint from a previous Apple project.
license: MIT
metadata:
  version: "0.1.0"
---

# Apple app blueprint

A set of decisions that worked together on a real agent-built Mac app. Each one exists because agents write most of the code: they are fast, but they drift, they verify badly through pixels, and they stop when the session ends. The blueprint makes drift fail loudly, makes verification cheap, and makes "done" mean proven.

Use it in two ways:

1. **Kickoff.** Walk the user through `references/kickoff-questions.md` one question at a time, recommending the blueprint's default for each and recording every answer as a decision. Then write the plan and the ADRs.
2. **Setup.** Apply the defaults below and the details in the references. Adapt numbers to the codebase; never weaken a bar silently.

## The defaults, and why

### 1. Plan in milestones; the first one has no clever features
Milestone 1 is the core experience plus the full infrastructure, design system and install path. Clever features (AI, sync extras, integrations) come later. Reason: the riskiest technical parts and the quality machinery need to exist before anything is built on top, and a usable M1 gets daily use, which is the best test.

### 2. Generated project, logic in local Swift packages
XcodeGen `project.yml` with thin app targets; the `.xcodeproj` is generated and ignored. Logic lives in local SwiftPM packages (model, format/persistence, core view models, platform bridges, UI). Reason: no project-file merge conflicts, agents can edit YAML reliably, `swift test` is fast and headless, coverage is per package. Plan for iPad from day one by keeping model, format and core packages multiplatform even if the iPad UI comes later.

### 3. Headless core: view models with `state` and `send(_:)`, plus a CLI
Following Shopify's 2026 native rewrite (https://shopify.engineering/back-to-native): a core package of `@Observable` view models that **never imports SwiftUI, AppKit or UIKit**; each view binds to one view model and holds no logic (a review rule, not a gate check; only the import rule is gate-enforced); a command-line tool links only the core and can create, act on and inspect state. Behaviour tests are JSON-lines scenarios run through the CLI. Reason: agents verify in milliseconds through state instead of minutes through screenshots, and nearly all logic becomes cheap to test. See `references/architecture.md`.

### 4. Pure model with an edit algebra
Every user action is a value; `apply(edit) -> (newState, inverse)`. Undo is applying the inverse. Merges are pure functions. Reason: exact undo, property tests, and low CRAP for free.

### 5. Quality gates run locally and the agent cannot end a session red
One `scripts/gate.sh`. The agent harness Stop hook runs it when the source fingerprint changed and exits with code 2 on failure, which blocks the session and returns the report to the agent. The hook reads `stop_hook_active` from its stdin JSON and never traps a session forever: after 3 consecutive blocked stops with an unchanged failure, or when `GATE_BYPASS_REASON` or a `.gate-bypass` file with a reason is present, it allows the stop, prints a loud report and records the bypass in the gate report. Never bypass silently. The git pre-push hook runs the full gate including mutation testing and UI performance. No CI is needed for a private solo project, which avoids the macOS runner multiplier. Bars: CRAP at most 15 per function, cyclomatic at most 10, cognitive at most 12, nesting at most 3, Halstead difficulty at most 50, at most 450 lines per file, zero duplicate blocks of 50 tokens, zero dead code, zero surviving mutants in the model and persistence packages, coverage ratcheted per package. Every exception needs a written reason and stale exceptions fail. See `references/quality-gates.md`.

### 6. Performance budgets are gated
Keystroke or interaction to screen within one 120 Hz frame at p95, model operations under a millisecond, launch and open budgets, autosave never on the main thread, and a regression of more than 20 % against a recorded baseline fails. Reason: "smooth" is not checkable until it is a number.

### 7. Agent roles by model tier
The large model orchestrates, plans, integrates and merges. A mid model writes code, one lane per git worktree. A small model writes tests, runs scenarios and tries the app. A fresh large model reviews every pull request, and a different vendor's model gives an adversarial review at milestone sign-off. Reason: cost goes where judgement is needed, and the reviewer never shares the author's context. See `references/agent-workflow.md`.

### 8. Verification is a project skill with a feature map
A project-local `verify-<app>` skill: doctor, launch, drive, prove, clean up. A feature map with one file per feature, each with the same four headings. "It opens" is not proof; drive the production path and check persistence by relaunching. Reason: agents claim success too early, and a scoped feature file is cheaper to load than a wiki. See `references/verification.md`.

### 9. Code is agent-readable and context-readable
Small files, one primary type per file, a README per package, doc comments on every public symbol, explicit names, no clever generics, architecture map updated in the same pull request. Reason: every file an agent reads costs context; code that fits in one read gets changed correctly.

### 10. Always installable on the developer's Mac
`make install` builds Release, quits the running app, keeps the previous build for `make rollback`, installs into `/Applications` and relaunches. `make install-dev` does the same for the Dev app (its own bundle identifier and name, installed beside the real one, with its own rollback copy), so unfinished branches can be tried without touching the real app. A post-merge hook on `main` runs `make install`. About shows version, build and git SHA. A separate Dev app with its own bundle identifier and its own iCloud container protects real data from unfinished builds.

### 11. The README is the storefront
`README.md` presents the project on GitHub: icon, name, one line of pitch, one hero screenshot with light and dark variants, a few principles, a link to docs. Developer docs live in `docs/development.md`, agent docs in `AGENTS.md`.

### 12. Toolchain pinned per repo
Pin the Xcode version with `DEVELOPER_DIR` in the Makefile, gate and hooks, never by changing the global `xcode-select`. Swift 6 language mode, complete strict concurrency, approachable-concurrency upcoming features, main-actor default isolation only in UI and app targets so the model stays nonisolated and testable.

## Skills to pair with this blueprint
`references/skills.md` lists the skills that covered SwiftUI, concurrency, testing, performance, TextKit, accessibility, Liquid Glass, macOS design and app icons, chosen for recency and lack of overlap. Re-check versions with `npx skills find` at kickoff; the list ages.

## What to write at kickoff
- `docs/plans/M1.md`: decisions table, scope in and out, architecture sketch, gate, budgets, roles, phases and slices, human checkpoints, definition of done.
- `docs/adr/0001` onwards, one decision per file, with `ADR.md` as the index.
- `AGENTS.md` as the source of truth for agents, `CLAUDE.md` importing it.
- `docs/architecture.md` as a one-page map.
- A brief per slice in `docs/plans/briefs/` that a coder agent can follow without the conversation.
