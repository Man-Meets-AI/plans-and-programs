# Program Planning Refresh Prompt

Use this prompt after a child ExecPlan lands.

```text
Read AGENTS.md, docs/programs/PROGRAMS.md, docs/exec-plans/PLANS.md, and this Program:

<PROGRAM_PATH>

Read current-planning-brief.txt, then read the referenced planning-brief-N.md. Read the completed child ExecPlan.

Refresh the Program packet:

1. Update program.md with what landed.
2. Add the completed child ExecPlan to the Slice Ledger.
3. Record new decisions, risks, validation evidence, and outcomes.
4. Write the next planning-brief-(N+1).md if more work remains.
5. Update current-planning-brief.txt to the new brief filename.
6. If no required next slice remains, complete the Program only when the retrospective and validation evidence support it.

Run Program and plan validation if available.
```

