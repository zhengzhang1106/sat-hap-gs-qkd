# Satellite-HAP-GS QKD

This project is the framework for Satellite-HAP-GS QKD network modeling.

The current implementation focuses on the MILP-ready data model. DRL remains only a future route and is not part of the current implementation target.

## Modeling Scope

The framework integrates the two reference codebases kept under `work/`:

- `zhengzhang1106/satellite-QKD`: Satellite-GS QKD source model
- `zhengzhang1106/HAP-QKD`: HAP-GS QKD source model

The new code under `src/` is organized by network entities rather than by a generic `common` package.

## Current Structure

```text
satellite_hap_gs_qkd/
  work/                         # reference implementations from the two papers
  inputs/
    raw/
    scenarios/
  outputs/
  examples/
  src/
    entities/
      nodes/
        base_node.py
        ground_station.py
        satellite.py
        air_platform.py
        node_type.py
      links/
        base_link.py
        satellite_ground_link.py
        platform_ground_link.py
        inter_layer_link.py
        link_type.py
    qkp/
      key_pool.py
    services/
      service_demand.py
    scenario/
      network_scenario.py
    topology/
    milp/
    drl/
    common/                      # compatibility exports only
  tests/
```

## Unit Convention

- Link classes store physical key generation rate in `bps` through `capacity_by_time` and `key_rate_bps_at(t)`.
- MILP data exposes both:
  - `capacity[(link_id, t)]`: bps, kept for compatibility.
  - `capacity_bits[(link_id, t)]`: bits available within one time slot.
- Demands and QKP storage are measured in key bits.

## Quick Checks

```powershell
python -m compileall satellite_hap_gs_qkd
python satellite_hap_gs_qkd\examples\run_simple_scenario.py
python satellite_hap_gs_qkd\examples\run_source_mapped_topology.py
python -m pytest satellite_hap_gs_qkd\tests
```
