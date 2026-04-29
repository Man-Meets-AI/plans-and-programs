---
name: program-planning-refresh
description: Use after a child ExecPlan lands to refresh the owning Program and select the next slice.
---

# Program Planning Refresh

Refresh a Program after one child ExecPlan has landed.

## Use When

- a Program-linked ExecPlan completed
- the Program needs a new planning brief
- the next slice should be chosen from current evidence

## Procedure

1. Read `AGENTS.md`.
2. Read `docs/programs/PROGRAMS.md`.
3. Read the Program packet.
4. Read the completed child ExecPlan.
5. Update `program.md`.
6. Write the next `planning-brief-N.md` if work remains.
7. Update `current-planning-brief.txt`.
8. Complete the Program only when no required slice remains and the retrospective is truthful.
9. Run `npm run programs:lint` or the local equivalent before returning.

## Prompt Asset

Use `docs/prompts/program-planning-refresh.md` for the copy-paste prompt.

