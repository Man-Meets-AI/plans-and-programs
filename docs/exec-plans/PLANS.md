# ExecPlan Contract

An ExecPlan is a self-contained Markdown plan that a fresh agent can follow to deliver one working slice.

The reader has the repository and this file. They do not have your chat history.

## Storage

Active plans live under:

```text
docs/exec-plans/active/YYYY-MM-DD-slice-name.md
```

Completed plans live under:

```text
docs/exec-plans/completed/YYYY-MM-DD-slice-name.md
```

## Required Frontmatter

Every ExecPlan starts with YAML frontmatter:

```yaml
---
title: Example Slice
status: active
created_at: 2026-04-29
completed_at: null
summary: One sentence describing the intended outcome.
post_build_recap: null
read_when:
  - Resuming implementation.
---
```

Program-linked ExecPlans also include:

```yaml
program_id: example-program
planning_brief: docs/programs/active/2026-04-29-example-program/planning-brief-1.md
```

If `program_id` is present, `planning_brief` is required. If `planning_brief` is present, `program_id` is required.

`planning_brief` must point at an immutable `planning-brief-N.md` file, never `current-planning-brief.txt`.

## Completion Rules

Use `status: active` while work remains.

Use `status: complete` only when:

- implementation is done
- validation is done or skipped with an explicit reason
- `completed_at` is a real date
- `post_build_recap` is non-empty
- `Outcomes & Retrospective` is filled in

## Required Sections

Use these sections in order:

1. `# <ExecPlan title>`
2. A short sentence saying this is a living execution plan
3. A sentence saying the ExecPlan must follow `docs/exec-plans/PLANS.md`
4. `## Purpose / Big Picture`
5. `## Progress`
6. `## Surprises & Discoveries`
7. `## Decision Log`
8. `## Outcomes & Retrospective`
9. `## Context and Orientation`
10. `### In Scope`
11. `### Out Of Scope`
12. `## Plan of Work`
13. `## Milestones`
14. `## Concrete Steps`
15. `## Validation and Acceptance`
16. `### Test Commands`
17. `## Idempotence and Recovery`
18. `## Artifacts and Notes`
19. `## Interfaces and Dependencies`

## Writing Standard

Make the plan novice-readable.

Name files, commands, inputs, outputs, and assumptions directly. Avoid vague phrases like "clean this up" or "wire the thing."

The plan should describe behavior that can be observed, not just code that could be written.

## Living Document Rule

Update these sections as work proceeds:

- `Progress`
- `Surprises & Discoveries`
- `Decision Log`
- `Outcomes & Retrospective`
- `Validation and Acceptance`
- `Artifacts and Notes`
- frontmatter

If implementation changes the scope or sequence, update the ExecPlan first, then continue.

