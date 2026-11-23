from repaircase.score import BAR, score_all


def row(agent, outcome_class, result, id_=None):
    return {"id": id_ or f"{agent}-{outcome_class}-{result}", "agent": agent,
            "outcome_class": outcome_class, "result": result}


def judge(agent, approved="yes", advised_against="no", tolerability="well"):
    return {"agent": agent, "approved": approved, "advised_against": advised_against,
            "tolerability": tolerability}


def by_agent(scores):
    return {s.agent: s for s in scores}


def test_replicated_positive_with_function_clears_the_bar():
    trials = [row("a", "biomarker", "positive", "t1"), row("a", "biomarker", "positive", "t2"),
              row("a", "functional", "positive", "t3")]
    s = by_agent(score_all(trials, [judge("a")]))["a"]
    assert (s.e1, s.e2, s.e3, s.e6) == (2, 2, 2, 1)
    assert s.total == 7 and s.status == "clears the bar"


def test_single_positive_is_below_the_bar():
    s = by_agent(score_all([row("a", "biomarker", "positive")], [judge("a")]))["a"]
    assert s.total == 3 < BAR and s.status == "below the bar"


def test_combination_supports_its_part_and_the_reverse():
    trials = [row("a", "biomarker", "positive"), row("a + b", "biomarker", "positive")]
    scores = by_agent(score_all(trials, [judge("a"), judge("a + b")]))
    assert scores["a"].e2 == 1 and scores["a + b"].e2 == 1


def test_negatives_are_capped_and_harm_counts():
    trials = [row("a", "functional", "negative", f"n{i}") for i in range(3)] + [row("a", "safety", "harm")]
    s = by_agent(score_all(trials, [judge("a", tolerability="limited")]))["a"]
    assert s.e4 == -2 and s.e5 == -2 and s.total == -4


def test_gates_and_missing_judgement():
    trials = [row("a", "biomarker", "positive"), row("b", "biomarker", "positive"),
              row("c", "biomarker", "positive"), row("d", "biomarker", "ongoing")]
    scores = by_agent(score_all(trials, [judge("a", approved="no"), judge("b", advised_against="yes")]))
    assert scores["a"].status == "gate failed" and scores["b"].status == "gate failed"
    assert scores["c"].status == "incomplete"
    assert "d" not in scores
