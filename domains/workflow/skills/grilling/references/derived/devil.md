# Grilling — devil

Part of `workflow:grilling`. Adapted reference material; the owner procedure, project conventions, scope and authorization rules take precedence. Examples are not automatically executed.

## devil — the sign-off manager who rejects your approval request

<!-- source: davila7/claude-code-templates cli-tool/components/skills/productivity/devil/SKILL.md#role-based-framing -->

### Role-based framing

At the start, **infer** the user's role from conversation context — **do not ask.** Pick the most likely role, declare it in the report's first line, and let the user correct you. Asking costs a round-trip before any value is delivered; declaring costs nothing when right and one re-request when wrong.

The review routine and ruling are identical regardless of role — **only the framing of the final "questions to forward" section** adapts to the role. Don't build separate modes; more branches means more weight.

**Read the signal from what the user says, not from what the document is.** The document is almost always a planner-authored spec, so "it's a 기획서, therefore the user is a planner" is a trap — engineers and designers bring in other people's specs constantly. Weigh these instead:

| Signal | Likely role |
|---|---|
| "내가 쓴", "공유하기 전에", "빠진 거 없나" — ownership of the doc | Planner (self-review) |
| "받은 스펙", "구현해도 되나", "뭘 물어봐야 하나" — about to build it | Engineer |
| "어떤 화면 그려야", "상태 뭐뭐 있나" — about to draw it | Designer |
| No signal at all (bare invocation with just a doc) | **Neutral** — do not guess from the document type |

When there's no signal, use the neutral framing (safeguard 2 below) rather than defaulting to a role. Priority: **confident role > neutral > wrong framing.**

| User | Scenario | Recipient of "questions to forward" |
|------|----------|-------------------------------------|
| Planner / PM | Self-review before sharing | Themselves (converted into a fill-in TODO list) |
| Engineer | Validate a received spec | The planner (a polite question list) |
| Designer | Confirm which screens to draw | The planner + themselves (list of states needing a mockup: empty/error/loading/max) |

**For a planner (self-review), attach a "pass example" spec sentence to each finding.** A planner who receives "pass condition: what must be written" still gets stuck at "…so what do I actually write?" So for each Major, offer an optional example sentence they can paste straight into the doc — this mirrors the engineer's layer tag. Example: for "no failure handling," add *"e.g. 'If the accrual API returns 5xx/timeout, roll the button back and show the toast «Please try again in a moment».'"* Keep it an example, not a mandate — the planner picks the wording; you just remove the blank-page cost.

**For an engineer, attach a layer tag to each finding.** What an engineer really needs is "which layer does this hole shake = must I ask now to start, or can I fill it in later?" Tag each finding with one **or more** of: `[UI]` (screen state/branching) · `[API]` (request/response contract, endpoints) · `[DATA]` (DB schema, migration, consistency) · `[POLICY]` (calculation/decision rules — who qualifies, how much, under what conditions). A hole that shakes two layers gets two tags; don't force it into one.

For `[UI]`/`[API]`/`[DATA]` the detected domain modules usually hand you the tag (mobile→UI, backend→API·DATA). **`[POLICY]` has no module to inherit from — it's the one you must judge fresh.** It's also the one most likely to be the real Blocker: a missing screen state costs a redesign, but a missing rule about *who gets how many points when* corrupts data you can't backfill.

Items tagged `[API]`/`[DATA]`/`[POLICY]` are usually required before starting (you can't design the DTO, the schema, or the calculation without them); `[UI]` items can often proceed in parallel.

**For a designer, the list is the star, not the ruling.** A designer has no authority to reject a document; what they need is "the list of screens I must draw right now that have no mockup." So don't slap a big Approve/Reject label on the title (mention it in one line in the summary if you must), and put the output's weight on **organizing the "missing screens to draw" list by screen state (empty / loading / error / max·truncation / variants)**. Each item must be concrete about "which screen" so the designer can start the mockup immediately.

#### Two safeguards against misjudging the role

1. **Declare the lens**: state the inferred role in the report's first line. This turns a misjudgment from a silent failure into a visible one, lowering the cost from "the whole output is wrong" to "one re-request." Since the ruling and reasons are role-agnostic, a re-request only needs the final section re-generated.
2. **Neutral fallback**: when the signal table above yields nothing, use neutral framing instead of a guessed one — "Forward these questions to the relevant party, or fill them in yourself." A neutral report is useful to all three roles; a confidently wrong lens is useful to none.
