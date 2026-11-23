# RepairCase, 2026-11-23

**No approved drug clears the bar.** The bar is 4 of 7 points on published human trial evidence (`docs/RUBRIC.md`, fixed before scoring). The best available candidate for a repair trial is **metformin plus clemastine** at 3 points. It is not cleared.

Scored on RepairMap v0.1.0 (64 trials, 39 agents, 63 rows checked against their source). Nothing here is medical advice.

## Ranking

Approved drugs, ranked:

| Candidate | Total | Biomarker (E1) | Replication (E2) | Function (E3) | Negative trials (E4) | Harm (E5) | Tolerability (E6) |
|---|---|---|---|---|---|---|---|
| metformin + clemastine | 3 | 2 | 1 | 0 | 0 | 0 | 0 |
| phenytoin | 3 | 2 | 0 | 0 | 0 | 0 | 1 |
| clemastine | 2 | 2 | 1 | 0 | 0 | −2 | 1 |
| high-dose biotin | 0 | 0 | 0 | 2 | −2 | 0 | 0 |
| bazedoxifene | −1 | 0 | 0 | 0 | −1 | 0 | 0 |
| domperidone | −2 | 0 | 0 | 0 | −2 | 0 | 0 |
| metformin | −2 | 0 | 0 | 0 | −2 | 0 | 0 |

Not ranked, gate failed:

| Candidate | Points | Gate |
|---|---|---|
| bexarotene | 1 | Trial authors advised against its use (thyroid and blood-fat effects in almost every participant) |
| CNM-Au8, GSK239512, PIPE-791, PIPE-307, opicinumab, elezanumab, cell therapy | 1 to −2 | Not approved for any use |

Full output: `results/scores.csv`. Inputs: `data/judgements.csv`.

## Why metformin plus clemastine and not phenytoin

They tie on points. The tie breaks on what was measured, which the rubric reports but does not score.

- The phenytoin trial measured thinning of the retinal nerve fibre layer after acute optic neuritis. That is nerve fibre loss, so the result is about protection, not repair of myelin. Its registry record lists a myelin measure as a secondary aim; the abstract does not report it.
- The metformin plus clemastine trial measured signal speed along the optic nerve, which is the closest thing the field has to a repair readout.

## The case for metformin plus clemastine

- It met its main outcome in a randomised, placebo-controlled trial of 70 people with relapsing MS over 26 weeks: signal delay was 1.2 ms shorter than placebo (95% CI 0.1 to 2.4).
- Clemastine alone had already met the same kind of outcome in a separate trial of 50 people: 1.7 ms per eye (95% CI 0.5 to 2.9).
- Both drugs are old, approved and off patent.

## The case against

- The effect is small. The combination trial found no change in disability or in other measures of vision.
- The combination result is a conference report from September 2025. No results paper was on PubMed on 2026-11-23, so the numbers have not been through peer review.
- People on the combination had more fatigue and gut side effects.
- Clemastine alone has a harm signal in a different group: in older people with progressive MS, 3 of 9 worsened much faster than before and that trial arm was stopped. The two trials in younger people with relapsing MS did not report this.
- Metformin alone was dropped from a large progressive MS trial in September 2026 for lack of promise.
- A cleaner drug aimed at the same target as clemastine (PIPE-307, not approved) missed every outcome in a trial of 182 people.

## What would move it over the bar

One of these, each worth the missing point:

1. A second trial of the combination that meets a repair biomarker outcome.
2. Any positive or mixed result on a functional outcome such as low-contrast vision.
3. A peer-reviewed report stating the combination was well tolerated at the tested dose.

## Trials already running that bear on it

| Trial | Registry | Measures | Primary completion |
|---|---|---|---|
| Clemastine, ReVIVE | NCT05359653 | Myelin MRI | 2027-06 |
| Clemastine, ReCOVER | NCT02521311 | Signal delay, low-contrast vision | 2028-08 |
| Metformin, MACSiMiSE-BRAIN | NCT05893225 | Walking speed over 96 weeks | 2027-02 |

No registered follow-on trial of the combination was found.

## Limits

- The rubric counts trial outcomes. It does not weigh effect size, trial size or who was tested.
- 30 of 31 paper rows in the trial table were checked against the abstract only.
- "Not approved" means no record in the FDA's Drugs@FDA database on 2026-11-23; the EMA was not checked for those drugs.
- The bexarotene follow-up is counted as a positive biomarker result although it was a follow-up of 20 people, not a planned main outcome. It does not change the ranking, because bexarotene fails a gate.
- One reader, one pass. No second person has scored this.
