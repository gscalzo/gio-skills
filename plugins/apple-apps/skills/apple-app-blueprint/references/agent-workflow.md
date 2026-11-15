# Agent workflow

Read this before splitting work across agents.

## Roles by model tier
| Role | Model tier | Works in |
|---|---|---|
| Orchestration: plan, brief, integrate, merge | largest model | the main session |
| Code for one slice | mid-size model | its own git worktree and branch |
| Tests, scenarios, trying the app | smallest model | alongside the coder, same worktree |
| Pull request review | a fresh largest-model session | a separate session with no shared context |
| Milestone adversarial review | a different vendor's model | a separate session |

The reviewer must not be the session that wrote or orchestrated the code. Different context, and at milestones a different model, catch different blind spots.

## Briefs
The orchestrator writes `docs/plans/briefs/<slice>.md` before starting a coder: role, what to read first, branch name, exact deliverables, "done when" checks, and what to report back. A coder that needs the conversation to do its job got a bad brief.

## Phases
1. **Foundation, sequential:** repo and docs, scaffold, gate, hooks and install, skills and the verification skill. Nothing parallel starts before the gate is real.
2. **Lanes in parallel:** typically core logic, look and feel, and the hardest platform piece (for an editor: the text system). Each lane is a coder plus a tester.
3. **Integration by the orchestrator:** bind lanes, onboarding, smoke tests, performance runs, polish, reviews, sign-off.

## Pull requests
One per slice, branch `m1/<slice>`, gate report summary in the description, fresh-model review before squash merge. Conventional Commits.

## Human checkpoints
Keep them few and concrete: icon concept, design tokens with screenshots, first hands-on feel of the core interaction, onboarding copy, README storefront, milestone sign-off with real use.
