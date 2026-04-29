# ExecPlan Execute Prompt

Use this prompt when an approved ExecPlan should be implemented.

```text
Read AGENTS.md, docs/exec-plans/PLANS.md, and this ExecPlan:

<PLAN_PATH>

Treat the ExecPlan as the source of truth. Identify the active milestone, choose the smallest validatable slice, implement it, run the narrowest relevant validation, and update the ExecPlan before moving on.

If validation fails, stop forward progress, diagnose, repair, and rerun validation.

If the real implementation changes scope or sequence, update the ExecPlan first.

When the plan is complete, fill completed_at, post_build_recap, Outcomes & Retrospective, validation evidence, and any remaining risks.
```

