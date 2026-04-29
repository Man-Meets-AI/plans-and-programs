# Cross-Repo Review

The starter is intentionally independent from any existing private project.

It keeps the reusable patterns:

- Programs are packet folders.
- ExecPlans are self-contained slice contracts.
- Planning briefs are immutable.
- `current-planning-brief.txt` is mutable and should not be used as ExecPlan provenance.
- Skills are lightweight workflow wrappers under `.agents/skills`.
- Validation should be runnable by a new contributor.

It omits project-specific runtime automation, role systems, release gates, product code, and private examples.

