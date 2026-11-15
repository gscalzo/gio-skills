# Kickoff questions

Ask one at a time. Give a recommended answer with each. Look facts up (installed Xcode versions, signing identities, sibling repos) instead of asking. Record every answer as a decision.

1. **Scope:** what is milestone 1? Recommend the core experience with no clever features, plus design and infrastructure.
2. **Project shape:** XcodeGen and local packages, Tuist, or a plain project? Recommend XcodeGen and packages.
3. **Platforms:** which now, which later? Recommend one platform for milestone 1 (macOS for a writing or desktop-first tool, iOS for a capture tool) and keep model, format and core multiplatform from day one.
4. **Data home and sync:** files in an iCloud container, CloudKit, or local only? Recommend files as the source of truth, key-value store for preferences, keychain for secrets.
5. **Document shape:** loose files, packages, or a database? Recommend packages with a canonical structured file and a derived readable one.
6. **App model:** document-based or library-based? Recommend a library for collections of items (notes, projects, entries) and document-based for standalone files the user names, moves and shares.
7. **Visual direction:** themes, type, where colour is allowed, motion rules. Recommend system fonts, one accent colour, light and dark from the start, and motion only to explain a change.
8. **Icon concept:** a few directions, built as an Icon Composer `.icon`. Recommend three directions, pick one, build it as a layered `.icon` file.
9. **Quality bars:** propose the blueprint bars; check sibling repos for house standards first. Recommend the SKILL.md §5 bars unchanged: CRAP at most 15, cyclomatic at most 10, cognitive at most 12, nesting at most 3, zero duplicates, zero dead code.
10. **Where gates run:** locally through the Stop and pre-push hooks, or CI? Recommend local hooks for a private solo project; add CI only when others contribute.
11. **Skills:** propose the paired list; search for newer versions. Recommend `references/skills.md` as the start, installed project-scoped and pinned.
12. **Toolchain:** Xcode version, deployment targets, concurrency settings. Recommend the latest stable Xcode pinned with `DEVELOPER_DIR`, deployment targets one major version back, Swift 6 mode with complete strict concurrency.
13. **Source of truth inside a document** and how edits and undo work. Recommend a pure value model with an edit algebra: every action is an `Edit`, undo applies the inverse.
14. **Architecture:** headless core with view models and a CLI? Recommend yes: core package of view models, CLI linking only the core, scenarios as acceptance tests.
15. **Signing:** team, bundle identifiers, containers, a separate Dev app. Recommend one team, a separate Dev app with its own bundle identifier and iCloud container, created at kickoff.
16. **Interaction details** the spec may get wrong (key bindings that clash with system shortcuts). Recommend listing every custom shortcut and checking it against system and standard-app shortcuts before building.
17. **Onboarding:** a real sample document that teaches by doing, tested as a scenario. Recommend exactly that, with no tour screens.
18. **Sync conflicts:** merge policy. Recommend a pure three-way merge that surfaces real collisions in the product's own vocabulary, never as a "conflicted copy".
19. **Performance budgets.** Recommend the SKILL.md §6 defaults: interaction within one 120 Hz frame at p95, model operations under 1 ms, a 20 % regression against baseline fails.
20. **Repo and git workflow.** Recommend trunk on `main`, one worktree per lane, short-lived branches, pull requests reviewed by a fresh agent, Conventional Commits.
21. **Agent roles and parallel lanes.** Recommend the SKILL.md §7 tiers: large model orchestrates and reviews, mid model codes one lane per worktree, small model tests.
22. **Install-latest path.** Recommend `make install` with `make rollback`, `make install-dev` for the Dev app, and a post-merge hook on `main`.
23. **Agent-readable code rules and the verification skill.** Recommend the SKILL.md §8 and §9 rules and a `verify-<app>` skill with a feature map created in milestone 1.
24. **README as storefront.** Recommend icon, name, one-line pitch, one hero screenshot with light and dark variants, a few principles, a link to docs.
