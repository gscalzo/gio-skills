# Skills to pair with the blueprint

Chosen in November 2026 for recency, install count and lack of overlap. Re-check with `npx skills find <topic>` at kickoff. Install project-scoped (`.agents/skills`, linked from `.claude/skills`) and pin in `skills-lock.json`.

| Concern | Skill |
|---|---|
| SwiftUI | `twostraws/swiftui-agent-skill@swiftui-pro` |
| Splitting large views | `dimillian/skills@swiftui-view-refactor` |
| Swift concurrency | `avdlee/swift-concurrency-agent-skill@swift-concurrency` |
| Swift Testing | `twostraws/swift-testing-agent-skill@swift-testing-pro` |
| SwiftUI performance | `dimillian/skills@swiftui-performance-audit` |
| AppKit/UIKit performance, Instruments | `dpearson2699/swift-ios-skills@debugging-instruments` |
| TextKit 2 | `charleswiltgen/axiom@axiom-textkit-ref`, `charleswiltgen/axiom@axiom-audit-textkit` |
| AppKit accessibility | `rgmez/apple-accessibility-skills@appkit-accessibility-auditor` |
| Liquid Glass | `dimillian/skills@swiftui-liquid-glass` |
| macOS design | `ehmo/platform-design-skills@macos-design-guidelines` |
| Public package APIs | `dpearson2699/swift-ios-skills@swift-api-design-guidelines` |
| App icon as an Icon Composer `.icon` | `jonjaques/agent-skillz@icon-composer` (needs Icon Composer 2, shipped with Xcode 27) |
| Adversarial review | `poteto/noodle@adversarial-review` |

Avoid stacking overlapping skills for the same concern; they give contradictory advice. Write a project-local skill for any hard area no public skill covers, and grow it as the project learns.
