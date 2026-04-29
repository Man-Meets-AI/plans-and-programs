# ExecPlans

ExecPlans are self-contained execution plans for one bounded slice of work.

Use an ExecPlan when:

- the work is too risky or complex for one chat reply
- a future agent needs to resume from a file
- validation must be explicit
- scope boundaries matter

## Folder Shape

```text
docs/exec-plans/active/YYYY-MM-DD-slice-name.md
docs/exec-plans/completed/YYYY-MM-DD-slice-name.md
```

Keep active plans under `active/` until the work is implemented, validated, and retrospectively documented.

## Loop

1. Write the ExecPlan.
2. Grill it for hidden assumptions.
3. Execute the smallest validatable slice.
4. Update the plan as reality changes.
5. Validate with real commands.
6. Complete the plan only when proof and retrospective are present.

## Contract

Read [PLANS.md](./PLANS.md) before authoring or changing ExecPlans.

## Examples

- [Completed seed ExecPlan](./completed/2026-04-29-seed-program-execplan-starter.md)

