# Spec — <feature>

- **Domain:** <domain>
- **Status:** draft | approved
- **ADRs:** <links to the decisions this spec relies on>

## Problem

The problem from the user's perspective, and why it matters now.

## Goals, non-goals, anti-goals

- Goals: what success looks like.
- Non-goals: what this deliberately does not do.
- Anti-goals: what would make this a failure even if it technically works.

## User stories

1. As a <actor>, I want <capability>, so that <benefit>.

Cover every actor and path, including errors and edge cases.

## Approaches

The two or three ways considered, what each trades off, which was picked and why.

## Decisions

Modules to build or change and their interfaces, schema changes, API contracts, interactions.
No file paths or code, except a short snippet from a prototype that encodes a decision
more precisely than prose (a state machine, a schema, a type shape).

## Testing decisions

- What a good test is here: external behaviour, not implementation details.
- The seams where the feature is tested: prefer existing seams, and the highest one possible.
- Prior art: similar tests in the codebase.

## Acceptance criteria

Numbered, verifiable statements. Each maps to at least one test or check.

## Out of scope

## Left to the builder

Decisions the builder may make without coming back.
