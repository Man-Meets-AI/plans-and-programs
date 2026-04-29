# ExecPlan Validate Prompt

Use this prompt after an ExecPlan has been executed and needs proof.

```text
Read AGENTS.md, docs/exec-plans/PLANS.md, and this ExecPlan:

<PLAN_PATH>

Validate the intended outcome against the repo-owned proof surface. Run the Test Commands from the plan first. Add any focused runtime or manual checks needed to prove the behavior.

Update the ExecPlan with:

- commands run
- results observed
- artifacts or evidence
- any skipped checks and exact reasons
- whether completion still stands

Do not mark the plan complete unless the proof supports it.
```

