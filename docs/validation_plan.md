# Validation Plan

## Current validation

The repository currently validates:

- scenario construction
- binary-vector decoding
- exact enumeration over all bitstrings
- result serialization through the scripts
- expected best-policy structure for each scenario

## Next validation gates

1. Compare exact enumeration results to optional Qiskit simulator outputs.
2. Add scenario perturbation tests across power budgets and stress levels.
3. Add constraint-by-constraint diagnostic scores to the result JSON.
4. Add plots for energy landscapes and top candidate separation.
5. Add benchmark tables across grid size, shots, and optimizer settings.
6. Expand the scenario library with a constellation scheduling case in a separate module.

## Acceptance logic

A scenario formulation is useful when its best candidate is interpretable, its top candidates are stable across reasonable parameter perturbations, and its penalties correctly suppress invalid policies.
