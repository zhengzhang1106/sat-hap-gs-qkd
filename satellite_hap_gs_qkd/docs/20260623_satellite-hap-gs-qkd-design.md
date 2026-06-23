# Satellite-HAP-GS QKD Project Design

## 1. First-Stage Goal

This project builds a new research-code framework for multi-layer QKD networks that integrate satellites, HAPs, and ground stations.

The first stage focuses on project structure and shared data models only. 

The framework is for integration of the existing Satellite-GS QKD and HAP-GS QKD code.



- **Satellite-GS QKD source code**

  including satellite visibility, free-space channel, SatQuMA-style SKR, and satellite-to-GS key-rate generation

- **HAP-GS QKD source code**

  including HAP trajectories, HAP-GS channel/SKR calculation, HAP flight planning, offline MILP, and online/DRL-style decision logic



## 2. Modeling Scope

The network contains three node types:

- `GS`: ground station
- `SAT`: satellite
- `HAP`: high-altitude platform

The framework supports three QKD link types:

- `SAT-GS`
- `SAT-HAP`
- `HAP-GS`

Each link can have time-varying key generation capacity represented as:

```python
{time_slot: key_rate}
```

Each physical or logical link can have its own QKP, including `SAT-GS`, `SAT-HAP`, and `HAP-GS` links.



## 3. Problem Statement

We study planning and dynamic management in a multi-layer QKD network that integrates satellites, HAPs, and ground stations.

The main challenge is that link capacity changes over time:

- satellite links vary with orbital motion, visibility, elevation, and weather
- HAP links vary with wind-driven mobility and atmospheric effects
- satellites and HAPs have limited RX/TX resources and alignment constraints
- routing, link activation, key generation, key consumption, and QKP storage must be optimized jointly

### Given

The input contains:

- GS-pair key demands for each time slot
- satellite orbit and visibility information
- HAP node positions or trajectories
- GS coordinates
- achievable key rates for `SAT-GS`, `SAT-HAP`, and `HAP-GS` links at each time slot
- initial QKP states
- node resource limits, including satellite and HAP connection limits

### Decide

The methods should decide:

- which links to activate at each time slot
- satellite-to-GS assignments
- satellite-to-HAP assignments
- HAP-to-GS assignments
- feasible end-to-end routing paths
- key flow allocation
- whether to serve demand directly, consume QKP keys, or store newly generated keys

### Objective

The primary objective is to maximize total served keys across all demands and time slots.

The secondary objective is to maximize final stored key bits in QKPs, so the network remains useful for future demand.

### Constraints

The model must respect:

- link capacity and link availability
- flow conservation
- demand upper bounds
- RX/TX and alignment limits on satellites and HAPs
- QKP generation, consumption, storage capacity, and update rules
- multi-layer connectivity over `SAT-GS`, `SAT-HAP`, and `HAP-GS` links

### Solution Routes

The project will support two methods under the same topic:

- `MILP`: an optimization route that later builds a joint link-activation, routing, and QKP allocation model
- `DRL`: a learning route where the agent selects active links, then a routing and QKP module computes feasible paths, key allocation, storage updates, and reward

In the first stage, both routes only need clear interfaces and placeholders.



## 4. Project Structure

The first-stage directory structure is:

```text
satellite_hap_gs_qkd/
  docs/
  inputs/
    raw/
    scenarios/
  outputs/
    milp/
      results/
      logs/
    drl/
      results/
      logs/
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
  README.md
```

The `inputs/raw/` directory is reserved for original orbit, HAP trajectory, weather, visibility, and SKR data.

The `inputs/scenarios/` directory is reserved for cleaned Python scenario definitions. This follows the style of the existing codebase, where topology and experiment parameters are defined directly in Python scripts.

The `outputs/` directory separates MILP and DRL results while keeping figures shared.

The first-stage framework does not keep a generic `utils/` package. Shared logic should stay close to its concept, such as nodes, links, scenarios, topology, MILP, or DRL. A utility module can be added later only when there is a concrete cross-module responsibility, for example coordinate conversion or result file I/O.



## 5. Core Data Model

### Node

A node stores:

- `node_id`
- `node_type`: `GS`, `SAT`, or `HAP`
- `position`
- `rx_tx_limit`
- `storage_capacity`
- `status`
- optional mobility or trajectory metadata

This extends the existing style, where `QuantumNode` mainly keeps `node_id`, memory, and channels, without forcing a heavy object model.

### Link

A link stores:

- `link_id`
- `source`
- `target`
- `link_type`: `SAT-GS`, `SAT-HAP`, or `HAP-GS`
- `distance_km`
- `capacity_by_time`
- `availability_by_time`
- optional channel metadata such as loss or weather condition

### Key Pool

A key pool stores:

- `link_id`
- `stored_keys_by_time`
- `capacity`
- update hooks for key generation and key consumption

### Demand

A demand stores:

- `demand_id`
- source GS
- destination GS
- requested key volume by time slot
- optional priority or weight

### Scenario

A scenario bundles:

- nodes
- links
- demands
- QKPs
- time slots
- global parameters



## 6. MILP Route

The MILP module will receive the shared scenario object and later build an optimization model for:

- link activation decisions
- key flow routing
- QKP generation, consumption, and storage
- transceiver limits on satellites and HAPs
- flow conservation across the multi-layer topology

In the first stage, the MILP module should only expose clear placeholder interfaces, such as:

- scenario-to-MILP data conversion
- model builder placeholder
- result object placeholder

No full Gurobi model is required in the first stage.

