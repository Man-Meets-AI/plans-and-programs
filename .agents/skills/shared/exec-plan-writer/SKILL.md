---
name: exec-plan-writer
description: Use when a scoped task should become one self-contained ExecPlan under docs/exec-plans.
---

# ExecPlan Writer

Write one ExecPlan that a fresh agent can execute without chat history.

## Use When

- the work is approved or scoped enough to plan
- the task needs milestones, validation, or recovery guidance
- the plan should live under `docs/exec-plans/active/`

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/exec-plans/PLANS.md`.
3. Inspect the repo surfaces the plan will touch.
4. Write exactly one plan using the required frontmatter and section order.
5. Make the plan novice-readable and validation-focused.
6. Run `bun run plans:lint` or the local equivalent before returning.

## Prompt Asset

Use `docs/prompts/exec-plan-writer.md` for the copy-paste prompt.
