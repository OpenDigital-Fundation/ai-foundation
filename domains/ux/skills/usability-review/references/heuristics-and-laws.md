# Heuristics, principles and laws of UX

Reference for `ux:usability-review`. Use it to name the principle a finding breaks and to argue a fix. Cite the principle in the finding; never use it as the only evidence that something is a problem.

## How much weight each kind of reference carries

| Kind | Examples | What it is | How to use it |
|---|---|---|---|
| Heuristic | Nielsen's ten, Shneiderman's eight golden rules | Expert rules of thumb for spotting problems | Sweep screens; every finding still needs an observed or walked-through failure |
| Design principle | Norman's affordances, signifiers, mapping, feedback | Vocabulary for why an interaction works or fails | Explain the cause of a finding and the shape of the fix |
| Empirical regularity | Fitts's law, Hick–Hyman law | Measured relationships, valid within their experimental conditions | Predict direction of effect (bigger, closer, fewer); do not quote numbers outside their context |
| Observed tendency | Jakob's law, serial position, peak-end, Zeigarnik, aesthetic-usability | Recurring behaviour, often from one or a few studies | Treat as a hypothesis to test, not a rule |
| Normative standard | WCAG 2.2, ISO 9241, ABNT NBR 17225 | Formal, verifiable criteria | Cite the criterion ID; see `accessibility:wcag-accessibility` (`references/standards-map.md`) |

Many items called "laws of UX" are tendencies, not laws. Pareto's 80/20, Miller's 7 ± 2 and the 400 ms Doherty threshold are frequently misquoted as limits; verify against the product's own data before deciding with them.

## Nielsen's ten usability heuristics

| # | Heuristic | Typical failure | Typical fix |
|---|---|---|---|
| 1 | Visibility of system status | Spinner with no end; a save that gives no confirmation | Progress with steps or percentage; explicit success state |
| 2 | Match between system and the real world | Internal jargon, codes or database names in labels | Users' words and order; dates and numbers in local format |
| 3 | User control and freedom | No cancel, no back, irreversible action | Undo, cancel, draft, confirmation only where the action cannot be undone |
| 4 | Consistency and standards | Same action named or placed differently across screens | One term and placement per action; follow platform conventions |
| 5 | Error prevention | Free text where a choice would do; destructive button next to the primary one | Constrain input, sensible defaults, separate destructive actions |
| 6 | Recognition rather than recall | User must remember a code from a previous screen | Show the information where it is needed; recent items, autocomplete |
| 7 | Flexibility and efficiency of use | Experts forced through the novice path | Shortcuts, bulk actions, saved preferences that do not hide the basic path |
| 8 | Aesthetic and minimalist design | Secondary content competing with the task | Remove or demote what the current task does not need |
| 9 | Help users recognise, diagnose and recover from errors | "Invalid input", error codes, cleared forms | Say what went wrong, where, and how to fix it; keep what the user typed |
| 10 | Help and documentation | Help only in a separate manual | Contextual help at the point of difficulty; searchable, task-oriented |

## Shneiderman's eight golden rules

Strive for consistency; seek universal usability; offer informative feedback; design dialogs to yield closure; prevent errors; permit easy reversal of actions; keep users in control; reduce short-term memory load. They overlap with Nielsen; they add emphasis on closure (a clear end to each task) and on universal usability (novices, experts, disabilities, devices), which helps in complex, data-heavy software.

## Norman's principles of interaction design

| Principle | Question to ask of each control |
|---|---|
| Affordance | What actions does this element allow? |
| Signifier | What tells the user that the action exists and where to do it? |
| Mapping | Does the control's layout correspond to its effect (order, direction, grouping)? |
| Feedback | Is there an immediate, perceptible response to every action? |
| Constraints | What stops the wrong action from being possible at all? |
| Conceptual model | Can the user form a correct picture of how the system works? |
| Discoverability | Can the user find what is possible without instructions? |

Most "users are confused" findings are missing signifiers or a wrong conceptual model, not missing documentation.

## Laws and effects, with their use in review

### Decision, memory and effort

| Name | What it says | Use in review | Caveat |
|---|---|---|---|
| Hick–Hyman law | Decision time grows with the number and uncertainty of choices | Flag long flat menus and many equal-weight options; group, order and default | Applies to choosing among known options, not to search or scanning |
| Miller's 7 ± 2 | Working memory holds few items at once | Prefer recognition and chunking over remembering | Not a cap on menu length |
| Chunking | Grouped information is easier to process | Split long forms into labelled sections; format long numbers | — |
| Cognitive load | Mental effort is limited and is spent by the task, the interface and distractions | Remove extraneous load: noise, unclear wording, needless steps | — |
| Jakob's law | Users expect your product to work like the others they use | Use common patterns for navigation, forms, carts and settings | Novel patterns need a strong reason and a test |
| Tesler's law (conservation of complexity) | Some complexity cannot be removed, only moved | Ask who carries it; move it into the system (defaults, inference, validation) | — |
| Occam's razor | Prefer the simplest design that does the job | Remove steps and components that change nothing | — |
| Pareto principle | A few causes often account for most effects | Prioritise the most-used flows and most frequent errors | 80/20 is an illustration; measure the real split |
| Choice overload | Too many alternatives can stall a decision | Recommend or pre-select while keeping choice | Effect size varies widely across studies |

### Interaction, speed and behaviour

| Name | What it says | Use in review | Caveat |
|---|---|---|---|
| Fitts's law | Time to reach a target grows with distance and shrinks with size | Make frequent and primary targets large and near; use screen edges and corners on desktop | Minimum target sizes: see `ui:design-system` (`references/platform-guidelines.md`) |
| Doherty threshold | Productivity rises when the system responds faster than the user waits (about 400 ms in the original study) | Give immediate feedback; show progress for anything slower | Use the product's own latency budget |
| Postel's law | Be liberal in what you accept, conservative in what you send | Accept phone numbers, tax IDs and dates in any common format; normalise on save | Never loosen validation that protects security or data integrity |
| Parkinson's law | Work expands to fill the time available | Short, focused flows; autofill; avoid open-ended steps | — |
| Goal-gradient effect | Effort increases as the goal looks closer | Progress indicators, especially near the end | — |
| Active user paradox | Users start using before reading instructions | Make the interface self-explanatory; put help in context | — |

### Attention, perception and memory of the experience

| Name | What it says | Use in review | Caveat |
|---|---|---|---|
| Von Restorff (isolation) effect | The item that differs is remembered | One visually distinct primary action per view | Several "distinct" items cancel each other |
| Serial position effect | First and last items are recalled best | Put key items at the start and end of lists and navigation | — |
| Peak-end rule | Experiences are judged by their peak and their end | Invest in the hardest moment and in the confirmation screen | — |
| Zeigarnik effect | Unfinished tasks stay in mind | Save drafts and let users resume; show what is left | Replication is mixed |
| Aesthetic-usability effect | Attractive interfaces are perceived as easier | Visual quality matters, but test usability separately | Users may tolerate real problems in a pretty UI |
| Selective attention | People filter out what seems irrelevant to their goal | Do not hide critical messages in banner-like areas (banner blindness) | — |

## Applying them in a review

1. Walk the task first (SKILL.md § 2); principles explain findings, they do not create them.
2. For each finding, name one primary heuristic or principle; add a law only when it predicts the fix.
3. State the evidence: observed in a test, walked through, or inferred. Inferred findings are hypotheses.
4. Prefer the fix that removes the cause (signifier, mapping, constraint) over one that adds explanation.

## Sources

- Nielsen Norman Group, [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/) (1994, updated 2020).
- Ben Shneiderman, [The Eight Golden Rules of Interface Design](https://www.cs.umd.edu/users/ben/goldenrules.html).
- Don Norman, *The Design of Everyday Things*, revised edition (2013).
- Jon Yablonski, [Laws of UX](https://lawsofux.com/).
