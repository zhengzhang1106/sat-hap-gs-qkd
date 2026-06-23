# Satellite-HAP-GS QKD

This repository contains a research framework for modeling and preparing MILP-based optimization for a multi-layer QKD network with satellites, high-altitude platforms, and ground stations.

The current goal is to build a clean data and code structure for integrating two reference codebases:

- `work/satellite-QKD`: reference implementation for Satellite-GS QKD links.
- `work/HAP-QKD`: reference implementation for HAP-GS QKD links.

The framework is currently focused on the MILP data preparation pipeline. The `drl/` folder is kept only as a placeholder for possible future work.

---

## 1. Network Model

The network contains three node types:

```text
GS   : ground station
SAT  : satellite trusted relay
HAP  : high-altitude platform trusted relay
```

The network contains three physical QKD link types:

```text
SAT-GS   : satellite-ground QKD link
HAP-GS   : HAP-ground QKD link
SAT-HAP  : inter-layer satellite-HAP QKD link
```

Each physical link can have a corresponding QKP, which stores generated key bits and supports later key consumption by routing or MILP modules.

---

## 2. Current Source Structure

```text
satellite_hap_gs_qkd/
  work/
    satellite-QKD/
    HAP-QKD/

  inputs/
    raw/
    scenarios/

  outputs/

  examples/

  src/
    adapters/
      source_adapters.py

    entities/
      nodes/
        base_node.py
        ground_station.py
        satellite.py
        air_platform.py
        high_altitude_platform.py
        node_type.py

      links/
        base_link.py
        satellite_ground_link.py
        platform_ground_link.py
        inter_layer_link.py
        link_type.py

    graph/
      network_graph.py

    qkp/
      key_pool.py

    services/
      service_demand.py

    scenario/
      network_scenario.py

    milp/
      milp_data.py

    drl/
      environment.py

  tests/
```

The old `common/` and `topology/` folders have been removed to avoid redundant abstractions.

---

## 3. Main Module Responsibilities

### `entities/`

Defines the basic network objects.

```text
entities/nodes/   defines GS, SAT, and HAP nodes
entities/links/   defines SAT-GS, HAP-GS, and SAT-HAP links
```

Each link stores a time-varying key generation rate and exposes a common interface:

```python
key_rate_bps_at(t)
capacity_bits_at(t, slot_duration_seconds)
```

### `qkp/`

Defines the quantum key pool model.

```text
qkp/key_pool.py
```

QKP quantities are stored in key bits.

### `adapters/`

Converts original paper code or data into the new framework format.

```text
src/adapters/source_adapters.py
```

This is where the original Satellite-GS and HAP-GS logic should be connected to the new `SatelliteGroundLink` and `PlatformGroundLink` classes.

### `inputs/scenarios/`

Defines concrete simulation or optimization cases.

A scenario specifies:

```text
nodes
links
demands
QKPs
time slots
global parameters
```

The scenario should call adapter functions instead of directly mixing original paper code into the scenario file.

### `graph/`

Builds a NetworkX graph view from a scenario.

```text
src/graph/network_graph.py
```

This is useful for checking connectivity, active links, incoming links, outgoing links, and link capacities.

### `milp/`

Converts a scenario into MILP-ready dictionaries.

```text
src/milp/milp_data.py
```

The full optimization model is not implemented yet. The current focus is to prepare correct inputs.

---

## 4. Unit Convention

The code uses the following unit convention:

| Quantity | Unit | Location |
|---|---:|---|
| link key generation rate | bps | `link.capacity_by_time`, `key_rate_bps_at(t)` |
| MILP link capacity | bits per time slot | `milp_input.capacity_bits[(link_id, t)]` |
| demand | bits per time slot | `Demand.requested_keys_by_time` |
| QKP storage | bits | `KeyPool.stored_keys_by_time` |
| QKP capacity | bits | `KeyPool.capacity` |

The conversion is:

```python
capacity_bits = key_rate_bps * slot_duration_seconds
```

---

## 5. Basic Workflow

The intended data flow is:

```text
work/ original paper code or data
        ↓
src/adapters/source_adapters.py
        ↓
inputs/scenarios/*.py
        ↓
scenario.network_scenario.Scenario
        ↓
src/graph/network_graph.py
        ↓
src/milp/milp_data.py
        ↓
future MILP model
```

In short:

```text
adapter  = converts original data/code into framework objects
scenario = builds one concrete experiment instance
graph    = checks the network structure
milp     = converts scenario data into optimization input
```

---

## 6. Current Development Task

The next implementation step is to complete the real link construction for:

```text
SAT-GS links
HAP-GS links
```

Main files to modify:

```text
src/adapters/source_adapters.py
src/entities/links/satellite_ground_link.py
src/entities/links/platform_ground_link.py
inputs/scenarios/source_mapped_multilayer_scenario.py
src/milp/milp_data.py
```

Expected result:

```text
1. Satellite-GS capacities can be loaded or computed from the satellite-QKD reference code.
2. HAP-GS capacities can be loaded or computed from the HAP-QKD reference code.
3. The scenario can be built successfully.
4. The graph view can be generated successfully.
5. MILP input can be generated successfully.
6. Tests pass.
```

---

## 7. Run Checks

From the repository root, run:

```powershell
python -m compileall satellite_hap_gs_qkd
python satellite_hap_gs_qkd\examples\run_simple_scenario.py
python satellite_hap_gs_qkd\examples\run_source_mapped_topology.py
python -m pytest satellite_hap_gs_qkd\tests
```

---

## 8. Development Rules

Do not work directly on `main`.

Create a separate branch, for example:

```bash
git checkout -b feature/sat-gs-hap-gs-links
```

Use AI tools if useful for understanding the original code, refactoring functions, or debugging. The final implementation should still be checked against the original paper logic and should pass the validation commands above.
