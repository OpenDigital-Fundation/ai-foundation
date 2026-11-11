# Codebase design — poka yoke

Part of `architecture:codebase-design`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## Poka-Yoke: Make the Mistake Unsayable

<!-- source: github/awesome-copilot skills/poka-yoke/SKILL.md#designing-something-new,evidence-and-its-limits,axis-1-what-happens-when-the-mistake-occurs,after-an-incident -->

### Axis 1: what happens when the mistake occurs

Rank every finding on this ladder, and say which rung the current code sits on and which rung
your fix reaches.

| Rung | Name | Meaning |
|---|---|---|
| 1 | **Control** | The wrong action cannot be performed. Type error, database constraint, missing permission. |
| 2 | **Warning** | It is possible, but announces itself as it happens. A linter, a runtime assertion, a confirmation you cannot skip. |
| 3 | **Detection** | It happens, and you find out afterwards. Tests, logging, monitoring, code review. |
| 0 | **rung zero** | Telling people to be careful. Docs, comments, "please remember to". |

Detection is not failure; sometimes it is all that is available. But a plan that stops at
Detection should say so, rather than presenting it as prevention.

### Designing something new

Mistake-proofing is cheapest before the code has callers. Once it has them, every device is a
migration; before it has them, a device is free.

Work from the call site. A signature that reads fine in isolation often reads terribly where
it is used:

```python
# the mistake is expressible: nothing stops refunding an order that was never paid
def refund(order: dict) -> Refund:
    return payments.refund(order["payment_id"])

# the mistake is no longer expressible
def refund(order: PaidOrder) -> Refund: ...
```

The moves, roughly in order of how often they apply:

**Make invalid states unrepresentable.** A bag of optional fields where only certain
combinations are legal becomes a discriminated union where the illegal ones cannot be
constructed.

**Parse, don't validate.** Convert unstructured input into a type that carries proof at the
boundary, once, rather than re-checking the same string in nine places.

**Distinguish concepts that share a primitive.** `transfer(from: str, to: str)` accepts its
arguments transposed. Distinct types for the two concepts, or keyword-only parameters, make the
transposition a compile error.

**Encode the order.** When calls must happen in sequence, let each step return the type the
next step requires, so the wrong order does not typecheck.

**Make the destructive path narrower than the safe one.** A required, non-defaulting argument
for the scope of a delete. A default that means "nothing" rather than "everything".

Close by naming what the design now makes impossible, and, just as importantly, **what you
deliberately left possible and why**. A design whose limits are unstated will be trusted past
them.

### After an incident

Separate three things that get conflated, because the fix belongs to the third:

- **Defect** — what the user experienced.
- **Mistake** — the specific wrong action someone took.
- **Hazard** — the property of the system that made that mistake available.

Fixing the mistake fixes one case. Fixing the hazard fixes the class. Then **sweep**: the same
shape almost certainly exists elsewhere, and finding the second and third instance is the
difference between a patch and a lesson.

Attribute cause to the system rather than to a person. Not primarily for kindness: "they made a
mistake" is a complete-sounding explanation that predicts nothing and prevents nothing, and it
ends the investigation early.

### Evidence, and its limits

This method was benchmarked at 591 blind-graded runs across six model families, scored against
assertions written before the runs by a grader that never saw which configuration produced a
response. The behaviour it most reliably changes is stating what a design forecloses: **45% of
responses did that unprompted, 80% with the method applied**, across 132 graded verdicts.

That average conceals where the effect lives. Asked squarely to design an interface, models
already do it 77% of the time; the skills add eleven points. The large gains are in tasks
where nobody asked for a design review — writing an endpoint goes 14% to 79%, shipping an
agent feature 33% to 83%, building a form 29% to 64%.

Stated honestly, because the limits matter: every run was the first turn of a fresh session, so
this measures the ceiling rather than what survives a long working session. The comparison was
against no methodology at all, not against a different one, so it does not establish that
*this* method is what produced the gain. And the method costs something measurable: responses
became somewhat worse at spotting the specific defect already on the page while becoming better
at changing the shape that allowed it. If you want the bug in front of you found, use a
reviewer. If you want that class of bug to stop being expressible, use this.

Raw runs, the harness and the assertion checklists are at
<https://github.com/rainmanjam/poka-yoke>.
