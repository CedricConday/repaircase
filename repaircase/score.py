"""Score repair-trial candidates against docs/RUBRIC.md.

Reads the RepairMap trial table and a small sheet of sourced judgements
(approval, tolerability). Prints the ranking and writes results/scores.csv.

Run: repaircase   (or, in a checkout: python -m repaircase.score --trials ../repairmap/data/trials.csv)
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKOUT = (ROOT / "pyproject.toml").exists()  # run from the repository, not an installed wheel


def _packaged(package: str, name: str) -> Path:
    from importlib.resources import files

    return Path(str(files(package) / name))


def _default_trials() -> Path:
    """The sibling RepairMap checkout when there is one, else the table in the installed repairmap."""
    sibling = ROOT.parent / "repairmap" / "data" / "trials.csv"
    return sibling if CHECKOUT and sibling.exists() else _packaged("repairmap.data", "trials.csv")


JUDGEMENTS = ROOT / "data" / "judgements.csv" if CHECKOUT else _packaged("repaircase.data", "judgements.csv")
BAR = 4
DECIDED = {"positive", "mixed", "negative", "harm"}


@dataclass
class Score:
    agent: str
    e1: int = 0
    e2: int = 0
    e3: int = 0
    e4: int = 0
    e5: int = 0
    e6: int = 0
    gates_failed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    ongoing: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.e1 + self.e2 + self.e3 + self.e4 + self.e5 + self.e6

    @property
    def status(self) -> str:
        if self.gates_failed:
            return "gate failed"
        if self.missing:
            return "incomplete"
        return "clears the bar" if self.total >= BAR else "below the bar"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def parts(agent: str) -> list[str]:
    return [p.strip() for p in agent.split("+")]


def _positive_biomarker(rows: list[dict[str, str]]) -> int:
    return sum(r["outcome_class"] == "biomarker" and r["result"] == "positive" for r in rows)


def score_agent(agent: str, trials: list[dict[str, str]], judgement: dict[str, str] | None) -> Score:
    s = Score(agent)
    own = [r for r in trials if r["agent"] == agent]
    decided = [r for r in own if r["result"] in DECIDED]
    s.ongoing = [r["id"] for r in own if r["result"] == "ongoing"]

    # Related rows: combinations that contain this agent, or the parts of this combination.
    mine = set(parts(agent))
    related = [
        r for r in trials
        if r["agent"] != agent and r["result"] in DECIDED
        and (mine < set(parts(r["agent"])) or set(parts(r["agent"])) < mine)
    ]

    pos_bio = _positive_biomarker(decided)
    if pos_bio:
        s.e1 = 2
    elif any(r["outcome_class"] == "biomarker" and r["result"] == "mixed" for r in decided):
        s.e1 = 1

    if pos_bio >= 2:
        s.e2 = 2
    elif pos_bio == 1 and _positive_biomarker(related):
        s.e2 = 1

    functional = [r for r in decided if r["outcome_class"] == "functional"]
    if any(r["result"] == "positive" for r in functional):
        s.e3 = 2
    elif any(r["result"] == "mixed" for r in functional):
        s.e3 = 1

    s.e4 = -min(2, sum(r["result"] == "negative" for r in decided))
    s.e5 = -2 if any(r["result"] == "harm" for r in decided) else 0

    if not decided:
        s.gates_failed.append("G2 no trial with a result")
    if judgement is None:
        s.missing.append("no judgement row (approval, tolerability)")
        return s
    if judgement["approved"] == "no":
        s.gates_failed.append("G1 not approved for any use")
    elif judgement["approved"] != "yes":
        s.missing.append("approval not sourced")
    if judgement["advised_against"] == "yes":
        s.gates_failed.append("G3 trial authors advised against use")
    if judgement["tolerability"] == "well":
        s.e6 = 1
    elif judgement["tolerability"] not in {"limited", "na"}:
        s.missing.append("tolerability not sourced")
    return s


def score_all(trials: list[dict[str, str]], judgements: list[dict[str, str]]) -> list[Score]:
    by_agent = {j["agent"]: j for j in judgements}
    agents = sorted({r["agent"] for r in trials if r["result"] in DECIDED})
    scores = [score_agent(a, trials, by_agent.get(a)) for a in agents]
    return sorted(scores, key=lambda s: (bool(s.gates_failed), -s.total, s.agent))


def write(scores: list[Score], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["agent", "total", "status", "e1", "e2", "e3", "e4", "e5", "e6",
                    "gates_failed", "missing", "ongoing_trials"])
        for s in scores:
            w.writerow([s.agent, s.total, s.status, s.e1, s.e2, s.e3, s.e4, s.e5, s.e6,
                        "; ".join(s.gates_failed), "; ".join(s.missing), "; ".join(s.ongoing)])


def main() -> int:
    ap = argparse.ArgumentParser(description="Score repair-trial candidates against docs/RUBRIC.md.")
    ap.add_argument("--trials", type=Path, default=None,
                    help="RepairMap trials.csv (default: the installed repairmap's table)")
    ap.add_argument("--judgements", type=Path, default=JUDGEMENTS)
    default_out = ROOT / "results" / "scores.csv" if CHECKOUT else Path("scores.csv")
    ap.add_argument("--out", type=Path, default=default_out)
    a = ap.parse_args()

    judgements = read_csv(a.judgements) if a.judgements.exists() else []
    scores = score_all(read_csv(a.trials or _default_trials()), judgements)
    write(scores, a.out)
    for s in scores:
        print(f"{s.total:>3}  {s.status:<15} {s.agent}  "
              f"[E1 {s.e1} E2 {s.e2} E3 {s.e3} E4 {s.e4} E5 {s.e5} E6 {s.e6}]"
              + (f"  ({'; '.join(s.gates_failed + s.missing)})" if s.gates_failed or s.missing else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
