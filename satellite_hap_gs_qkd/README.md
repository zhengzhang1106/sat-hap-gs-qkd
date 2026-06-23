# Satellite-HAP-GS QKD

Framework for Satellite-HAP-GS QKD network modeling.

Main source layout:

```text
src/adapters
src/entities/nodes
src/entities/links
src/graph
src/qkp
src/services
src/scenario
src/milp
src/drl
```

Link rates are stored in bps. MILP input also provides capacity_bits for bits per time slot. Demands and stored keys use bits.
