# RepairCase rubric

Registered 2026-11-23, before the trial table (RepairMap) was checked a second time and before any candidate was scored. Changes after this commit are appended below with a date and a reason; the rules above are not edited.

## Question

Which drug that is already approved for some other use has the best published human evidence for a myelin repair trial in multiple sclerosis, and does any of them clear a fixed bar?

Only published results from trials in people count. Animal and cell results do not score.

## Candidates

Every distinct agent in RepairMap that has at least one trial with a result. A combination (written `A + B` in the table) is its own candidate.

## Gates

A candidate that fails a gate is listed with the reason and is not ranked.

- **G1 Approved.** The drug, or every drug in the combination, is approved for human use for some indication by the FDA or the EMA or a national European regulator. Source required.
- **G2 Tested for repair in MS.** At least one RepairMap row with a result of positive, mixed, negative or harm.
- **G3 Usable.** The trial authors did not advise against its use on tolerability grounds.

## Score

Computed from RepairMap rows by `repaircase/score.py`. No hand scoring except E6, which needs a sourced judgement.

| Item | Rule | Points |
|---|---|---|
| E1 Biomarker signal | A randomised trial of this candidate met a biomarker primary outcome (`outcome_class=biomarker`, `result=positive`) | 2 |
| | Otherwise a `mixed` biomarker result | 1 |
| E2 Replication | Two or more positive biomarker rows for this candidate | 2 |
| | One positive row, plus a positive row for a combination that contains it (or, for a combination, for one of its parts) | 1 |
| E3 Function | A positive result on a functional primary outcome | 2 |
| | Otherwise a `mixed` functional result | 1 |
| E4 Contradiction | Each trial of this candidate with a `negative` result | −1 each, at most −2 |
| E5 Harm in MS | Any row with `result=harm` | −2 |
| E6 Tolerability | Well tolerated at the tested dose in the positive trial, per the trial report | 1 |
| | Side effects that the report says limited use or dosing | 0 |

Maximum 7.

## Bar

A candidate **clears the bar** at 4 points or more with all gates passed.

If no candidate clears the bar, RepairCase says so in its first line, names the highest-scoring candidate as "best available, not cleared", and lists what single result would move it over the bar.

## Notes that are reported but not scored

- Whether a trial that could settle the question is already running (rows with `result=ongoing`). If so the case says "wait for this readout" and gives the date.
- Negative trials of other drugs with the same mechanism.
- Who was tested (age, disease stage), since the published explanations for failure point to both.

## What this rubric cannot do

It ranks on published trial outcomes only. It does not predict that a drug works, and nothing produced with it is medical advice.
