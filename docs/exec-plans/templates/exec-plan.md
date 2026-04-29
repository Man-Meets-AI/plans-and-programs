---
title: Example Slice
status: active
created_at: 2026-04-29
completed_at: null
summary: Describe the intended outcome in one sentence.
post_build_recap: null
read_when:
  - Resuming implementation.
---

# Example Slice

This is a living execution plan.

This ExecPlan must be maintained in accordance with `docs/exec-plans/PLANS.md`.

## Purpose / Big Picture

Explain the user-visible or operator-visible result this slice will produce.

## Progress

- [ ] YYYY-MM-DD: Created the ExecPlan.

## Surprises & Discoveries

Record new facts found during execution.

## Decision Log

Decision: Record the first implementation decision.
Rationale: Explain why this path was chosen.
Date: YYYY-MM-DD

## Outcomes & Retrospective

Leave this future-facing while active. Fill it in when complete.

## Context and Orientation

Explain the repository areas and concepts a newcomer needs.

### In Scope

Name the concrete work this slice includes.

### Out Of Scope

Name adjacent work this slice must not absorb.

## Plan of Work

Describe the implementation sequence in prose.

## Milestones

Describe independently verifiable milestones.

## Concrete Steps

List exact commands and edits.

## Validation and Acceptance

Explain what proves the slice works.

### Test Commands

Run these commands from the repo root:

```bash
bun run validate
bun run lint
bun run format:check
```

## Idempotence and Recovery

Explain how to rerun safely or recover from partial progress.

## Artifacts and Notes

Keep concise evidence here.

## Interfaces and Dependencies

Name commands, files, APIs, or systems this slice depends on.
