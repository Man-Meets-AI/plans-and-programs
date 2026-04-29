---
program_id: teaching-starter-seed
title: Teaching Starter Seed
status: complete
created_at: 2026-04-29
completed_at: 2026-04-29
summary: Seed this repo as a public starter for Programs, ExecPlans, prompt loops, skills, and AGENTS routing.
post_build_recap: The starter now includes root onboarding, Program and ExecPlan contracts, templates, prompt assets, shared skill wrappers, a completed seed ExecPlan, and a no-dependency validator.
read_when:
  - Understanding how this starter was assembled.
  - Copying the Program and ExecPlan pattern into another project.
  - Extending the starter with more examples or automation.
---

# Teaching Starter Seed

This is a living initiative document.

This Program must be maintained in accordance with `docs/programs/PROGRAMS.md`.

## Purpose / Big Picture

This initiative turns an empty directory into a public teaching starter for durable agent workflows. A learner should be able to clone or fork the repo, understand the Program and ExecPlan primitives, copy the templates into their own project, and run validation without extra setup.

## Program Inputs

The Program packet lives at `docs/programs/completed/2026-04-29-teaching-starter-seed/`.

The packet inputs are:

- `research-pass-teaching-starter.md`
- `normalized-pass-teaching-starter.md`
- `converged-decision-packet.md`
- `dependency-graph.md`
- `plan-split-recommendation.md`
- `cross-repo-review.md`
- `planning-brief-1.md`
- `current-planning-brief.txt`

## Current State

The starter is seeded. Root onboarding, docs contracts, templates, prompts, skills, a completed child ExecPlan, and validation all exist.

## Progress

- [x] 2026-04-29: Created root onboarding and agent instructions.
- [x] 2026-04-29: Added Program and ExecPlan contracts.
- [x] 2026-04-29: Added Program and ExecPlan templates.
- [x] 2026-04-29: Added prompt assets for the loop.
- [x] 2026-04-29: Added shared skill wrappers.
- [x] 2026-04-29: Added the completed seed child ExecPlan.
- [x] 2026-04-29: Added no-dependency validation.

## Decision Log

Decision: Keep the starter project-agnostic.
Rationale: Students should not need access to any existing private repository to understand or reuse the primitives.
Date: 2026-04-29

Decision: Use a completed Program as the worked example.
Rationale: The fastest way to understand the lifecycle is to inspect a finished packet and its child ExecPlan.
Date: 2026-04-29

Decision: Use no-dependency validation.
Rationale: A cloneable starter should work immediately with the local Node runtime.
Date: 2026-04-29

## Slice Ledger

Active child ExecPlans:

- None.

Completed child ExecPlans:

- `docs/exec-plans/completed/2026-04-29-seed-program-execplan-starter.md`

## Next Slice

No required next slice remains inside this Program.

Future improvements should use new ExecPlans or a new Program if they add a website, CLI, GitHub Actions, richer examples, or package publishing.

## Risks and Watchpoints

Do not turn this starter into a private-repo mirror. The teaching value comes from small portable artifacts.

Do not hide the workflow inside a script. The Markdown contracts should remain readable and copyable.

Do not mark future Programs complete without validation evidence and a retrospective.

## Outcomes & Retrospective

The seed work created a complete starter surface for teaching Programs, ExecPlans, prompt loops, skill wrappers, and root agent routing. The starter stays small enough to copy into another project while still showing the full lifecycle through a completed Program and child ExecPlan.

## Validation and Acceptance

The Program is accepted when the starter contains the required docs, templates, prompts, skill wrappers, example packet, completed child ExecPlan, and validation command.

Validation command:

```bash
npm run validate
```

## Artifacts and Notes

Core starter files:

- `README.md`
- `AGENTS.md`
- `docs/programs/PROGRAMS.md`
- `docs/exec-plans/PLANS.md`
- `docs/prompts/`
- `.agents/skills/shared/`
- `scripts/validate.mjs`

## Interfaces and Dependencies

The starter depends on Node for `scripts/validate.mjs`. It has no package dependencies.

