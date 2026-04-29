# Agent Instructions

This repo teaches Program and ExecPlan workflows. Keep changes simple, explicit, and easy for a newcomer to copy into another project.

## Routing

- Read this file before meaningful work.
- Read [docs/index.md](./docs/index.md) before changing docs.
- Read [docs/programs/PROGRAMS.md](./docs/programs/PROGRAMS.md) before changing Program packets.
- Read [docs/exec-plans/PLANS.md](./docs/exec-plans/PLANS.md) before changing ExecPlans.
- Read the matching skill under `.agents/skills/shared/` before changing a skill wrapper.

## Core Rules

- Keep examples project-agnostic. Do not require access to any private repo.
- Preserve the distinction between Programs and ExecPlans.
- Programs coordinate multiple slices. ExecPlans execute one slice.
- Keep prompt and skill files short enough that users can adapt them.
- Prefer templates and worked examples over abstract explanation alone.
- Do not add dependencies unless the teaching value is worth the extra setup.

## Validation

Run the narrowest relevant command:

```bash
bun run validate
bun run programs:lint
bun run plans:lint
bun run lint
bun run format:check
```

If a behavior or contract changes, update the relevant README, template, prompt, and skill wrapper together.
