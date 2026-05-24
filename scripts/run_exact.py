from __future__ import annotations

import argparse
import json
from pathlib import Path

from qrt_qaoa_routing import exact_solve, get_scenario


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    scenario = get_scenario(args.scenario)
    result = exact_solve(scenario)

    out_path = Path(args.out) if args.out else Path("results") / f"{scenario.name}_exact.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
