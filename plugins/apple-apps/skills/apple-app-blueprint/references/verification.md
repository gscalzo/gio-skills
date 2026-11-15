# Verification skill and feature map

Read this when creating the project's `verify-<app>` skill. The pattern follows poteto's verification-skill-example.

## Layout
```
.agents/skills/verify-<app>/
  SKILL.md                 doctor, launch, drive, prove, clean up
  references/features/
    README.md              index, conventions, sweep order
    <feature>.md           one file per feature
```

## SKILL.md sections
- **Doctor:** is the installed build fresh (its SHA matches HEAD)? Is the run isolated from real user data (Dev bundle identifier, Dev container, temporary local store)?
- **Launch:** `make install-dev`, or the CLI against a temporary store.
- **Drive:** headless through the CLI first; then the real app through UI tests with stable accessibility identifiers and registered key equivalents, not coordinates.
- **Prove:** see the proof bar.
- **Clean up:** remove temporary stores; never touch the user's library.

## Proof bar
- Drive the production user path: keys, menus, normal plumbing. Inspect internals only after the user path ran.
- Cover success, cancel, error, empty and persistence paths that the change can affect. Persistence means quit, relaunch and check.
- Verify side effects in stored files and state, not only pixels.
- A capture against a stale build is not evidence.

## Feature files
Each uses the same four H2 headings: `Sub-features`, `How to reach it (user's view)`, `Driving it`, `Gotchas`. Keep them behaviour-level and short enough to run without reading source. The gate checks that every scenario maps to a feature file and every feature file has a scenario. Update the feature file in the same pull request as the behaviour change.
