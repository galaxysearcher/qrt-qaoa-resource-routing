# QRT QAOA Resource Routing

QAOA-style binary optimization examples for modular ISRU resource-routing policies.

The repository defines compact decision models for three resource-routing subsystems:

```text
water recovery → thermal regulation → acid-regolith processing
```

Each subsystem is represented as a binary policy vector with an energy function that combines reward terms, power limits, flow constraints, and subsystem-specific penalties.

## What this project does

- Defines interpretable binary decision variables for each subsystem.
- Builds diagonal energy landscapes over all candidate bitstrings.
- Solves each scenario with an exact enumeration baseline.
- Provides an optional Qiskit diagonal-ansatz sweep for local simulator runs.
- Writes structured JSON results for repeatable inspection.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python scripts/run_all.py
```

The run writes:

```text
results/water_recovery_exact.json
results/thermal_regulation_exact.json
results/acid_regolith_exact.json
results/summary.json
```

## Run tests

```bash
python -m pytest
```

## Optional Qiskit run

Install the optional Qiskit dependencies:

```bash
pip install -e ".[qiskit]"
python scripts/run_qiskit_sweep.py --scenario water_recovery --grid 7 --shots 1024
```

## Repository structure

```text
src/qrt_qaoa_routing/
  bitstrings.py
  scenarios.py
  energy.py
  solve.py
  qiskit_optional.py

scripts/
  run_all.py
  run_exact.py
  run_qiskit_sweep.py

docs/
  methodology.md
  validation_plan.md

examples/
  scenarios.json
```

## Scenario summary

| Scenario | Variables | Optimization focus |
|---|---:|---|
| water_recovery | 6 | water, oxygen, recycling, power, and flow balance |
| thermal_regulation | 6 | thermal-load damping, path activation, and power budget |
| acid_regolith | 8 | yield, circulation, corrosion control, acid loss, and downstream product step |

## Output format

Each result JSON contains:

- scenario name
- bit labels
- best bitstring
- decoded policy
- best energy
- top candidate policies
- constraint diagnostics

## Research workflow

This repository turns resource-routing policies into explicit binary optimization problems. The core artifact is the formulation discipline: define the policy variables, encode constraints, solve the energy landscape, and produce reviewable decisions.
