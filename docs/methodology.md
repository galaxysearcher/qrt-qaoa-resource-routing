# Methodology

## Objective

Represent small ISRU control decisions as binary optimization problems that can be evaluated by exact enumeration or a diagonal QAOA-style simulator.

## Formulation

Each scenario defines:

- a binary policy vector
- labels for each bit
- a scalar energy function
- subsystem-specific rewards and penalties

Lower energy is better.

## Scenario logic

### Water recovery

The water scenario rewards water storage, oxygen production, and recycling. Penalties enforce power budget, flow balance, oxygen-step gating, recycle consistency, and minimum throughput.

### Thermal regulation

The thermal scenario rewards activated thermal paths and radiator use when a path exists. Penalties track unmet thermal load, power budget deviation, and radiator activation without a path.

### Acid-regolith processing

The acid-regolith scenario rewards yield, circulation, separation, and downstream product activation. Penalties track energy use, corrosion exposure, acid loss, missing process path, and product activation without filtration.

## Solver logic

The default solver enumerates the full binary landscape. This gives a deterministic baseline for each compact scenario and provides a reference answer for future Qiskit runs.

The optional Qiskit runner applies a diagonal phase operator derived from the energy vector, followed by RX mixers, and sweeps gamma and beta over a small grid using a local simulator.
