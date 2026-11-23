# RepairCase

Working name. The written case for one already-approved drug as the candidate for a myelin repair trial in multiple sclerosis, scored against a rubric that was fixed before the scoring.

Started 2026-11-23. Part of [RepairStack](https://github.com/CedricConday/repairstack). Nothing here is medical advice.

## How it works

1. `docs/RUBRIC.md` sets the gates, the points and the bar. It was committed before any candidate was scored.
2. `repaircase/score.py` reads the RepairMap trial table and scores every candidate.
3. `docs/CASE.md` is the result: the ranking, and the case for and against the top candidate.

## State on 2026-11-23

Rubric registered. Scoring waits for the checked RepairMap table.
