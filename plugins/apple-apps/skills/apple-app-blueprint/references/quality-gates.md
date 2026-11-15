# Quality gates for agent-built Swift apps

Read this when setting up or changing the gate.

## Order in `scripts/gate.sh`
Cheapest first, so failures arrive fast:

1. `swiftformat --lint`
2. `swiftlint --strict` with `file_length` 350/450, `function_body_length` 40/60, `type_body_length` 220/300, `cyclomatic_complexity` 8/10, `missing_docs` on public declarations
3. Build every app target and build the multiplatform packages for each platform: Swift 6 mode, complete strict concurrency, warnings as errors
4. Tests with coverage: Swift Testing unit and property tests, snapshot tests for views, CLI scenarios, a few UI smoke tests
5. Metrics tool (below): CRAP, complexity, Halstead, import rule
6. Coverage ratchet per package
7. `jscpd` duplication (Swift is supported), Periphery dead code
8. Agent-readability checks: package READMEs exist; scenarios and feature files map one to one; feature files have the four headings
9. Headless benchmarks against `perf-baseline.json`

`gate.sh --full` adds mutation testing (Muter) on the model and persistence packages, limited to changed files, and UI performance tests.

## CRAP for Swift
CRAP = CC² × (1 − coverage)³ + CC, per function. A function with complexity 10 needs about 42 % line coverage to stay under 15; trivial functions pass untested; complex untested code fails. That is the point: it targets risk, not lines.

There is no off-the-shelf Swift CRAP tool, so build a small SwiftPM executable on swift-syntax:

- Walk every function, initializer, accessor and closure body. Cyclomatic complexity is one plus each `if`, `guard`, loop, `catch`, `case`, ternary, `&&`, `||` and `??`. Cognitive complexity adds nesting depth to each branch. Halstead difficulty is (distinct operators / 2) × (total operands / distinct operands).
- Read per-function line coverage from `xcrun xccov view --report --json <xcresult>`; it lists functions with names and line numbers. Join on file plus start line.
- Check the import graph: the core package must not import UI frameworks.
- Read thresholds and exceptions from `quality_config.json`. Every exception carries a reason; an exception that no longer matches a finding fails as stale.
- Write `build/quality/report.json` with every measured function, so a pull request can quote it.
- Give the tool its own tests with fixture Swift files and known expected values. A metrics tool that is wrong is worse than none.

Exclude SwiftUI `body` properties and pure app wiring from CRAP and coverage, and cover views with snapshot tests instead. Document each exclusion.

## Bars
Start from these and ratchet down to the codebase's own level ("this number or stricter"):

| Bar | Gate |
|---|---|
| CRAP | ≤ 15 per function |
| Cyclomatic / cognitive / nesting / Halstead | ≤ 10 / ≤ 12 / ≤ 3 / ≤ 50 |
| File size | ≤ 450 lines |
| Duplication | 0 clones of 50 or more tokens |
| Dead code | 0 Periphery findings |
| Mutation | 0 survivors in model and persistence |
| Coverage | per-package floor starting at the measured level, never below 70 % |

Lowering a bar or narrowing scope requires an ADR change. Raising one happens in the same commit as the improvement.

## Hooks
- **Agent Stop hook** (Claude Code `Stop` in `.claude/settings.json`): run `scripts/stop-gate.sh`. It hashes Swift sources, project and package manifests and the quality config; if the hash matches the last green run it exits 0, otherwise it runs the gate and on failure prints a short report to stderr and exits 2. Exit code 2 blocks the stop and sends the report back to the agent, so a session cannot finish red. A hook that only echoes a reminder enforces nothing.
- **PostToolUse hook**: format edited Swift files with swiftformat.
- **pre-push**: `gate.sh --full`. **post-merge** on `main`: `make install`.
- Keep mutation and UI performance out of the Stop hook; they take minutes.

## Performance budgets
Measure with `os_signpost` and XCTest metrics in a Release build. Typical budgets: interaction to pixels p95 under 8 ms on a large document, model operation p95 under 1 ms, incremental derived values under 4 ms, scroll hitch ratio under 5 ms/s, cold launch under 400 ms, open document under 100 ms, and saving never on the main thread. Headless benchmarks run in the Stop hook; UI-driven ones in pre-push. A 20 % regression against the recorded baseline fails.
