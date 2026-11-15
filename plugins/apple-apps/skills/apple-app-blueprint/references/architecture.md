# Architecture: headless core, CLI, pure model

Read this when shaping packages or adding a feature.

## Layers
```
App targets (thin: scenes, menus, entitlements)
 ├─ UI package          SwiftUI views and the design system (main actor)
 ├─ Platform bridge     AppKit/UIKit pieces SwiftUI cannot do well (main actor)
 └─ Core package        @Observable view models: state + send(_ action:)
      ├─ Model package  pure value types, edit algebra, derived values, merge
      └─ Format package persistence, schema and migrations, storage locations
CLI → Core only         Metrics tool → swift-syntax
```

Rules the gate enforces:
- Core never imports SwiftUI, AppKit or UIKit.
- A view binds to one view model, reads `state`, calls `send`. No logic in views.
- The platform bridge renders view-model state and turns input into actions; it never mutates the model directly.

## The edit algebra
Every user action is an `Edit` value. `apply(_:) -> (Document, inverse: Edit)`. One user gesture is one undo group. Projection into a platform text or view system is tested by round-tripping: apply an edit, project, map the platform change back, compare.

## The CLI and scenarios
`app new`, `app send <doc> '<action json>'`, `app state <doc> --json`, `app run scenario.jsonl`. A scenario is a JSON-lines script of actions and expectations, run against a temporary local store. Scenarios are the primary acceptance tests; UI tests shrink to a few smoke flows. Use swift-argument-parser in the CLI target only, so the shipped app keeps zero third-party dependencies.

## Storage and sync
Prefer a document package per item (a directory with a canonical structured file plus a derived human-readable file) so state and text save atomically and nothing anchors by offset. Put storage behind a protocol with an iCloud implementation and a local one; the CLI and tests always use the local one. Treat sync conflicts as a pure three-way merge, and surface real collisions in the product's own vocabulary rather than as a "conflicted copy".

## Concurrency
Swift 6 mode, complete strict concurrency, `NonisolatedNonsendingByDefault`, `InferIsolatedConformances`. Main-actor default isolation in UI and app targets only. Persistence lives in an actor; saving is debounced and off the main thread.
