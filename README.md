# Programs, ExecPlans, And Agent Loops

![Plans & Programs](./assets/plans-and-programs.png)

This repo is a starter kit for teaching agents how to plan and execute real work through durable Markdown artifacts.

It is intentionally small. You can fork it, copy the folders into an existing project, or use it as a reference while building your own agent-ready workflow.

## The Primitives

This starter is based on the same core idea OpenAI describes in ["Harness engineering: leveraging Codex in an agent-first world"](https://openai.com/index/harness-engineering/): the repo needs to become legible to agents. A short `AGENTS.md` should act as a table of contents, durable knowledge should live in structured docs, and execution plans should be checked into the repository so agents can operate from files instead of chat memory.

OpenAI's article describes a repo layout with `docs/exec-plans/active/` and `docs/exec-plans/completed/`, and explains that complex work is captured in execution plans with progress and decision logs. This repo packages that pattern into a small cloneable starter.

### Program

A Program is the durable home for a larger initiative that will take more than one implementation slice.

Use a Program when the work has multiple phases, multiple agents, research that must not be lost, or a sequence that needs to survive beyond one chat session.

A Program answers:

- what larger initiative is underway
- what research and decisions shaped it
- which ExecPlans belong to it
- what has already landed
- what the next slice should be

Program packets live under:

```text
docs/programs/active/<YYYY-MM-DD-program-id>/
docs/programs/completed/<YYYY-MM-DD-program-id>/
```

### ExecPlan

An ExecPlan is the execution contract for one bounded slice of work.

Use an ExecPlan when a fresh coding agent needs enough context to implement, validate, and close out a change without reading chat history.

An ExecPlan answers:

- what outcome the slice must produce
- what is in scope and out of scope
- what files or systems matter
- what steps to take
- what commands prove the work
- what happened during execution

ExecPlans live under:

```text
docs/exec-plans/active/
docs/exec-plans/completed/
```

### Skills

Skills are reusable workflow packages that teach an agent when and how to perform a repeatable task.

This repo includes small skill wrappers under `.agents/skills/shared/` for:

- `exec-plan-writer`
- `exec-plan-griller`
- `exec-plan-execute`
- `exec-plan-validate`
- `program-planning-refresh`

They point back to the docs contracts instead of hiding the workflow in chat.

## How Programs Work

Programs are the piece most people skip too long. Use one when the work is bigger than a single ExecPlan.

### Step 1: Create The Program Folder

Create a folder under `docs/programs/active/`:

```text
docs/programs/active/2026-04-29-improve-onboarding/
```

The folder name is:

```text
YYYY-MM-DD-program-id
```

The `program_id` in `program.md` should match the folder slug after the date:

```yaml
program_id: improve-onboarding
```

### Step 2: Add The Program Packet

A Program packet is more than `program.md`. It keeps the reasoning around the initiative together:

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

### Step 3: Point At The Current Brief

`current-planning-brief.txt` contains exactly one filename:

```text
planning-brief-1.md
```

The pointer can move as the Program evolves. The planning brief files are immutable snapshots.

### Step 4: Write One Child ExecPlan

Create one ExecPlan under `docs/exec-plans/active/`:

```text
docs/exec-plans/active/2026-04-29-add-empty-onboarding-state.md
```

If it belongs to a Program, stamp the exact immutable brief path:

```yaml
program_id: improve-onboarding
planning_brief: docs/programs/active/2026-04-29-improve-onboarding/planning-brief-1.md
```

Never use `current-planning-brief.txt` as `planning_brief`.

### Step 5: Run The ExecPlan Loop

Use:

```text
writer -> griller -> execute -> validate
```

Keep the ExecPlan current while the work changes. The file should tell the next agent what happened without needing the chat.

### Step 6: Refresh The Program

After the child ExecPlan lands:

1. Update `program.md`.
2. Move the child ExecPlan from `active/` to `completed/` if it is truly complete.
3. Record decisions, validation, and new risks.
4. Write `planning-brief-2.md` if more work remains.
5. Update `current-planning-brief.txt` to `planning-brief-2.md`.
6. Choose the next child ExecPlan.

### Step 7: Complete The Program

Move the whole Program folder to `docs/programs/completed/` only when:

- no required next slice remains
- `completed_at` is filled
- `post_build_recap` is filled
- `Outcomes & Retrospective` tells the truth
- `npm run programs:lint` passes

## The Loop

Use this sequence for serious work:

1. Create or refresh a Program when the initiative spans several slices.
2. Write one ExecPlan for the next slice.
3. Grill the ExecPlan until scope, sequencing, and validation are clear.
4. Execute the plan in small validated increments.
5. Validate the finished slice against real proof commands.
6. Update the Program with what changed and choose the next slice.

The core loop is:

```text
Program -> ExecPlan Writer -> ExecPlan Griller -> Execute -> Validate -> Program Refresh
```

## Start Here

Read these files in order:

1. [AGENTS.md](./AGENTS.md)
2. [docs/index.md](./docs/index.md)
3. [docs/adoption.md](./docs/adoption.md)
4. [docs/programs/README.md](./docs/programs/README.md)
5. [docs/exec-plans/README.md](./docs/exec-plans/README.md)
6. [docs/prompts/README.md](./docs/prompts/README.md)

Then inspect the completed seed Program:

- [docs/programs/completed/2026-04-29-teaching-starter-seed/program.md](./docs/programs/completed/2026-04-29-teaching-starter-seed/program.md)
- [docs/exec-plans/completed/2026-04-29-seed-program-execplan-starter.md](./docs/exec-plans/completed/2026-04-29-seed-program-execplan-starter.md)

## Copy This Into Your Project

For the smallest useful adoption, copy:

```text
AGENTS.md
docs/programs/
docs/exec-plans/
docs/prompts/
.agents/skills/shared/
scripts/validate.mjs
package.json
```

Then update `AGENTS.md` and `package.json` for your project commands.

## Markdown And Frontmatter Linting

This starter includes a no-dependency validator:

```bash
npm run validate
npm run programs:lint
npm run plans:lint
```

What it checks:

- required starter files exist
- Program packet files exist
- Program frontmatter has required keys
- ExecPlan frontmatter has required keys
- required Program and ExecPlan sections exist in order
- completed examples are marked complete truthfully
- Markdown files avoid tabs and CRLF line endings

The validator lives at [scripts/validate.mjs](./scripts/validate.mjs).

This is intentionally not a full prose linter. For editor feedback, install the recommended VS Code extensions in [.vscode/extensions.json](./.vscode/extensions.json). The workspace also includes:

- [.markdownlint.json](./.markdownlint.json) for Markdown style rules
- [schemas/program-frontmatter.schema.json](./schemas/program-frontmatter.schema.json) for Program frontmatter
- [schemas/exec-plan-frontmatter.schema.json](./schemas/exec-plan-frontmatter.schema.json) for ExecPlan frontmatter

VS Code cannot natively validate YAML frontmatter inside Markdown with the same precision as a standalone script, so treat `npm run validate` as the source of truth. The schemas document the required keys and help when copying frontmatter into YAML-aware tools.

## Commands

This starter uses zero dependencies.

```bash
npm run validate
npm run programs:lint
npm run plans:lint
```

The validation script checks the required contracts, templates, skill files, and completed seed artifacts.
