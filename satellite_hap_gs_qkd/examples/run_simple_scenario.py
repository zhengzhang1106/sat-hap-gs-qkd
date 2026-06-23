from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from drl.environment import MultiLayerQKDEnv
from inputs.scenarios.simple_sat_hap_gs_scenario import build_scenario
from milp.milp_data import build_milp_input
from topology.network_topology import MultiLayerTopology


def main() -> None:
    scenario = build_scenario()
    topology = MultiLayerTopology(scenario)
    milp_input = build_milp_input(scenario)
    env = MultiLayerQKDEnv(scenario)
    initial_state = env.reset()

    print("=" * 80)
    print(f"Scenario: {scenario.scenario_id}")
    print(f"Time slots: {scenario.time_slots}")
    print(f"Nodes: {len(scenario.nodes)}")
    print(f"Links: {len(scenario.links)}")
    print(f"Demands: {len(scenario.demands)}")
    print("-" * 80)
    print("Nodes by type:")
    for node_type in ("GS", "SAT", "HAP"):
        count = sum(1 for n in scenario.nodes.values() if n.node_type.value == node_type)
        print(f"  {node_type}: {count}")

    print("-" * 80)
    print("Active links by time slot:")
    for t in scenario.time_slots:
        active = [link.link_id for link in topology.get_active_links(t)]
        print(f"  t={t}: {active}")

    print("-" * 80)
    print("MILP input summary:")
    print(f"  node_ids={milp_input.node_ids}")
    print(f"  link_ids={milp_input.link_ids}")
    print(f"  demand_ids={milp_input.demand_ids}")

    print("-" * 80)
    print("Initial DRL state summary:")
    print(f"  time_slot={initial_state.time_slot}")
    print(f"  link_capacity={initial_state.link_capacity}")
    print(f"  demand={initial_state.demand}")
    print(f"  qkp_storage={initial_state.qkp_storage}")
    print("=" * 80)


if __name__ == "__main__":
    main()

