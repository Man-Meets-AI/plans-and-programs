# Program Contract

A Program is a living initiative document. It keeps the durable truth for work that spans several ExecPlans.

## What A Program Is

A Program records:

- why the initiative exists
- which research and decisions shaped it
- which child ExecPlans belong to it
- what has landed
- what is next
- what evidence proves the initiative can be completed

A Program is not a task list and not a single implementation plan. The implementation details belong in child ExecPlans.

## Storage

Active Programs live under:

```text
docs/programs/active/<YYYY-MM-DD-program-id>/
```

Completed Programs live under:

```text
docs/programs/completed/<YYYY-MM-DD-program-id>/
```

Move the whole folder only when the initiative is actually complete.

## Required Packet Files

Each Program packet should contain:

- `program.md`
- at least one `research-pass-*.md`
- at least one `normalized-pass-*.md`
- `converged-decision-packet.md`
- `dependency-graph.md`
- `plan-split-recommendation.md`
- `cross-repo-review.md`
- one or more `planning-brief-<N>.md` files
- `current-planning-brief.txt`

The pointer file must contain exactly one planning brief filename.

## `program.md` Frontmatter

Every `program.md` starts with YAML frontmatter:

```yaml
---
program_id: example-program
title: Example Program
status: active
created_at: 2026-04-29
completed_at: null
summary: One sentence describing the initiative.
post_build_recap: null
read_when:
  - Planning the next slice.
---
```

When complete:

- `status` is `complete`
- `completed_at` is a real date
- `post_build_recap` is non-empty
- `Outcomes & Retrospective` explains what happened
- `Next Slice` says no required next slice remains

## Required Sections

Use these sections in order:

1. `# <Program title>`
2. A short sentence saying this is a living initiative document
3. A sentence saying the Program must follow `docs/programs/PROGRAMS.md`
4. `## Purpose / Big Picture`
5. `## Program Inputs`
6. `## Current State`
7. `## Progress`
8. `## Decision Log`
9. `## Slice Ledger`
10. `## Next Slice`
11. `## Risks and Watchpoints`
12. `## Outcomes & Retrospective`
13. `## Validation and Acceptance`
14. `## Artifacts and Notes`
15. `## Interfaces and Dependencies`

## Relationship To ExecPlans

Programs and ExecPlans work together:

- Program: initiative memory across several slices.
- ExecPlan: exact execution contract for one slice.

Program-linked ExecPlans should include:

```yaml
program_id: example-program
planning_brief: docs/programs/active/2026-04-29-example-program/planning-brief-1.md
```

Never point an ExecPlan at `current-planning-brief.txt`.

