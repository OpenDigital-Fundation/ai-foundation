# Management models, organisational laws and execution frameworks

Reference for `operations:project-management`. Use it to pick a method that fits the problem and to name the effect behind a recurring failure. None of these replaces data from the organisation itself.

## How much weight each item carries

| Kind | Examples | Use |
|---|---|---|
| Quantitative relationship | Little's law, diminishing returns | Holds under stated conditions; compute with it |
| Empirical tendency | Pareto distributions, Brooks's law, planning fallacy | Expect the direction; measure the size |
| Maxim or satire | Parkinson, Peter principle, Hofstadter, Chesterton's fence, Hanlon's razor | A prompt to check, not a finding |
| Method | PDCA, Lean, Six Sigma, TOC, Kanban, OKR, BSC | A way of working; judge it by results in context |

## Schools of management, in one line each

| School | Key figures | Idea that still matters |
|---|---|---|
| Scientific management | Frederick Taylor | Study the work before changing it; standardise what is repeatable |
| Classical administration | Henri Fayol | Management as planning, organising, commanding, coordinating and controlling |
| Bureaucracy | Max Weber | Rules and roles that are impersonal and predictable |
| Human relations | Elton Mayo | Social context and attention change performance |
| Management by objectives | Peter Drucker | Agree objectives and judge by results |
| Behavioural theory | Herbert Simon, Douglas McGregor | Bounded rationality; assumptions about people shape the system |
| Systems theory | Ludwig von Bertalanffy | Parts interact; optimise the whole, not each part |
| Contingency theory | Burns and Stalker | The right structure depends on environment and technology |
| Quality and learning | W. Edwards Deming, Peter Senge | Most problems are in the system, not the worker; organisations learn |
| Managerial work | Henry Mintzberg | Real management is fragmented, interpersonal and informational |

Fayol's fourteen principles (division of work, authority and responsibility, discipline, unity of command, unity of direction, subordination of individual interest, remuneration, centralisation, scalar chain, order, equity, stability of tenure, initiative, esprit de corps) explain where many organisational conventions come from; apply them as questions, not rules. Unity of command, for instance, conflicts with matrix organisations by design.

## Organisational laws and effects

| Name | Statement | Use | Caveat |
|---|---|---|---|
| Pareto principle | A few causes often produce most of the effect | Rank defects, customers, costs; work the top of the list | 80/20 is illustrative; measure the real split |
| Parkinson's law | Work expands to fill the time available | Time-box tasks; define done before starting | Satire (1955) with a real kernel |
| Peter principle | People are promoted until they reach a role they cannot do well | Promote on the skills of the next role; offer expert tracks | Some empirical support in sales promotions; not universal |
| Goodhart's law | When a measure becomes a target, it ceases to be a good measure | Pair every target with counter-metrics; review how numbers are produced | — |
| Campbell's law | The more a quantitative indicator drives social decisions, the more it is corrupted | Avoid single-number evaluations of people or units | — |
| Little's law | Average items in a stable system = arrival rate × average time in system (L = λW) | Cut lead time by limiting work in progress | Needs a stable system and consistent units |
| Diminishing returns | Adding one input while others stay fixed yields smaller and smaller gains | Find the binding constraint before adding resources | — |
| Brooks's law | Adding people to a late software project makes it later | Add people early or to independent work; count onboarding and communication cost | Strongest for tightly coupled work |
| Hofstadter's law | It always takes longer than you expect, even accounting for this law | Use reference-class forecasts and ranges | See the planning fallacy (Kahneman and Tversky) |
| Chesterton's fence | Do not remove a rule until you know why it exists | Find the owner and the incident behind a control before cutting it | — |
| Hanlon's razor | Do not assume malice where error explains it | Run blameless reviews; fix the system first | Does not excuse repeated negligence |
| Occam's razor | Prefer the simplest explanation that fits | Simplest process that meets the requirement | — |

## Execution and improvement methods

| Method | Origin | Core loop or tool | When to use |
|---|---|---|---|
| PDCA / PDSA | Shewhart, Deming | Plan, Do, Check (Study), Act | Any improvement; PDSA stresses studying results against a prediction |
| Lean | Toyota Production System | Value stream, flow, pull, eliminate waste (overproduction, waiting, transport, over-processing, inventory, motion, defects, unused talent) | Processes with queues, handoffs and rework |
| Kaizen | Japanese management practice | Small, frequent improvements by the people doing the work | Mature processes needing steady gains |
| Six Sigma / DMAIC | Motorola, GE | Define, Measure, Analyse, Improve, Control | Variation and defects with measurable outputs |
| Theory of Constraints | Eliyahu Goldratt | Identify the constraint, exploit it, subordinate everything else, elevate it, repeat | Throughput limited by a bottleneck |
| Kanban | Toyota; adapted to knowledge work | Visualise work, limit WIP, manage flow, explicit policies | Continuous flow of varied work |
| OKR | Andy Grove at Intel; spread by John Doerr | Qualitative objective plus 2–5 measurable key results per cycle | Focus and alignment; keep separate from performance pay |
| Balanced Scorecard | Kaplan and Norton | Financial, customer, internal process, learning and growth perspectives, linked in a strategy map | Translating strategy into a few linked measures |
| SMART goals | George T. Doran (1981) | Specific, measurable, assignable (often "achievable"), realistic, time-related | Writing individual objectives |
| Eisenhower matrix | Attributed to Dwight Eisenhower | Urgent × important | Personal and team triage |
| RACI | Project management practice | Responsible, accountable (one), consulted, informed | Clarifying ownership of decisions and deliverables |
| 5W2H | Quality management practice | What, why, who, when, where, how, how much | Action plans |
| OODA loop | John Boyd | Observe, orient, decide, act | Fast-changing, competitive situations |

In public organisations the Balanced Scorecard usually puts citizens and social outcomes at the top of the strategy map, with financial sustainability as a constraint.

## Choosing a method

| Problem | Start with |
|---|---|
| Work is late and lead times grow | Little's law and WIP limits (Kanban), then TOC on the bottleneck |
| Output varies or has defects | DMAIC with a measured baseline |
| Strategy does not reach daily work | OKR or Balanced Scorecard, a few measures each with counter-metrics |
| Nobody knows who decides | RACI with exactly one accountable person per decision |
| Recurring incidents | Blameless review (Hanlon), PDSA on the fix, check the controls before removing them (Chesterton) |
