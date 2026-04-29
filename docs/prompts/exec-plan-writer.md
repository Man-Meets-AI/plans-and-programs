# ExecPlan Writer Prompt

Use this prompt when a scoped task should become one self-contained ExecPlan.

```text
Read AGENTS.md and docs/exec-plans/PLANS.md.

Write exactly one ExecPlan for this task:

<TASK>

Target path:

docs/exec-plans/active/YYYY-MM-DD-<slug>.md

Before writing, inspect the files, docs, tests, and commands the plan will touch. Resolve ambiguity from the repo before asking questions.

The plan must be self-contained for a fresh agent with no chat history. Use the required frontmatter and section order from docs/exec-plans/PLANS.md. Include exact scope, out-of-scope boundaries, milestones, concrete steps, validation commands, recovery notes, and interfaces.

After writing, run the repo's plan validation command if available. If validation cannot run, state why.
```

