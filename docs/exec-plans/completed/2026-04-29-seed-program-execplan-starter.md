---
title: Seed Program And ExecPlan Starter
status: complete
created_at: 2026-04-29
completed_at: 2026-04-29
summary: Create a cloneable teaching starter for Programs, ExecPlans, prompt loops, skills, and AGENTS routing.
post_build_recap: The repo now includes root onboarding, Program and ExecPlan docs, templates, prompts, shared skills, a completed seed Program, and validation.
program_id: teaching-starter-seed
planning_brief: docs/programs/completed/2026-04-29-teaching-starter-seed/planning-brief-1.md
read_when:
  - Reviewing the starter seed slice.
  - Copying the structure into another project.
  - Adding the next educational example.
---

# Seed Program And ExecPlan Starter

This is a living execution plan.

This ExecPlan must be maintained in accordance with `docs/exec-plans/PLANS.md`.

## Purpose / Big Picture

The repo should teach durable agent workflow primitives in a way students can immediately clone, fork, or copy into an existing project. After this slice, the starter should explain Programs, ExecPlans, prompts, skills, and AGENTS routing without relying on any private codebase.

## Progress

- [x] 2026-04-29: Added root README and AGENTS instructions.
- [x] 2026-04-29: Added Program and ExecPlan contracts.
- [x] 2026-04-29: Added templates for new Programs and ExecPlans.
- [x] 2026-04-29: Added prompt assets for writer, griller, execute, validate, and Program refresh.
- [x] 2026-04-29: Added shared skill wrappers.
- [x] 2026-04-29: Added the completed seed Program packet.
- [x] 2026-04-29: Added validation script and package scripts.

## Surprises & Discoveries

The starter directory began empty and was not a git repository. That made a project-agnostic seed cleaner than adapting existing project files.

## Decision Log

Decision: Teach from a self-contained starter instead of private repo examples.
Rationale: Students should be able to understand and reuse the pattern with only this repository.
Date: 2026-04-29

Decision: Include a completed Program and child ExecPlan as examples.
Rationale: A finished artifact teaches completion rules better than a template alone.
Date: 2026-04-29

## Outcomes & Retrospective

The starter now has the core artifact set needed to teach and reuse the loop. The examples are deliberately small and generic. Future slices can add richer examples, a website, GitHub Actions, or a packet-generation CLI.

## Context and Orientation

This repo is a docs-first teaching starter. The root README explains the primitives. `AGENTS.md` gives agents local rules. `docs/programs/` owns initiative-level Program packets. `docs/exec-plans/` owns slice-level execution plans. `docs/prompts/` owns copy-paste prompt assets. `.agents/skills/shared/` owns reusable skill wrappers.

### In Scope

Seed the public starter with docs, templates, prompts, shared skills, a completed Program, a completed child ExecPlan, and no-dependency Bun validation.

### Out Of Scope

Do not add a web app, package publishing, private repo examples, or runtime automation in this slice.

## Plan of Work

Create the root orientation files first, then add Program and ExecPlan contracts. Add templates and prompt assets after the contracts so they can point at the right source of truth. Add skill wrappers that reference the prompt assets. Finish with a completed seed Program, completed child ExecPlan, and validation script.

## Milestones

The first milestone is onboarding. It is complete when a learner can read the root README and understand the primitives.

The second milestone is contract shape. It is complete when Program and ExecPlan contract files define required frontmatter, sections, and lifecycle rules.

The third milestone is workflow reuse. It is complete when prompt assets and skill wrappers exist for writer, griller, execute, validate, and Program refresh.

The fourth milestone is proof. It is complete when `bun run validate` checks the starter structure.

## Concrete Steps

From repo root, inspect the structure:

```bash
find . -maxdepth 3 -type f | sort
```

Run validation:

```bash
bun run validate
bun run lint
bun run format:check
```

To start a new initiative, copy:

```text
docs/programs/templates/program.md
docs/exec-plans/templates/exec-plan.md
```

Then place them under the matching `active/` folders and update the frontmatter, body, planning brief, and validation commands.

## Validation and Acceptance

The slice is accepted when all starter docs, templates, prompts, skills, and completed examples exist and the validator passes.

### Test Commands

Run these commands from the repo root:

```bash
bun run validate
bun run programs:lint
bun run plans:lint
bun run lint
bun run format:check
```

## Idempotence and Recovery

The starter consists of Markdown files and one validation script. If a file is accidentally removed, restore it from the templates or rerun the seed work by recreating the required paths listed in `scripts/validate.mjs`.

## Artifacts and Notes

The completed Program packet is:

```text
docs/programs/completed/2026-04-29-teaching-starter-seed/
```

The completed child ExecPlan is:

```text
docs/exec-plans/completed/2026-04-29-seed-program-execplan-starter.md
```

## Interfaces and Dependencies

The validation interface is `scripts/validate.mjs`, exposed through Bun-backed `package.json` scripts. The starter assumes Bun is available and uses `oxlint` plus `oxfmt` as development dependencies for linting and formatting.
