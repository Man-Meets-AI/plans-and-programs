---
name: exec-plan-griller
description: Use after an ExecPlan exists and before implementation starts, to stress-test scope, sequence, and proof.
---

# ExecPlan Griller

Harden one ExecPlan until it can be executed without guessing.

## Use When

- a plan exists but may be vague
- validation is weak
- boundaries are unclear
- the next agent should not rely on chat context

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/exec-plans/PLANS.md`.
3. Read the target ExecPlan.
4. Inspect the real repo surfaces it touches.
5. Tighten scope, out-of-scope boundaries, milestones, validation, recovery, and interfaces.
6. Do not implement the plan.
7. Run `bun run plans:lint` or the local equivalent before returning.

## Prompt Asset

Use `docs/prompts/exec-plan-grill.md` for the copy-paste prompt.
