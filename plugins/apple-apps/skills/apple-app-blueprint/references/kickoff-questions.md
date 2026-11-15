# Kickoff questions

Ask one at a time. Give a recommended answer with each. Look facts up (installed Xcode versions, signing identities, sibling repos) instead of asking. Record every answer as a decision.

1. **Scope:** what is milestone 1? Recommend the core experience with no clever features, plus design and infrastructure.
2. **Project shape:** XcodeGen and local packages, Tuist, or a plain project? Recommend XcodeGen and packages.
3. **Platforms:** which now, which later? Keep model, format and core multiplatform from day one.
4. **Data home and sync:** files in an iCloud container, CloudKit, or local only? Recommend files as the source of truth, key-value store for preferences, keychain for secrets.
5. **Document shape:** loose files, packages, or a database? Recommend packages with a canonical structured file and a derived readable one.
6. **App model:** document-based or library-based?
7. **Visual direction:** themes, type, where colour is allowed, motion rules.
8. **Icon concept:** a few directions, built as an Icon Composer `.icon`.
9. **Quality bars:** propose the blueprint bars; check sibling repos for house standards first.
10. **Where gates run:** locally through the Stop and pre-push hooks, or CI?
11. **Skills:** propose the paired list; search for newer versions.
12. **Toolchain:** Xcode version, deployment targets, concurrency settings.
13. **Source of truth inside a document** and how edits and undo work.
14. **Architecture:** headless core with view models and a CLI?
15. **Signing:** team, bundle identifiers, containers, a separate Dev app.
16. **Interaction details** the spec may get wrong (key bindings that clash with system shortcuts).
17. **Onboarding:** a real sample document that teaches by doing, tested as a scenario.
18. **Sync conflicts:** merge policy.
19. **Performance budgets.**
20. **Repo and git workflow.**
21. **Agent roles and parallel lanes.**
22. **Install-latest path.**
23. **Agent-readable code rules and the verification skill.**
24. **README as storefront.**
