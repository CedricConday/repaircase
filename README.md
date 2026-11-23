# RepairCase

Working name. The written case for one already-approved drug as the candidate for a myelin repair trial in multiple sclerosis, scored against a rubric that was fixed before the scoring.

Started 2026-11-23. Part of [RepairStack](https://github.com/CedricConday/repairstack). Nothing here is medical advice.

## How it works

1. `docs/RUBRIC.md` sets the gates, the points and the bar. It was committed before any candidate was scored.
2. `repaircase/score.py` reads the RepairMap trial table and scores every candidate.
3. `docs/CASE.md` is the result: the ranking, and the case for and against the top candidate.

## Result on 2026-11-23

No approved drug clears the bar of 4 points. The best available candidate is metformin plus clemastine at 3 points. Read `docs/CASE.md` for the ranking, the case for and against, and what result would change it.

Scored on RepairMap v0.1.0 (64 trials).

## Run it

```
pip install -e ".[dev]"
python -m repaircase.score --trials ../repairmap/data/trials.csv
```

Approval and tolerability for each drug are in `data/judgements.csv`, each with its source. US approval records come from the FDA's public Drugs@FDA database.
