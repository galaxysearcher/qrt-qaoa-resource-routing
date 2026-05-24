from __future__ import annotations

import json
from pathlib import Path

from qrt_qaoa_routing import exact_solve, get_scenario, list_scenarios


def main() -> int:
    Path("results").mkdir(exist_ok=True)
    summary = []

    for name in list_scenarios():
        scenario = get_scenario(name)
        result = exact_solve(scenario)
        out_path = Path("results") / f"{name}_exact.json"
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        summary.append({
            "scenario": name,
            "best_bitstring": result["best_bitstring"],
            "best_energy": result["best_energy"],
            "best_policy": result["best_policy"],
        })

    summary_path = Path("results") / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
