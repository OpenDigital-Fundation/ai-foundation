# Decision questions and spec standards

Part of workflow:brainstorming: how to turn rough intent into a precise spec, and which questions are worth asking.

## Ask questions that force a product decision

Ask only when the answer changes what is built or its risk, and the codebase or common practice cannot answer it. Good questions:

- What happens to existing records when this entity is deleted?
- Is this a historical snapshot or always the current state?
- Who can perform this transition?
- Does this action need an audit history?
- Is the relationship required or optional?

Do not outsource routine engineering judgement to the user.

## Shape of the spec

1. Restate the outcome in one sentence.
2. Identify the product object, actors, state transitions, permissions and data ownership.
3. Separate confirmed requirements from assumptions; turn an assumption into a question only when its answer changes implementation or risk.
4. Cover: context, objective, functional scope, non-functional requirements, data and API impact, edge cases, acceptance criteria, open questions.

## Spec standards

- Use precise verbs: create, edit, archive, delete, move, approve, reject, restore.
- Call out destructive behaviour explicitly. Prefer archive or soft delete when records have business history, unless told otherwise.
- Make acceptance criteria testable: user-visible behaviour, API behaviour, data persistence, validation failures, migration and backward compatibility, reporting impact.

## Issue shape

When the spec becomes an issue, write it so a teammate can start without the conversation:

```markdown
## Context
## Objective
## Scope
## Acceptance criteria
## Decision questions
## Technical notes
```
