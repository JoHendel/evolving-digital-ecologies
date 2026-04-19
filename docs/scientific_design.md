# Scientific Design Notes

## Modeling Philosophy

The framework treats evolution as an ecological process rather than a leaderboard optimization task. There is no global fitness function. Fitness is implicit: organisms that survive long enough to reproduce contribute more descendants to later population states.

## State Variables

Agents carry heritable scalar traits affecting movement, perception, metabolism, reproduction, aggression, sociality, exploration, risk response, and communication tendency. Optional neural genomes encode a compact feedforward controller whose weights are inherited and mutated.

## Selection Pressures

Selection arises through:

- Scarce and spatially uneven resources
- Metabolic cost of movement and perception
- Hazard damage
- Local crowding costs
- Reproductive energy thresholds
- Agent-agent competition
- Age and health constraints

## Emergence Metrics

The framework records population size, births, deaths, resource count, energy, age, trait diversity, clustering, resource efficiency, live lineages, and selected trait means. These measures are designed to support thesis chapters on stability, diversity, collapse, spatial aggregation, and lineage dominance.

## Reproducibility

All stochastic components derive from seeded random streams. Run outputs include a configuration snapshot, CSV metrics, final population data, and a JSON summary.

