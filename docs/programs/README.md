# Programs

Programs are durable initiative folders for work that spans multiple ExecPlans.

Use a Program when:

- the work will take several slices
- several agents may touch it
- research or decisions must survive across sessions
- you need a durable ledger of what happened and what comes next

## Folder Shape

```text
docs/programs/active/<YYYY-MM-DD-program-id>/
  program.md
  research-pass-*.md
  normalized-pass-*.md
  converged-decision-packet.md
  dependency-graph.md
  plan-split-recommendation.md
  cross-repo-review.md
  planning-brief-1.md
  current-planning-brief.txt

docs/programs/completed/<YYYY-MM-DD-program-id>/
  ...
```

`current-planning-brief.txt` contains one filename, such as:

```text
planning-brief-1.md
```

Child ExecPlans must point to the immutable planning brief file, not the pointer file.

## Loop

1. Read `program.md`.
2. Resolve `current-planning-brief.txt`.
3. Write one child ExecPlan from the current brief.
4. Grill the ExecPlan.
5. Execute and validate the child slice.
6. Write the next `planning-brief-N.md`.
7. Refresh `program.md`.
8. Repeat until the Program is complete.

## Contract

Read [PROGRAMS.md](./PROGRAMS.md) before authoring or changing Program packets.

## Examples

- [Completed seed Program](./completed/2026-04-29-teaching-starter-seed/program.md)

