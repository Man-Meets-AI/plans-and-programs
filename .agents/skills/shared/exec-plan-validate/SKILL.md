---
name: exec-plan-validate
description: Use after implementation to prove an ExecPlan outcome and update the plan with evidence.
---

# ExecPlan Validate

Validate a completed or nearly completed ExecPlan against real proof.

## Use When

- code or docs were implemented from an ExecPlan
- the plan needs completion evidence
- the user wants to know whether completion stands

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/exec-plans/PLANS.md`.
3. Read the target ExecPlan.
4. Run the plan's `### Test Commands`.
5. Add focused checks when the plan's commands are not enough.
6. Update the ExecPlan with exact commands, results, skipped checks, and remaining risks.
7. Mark complete only when evidence supports it.

## Prompt Asset

Use `docs/prompts/exec-plan-validate.md` for the copy-paste prompt.

