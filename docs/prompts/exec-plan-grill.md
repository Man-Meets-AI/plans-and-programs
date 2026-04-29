# ExecPlan Griller Prompt

Use this prompt after an ExecPlan exists and before implementation starts.

```text
Read AGENTS.md, docs/exec-plans/PLANS.md, and the target ExecPlan.

Grill this ExecPlan:

<PLAN_PATH>

Inspect the real repo surfaces it touches. Find hidden assumptions, vague scope, weak validation, missing recovery paths, missing interfaces, sequencing risks, and out-of-scope work that could be accidentally absorbed.

Update the plan in place with focused edits. Preserve the target path. Do not implement code.

The grill is complete only when a fresh agent could execute the plan without chat history and without guessing the proof path.

Run plan validation if available and report the result.
```

