# A study loop that can change after evidence

## Synthetic example: choosing a database index

Goal: explain an index choice for a new query using its access pattern and a supplied execution plan. This example teaches reasoning, not production database changes.

Initial task: predict which of two supplied plans scans fewer rows and explain the trade-off. Record the attempt and whether a hint was used. If the learner cannot interpret a plan, first model one small plan with annotated inputs and outputs.

Practice sequence proposed for the learner's available week:

- First meeting: annotate a worked example, complete a partly worked one, then attempt a fresh case with feedback.
- Next available meeting: recall the decision criteria without the notes; explain an incorrect index choice and correct it.
- Later meeting: discriminate among query shapes, predict which criteria matter and check the explanation against the supplied plan.
- End check: justify a new case with the aids allowed by the actual goal. Mark unsupported assumptions and compare with the baseline.

These are sample checkpoints, not validated optimal intervals. A correct choice with no explanation may be a guess; a plausible explanation with a wrong plan reading identifies a different gap. Keep the error log small: task, observed error, corrected principle, next distinguishing case.

## Select a method by the difficulty

| Observed difficulty | Useful move | Evidence to inspect next |
|---|---|---|
| Cannot recall necessary facts | Short retrieval followed by correction | Recall after a delay, not familiarity while rereading |
| Follows a solution but cannot start | Worked example, then remove one support | An independently selected first step |
| Picks a method indiscriminately | Contrast related cases and explain the choice | Correct discrimination on a fresh case |
| Explains fluently but cannot perform | Attempt a bounded real task with feedback | Observable performance, not confidence |

Do not label the learner visual/auditory/kinesthetic or promise speed multipliers. Choose representations for the content and access needs. A self-explanation can reveal an error and still require correction.

## Readings, consulted 2026-11-11

Original procedure and example; no source wording, graphics or templates imported. The [IES practice guide](https://ies.ed.gov/ncee/WWC/PracticeGuide/1) discusses spacing, quizzing, explanatory questions and alternating worked examples with problems, with different evidence levels. [Carnegie Mellon on spaced practice](https://www.cmu.edu/teaching/resources/instructionalstrategies/activelearningstrategies/spacedopractice/index.html) gives course applications. Neither source validates this synthetic schedule.
