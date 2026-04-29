# Adoption Guide

Use this guide to bring Programs and ExecPlans into another project quickly.

## Fastest Path

Copy these paths into your project:

```text
AGENTS.md
docs/programs/
docs/exec-plans/
docs/prompts/
.agents/skills/shared/
scripts/validate.mjs
package.json
```

If your project already has a `package.json`, copy only the scripts you need:

```json
{
  "scripts": {
    "validate": "bun scripts/validate.mjs",
    "programs:lint": "bun scripts/validate.mjs --programs",
    "plans:lint": "bun scripts/validate.mjs --plans",
    "lint": "oxlint . --deny-warnings",
    "format": "oxfmt scripts/validate.mjs package.json .markdownlint.json .oxlintrc.json .oxfmtrc.json .vscode/settings.json .vscode/extensions.json schemas/program-frontmatter.schema.json schemas/exec-plan-frontmatter.schema.json",
    "format:check": "oxfmt --check scripts/validate.mjs package.json .markdownlint.json .oxlintrc.json .oxfmtrc.json .vscode/settings.json .vscode/extensions.json schemas/program-frontmatter.schema.json schemas/exec-plan-frontmatter.schema.json",
    "check": "bun run validate && bun run lint && bun run format:check"
  }
}
```

Then edit:

- `AGENTS.md`: add your package manager, test commands, framework rules, and nearest-doc routing.
- `docs/exec-plans/templates/exec-plan.md`: replace the sample validation command with your real local proof command.
- `docs/programs/templates/program.md`: add any project-specific ownership or release fields you care about.

## First Program

Use a Program when the initiative needs more than one ExecPlan.

Example:

```text
docs/programs/active/2026-04-29-improve-onboarding/
```

Start with:

```text
program.md
research-pass-onboarding.md
normalized-pass-onboarding.md
converged-decision-packet.md
dependency-graph.md
plan-split-recommendation.md
cross-repo-review.md
planning-brief-1.md
current-planning-brief.txt
```

Keep `current-planning-brief.txt` to one line:

```text
planning-brief-1.md
```

## First ExecPlan

Use an ExecPlan for the next shippable slice.

Example:

```text
docs/exec-plans/active/2026-04-29-add-empty-onboarding-state.md
```

If the plan belongs to a Program, include:

```yaml
program_id: improve-onboarding
planning_brief: docs/programs/active/2026-04-29-improve-onboarding/planning-brief-1.md
```

Do not point at `current-planning-brief.txt`.

## Linting In Your Project

Keep the validation script even if you later add a full Markdown linter.

The starter's validator checks structure that generic Markdown linters do not understand:

- Program packet completeness
- frontmatter keys
- required section order
- immutable `planning_brief` usage
- completed-state truth

Run:

```bash
bun run validate
bun run lint
bun run format:check
```

If you use VS Code, copy `.vscode/`, `.markdownlint.json`, `.oxlintrc.json`, `.oxfmtrc.json`, and `schemas/` too.

## Operating Cadence

Use this cadence:

1. Write the ExecPlan.
2. Grill it.
3. Execute one milestone.
4. Validate the milestone.
5. Update the ExecPlan.
6. Repeat until complete.
7. Refresh the Program.

The durable artifact is the file, not the chat.

## What To Customize

Customize:

- validation commands
- release commands
- ownership fields
- docs routing
- project-specific risk checks
- skill descriptions

Do not customize away:

- active versus completed lifecycle
- Program versus ExecPlan distinction
- immutable planning brief provenance
- living `Progress`, `Decision Log`, validation, and retrospective sections
