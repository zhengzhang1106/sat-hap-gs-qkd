# Satellite-HAP-GS QKD

This project is the new framework for satellite-HAP-GS QKD network modeling.

The first stage focuses on the common network structure used by both future methods:

- `MILP`: optimization model for link activation, routing, and QKP allocation
- `DRL`: learning environment for dynamic link selection and reward evaluation

## Current Scope

The code currently builds the shared nodes, links, demands, key pools, scenarios, and topology graph. It maps the existing source repositories as:

- `zhengzhang1106/satellite-QKD`: Satellite-GS QKD source model
- `zhengzhang1106/HAP-QKD`: HAP-GS QKD source model
- `SAT-HAP`: topology placeholder; physical/SKR model still needs to be added

## Structure

```text
satellite_hap_gs_qkd/
  docs/
  inputs/
    raw/
    scenarios/
  outputs/
    milp/
    drl/
    figures/
  examples/
  src/
    common/
      network_types.py
      network_node.py
      quantum_link.py
      key_pool.py
      network_demand.py
      network_scenario.py
      models.py
    topology/
    milp/
    drl/
  tests/
```

`src/common/models.py` is only a compatibility export file. New code should import from the concept-specific files, such as `common.network_node` and `common.quantum_link`.

## Quick Checks

```powershell
python -m compileall satellite_hap_gs_qkd
python satellite_hap_gs_qkd\examples\run_simple_scenario.py
python satellite_hap_gs_qkd\examples\run_source_mapped_topology.py
python -m pytest satellite_hap_gs_qkd\tests
```
