import json
import subprocess
import sys
from pathlib import Path

from qrt_qaoa_routing import exact_solve, get_scenario, list_scenarios


def test_scenarios_exist():
    assert list_scenarios() == ["water_recovery", "thermal_regulation", "acid_regolith"]


def test_exact_solve_outputs_policy():
    for name in list_scenarios():
        scenario = get_scenario(name)
        result = exact_solve(scenario)
        assert len(result["best_bitstring"]) == scenario.n_bits
        assert set(result["best_policy"].keys()) == set(scenario.labels)
        assert len(result["top_candidates"]) >= 3


def test_run_all_script(tmp_path):
    result = subprocess.run(
        [sys.executable, "scripts/run_all.py"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    assert "water_recovery" in result.stdout
    assert Path("results/summary.json").exists()
    summary = json.loads(Path("results/summary.json").read_text(encoding="utf-8"))
    assert len(summary) == 3
