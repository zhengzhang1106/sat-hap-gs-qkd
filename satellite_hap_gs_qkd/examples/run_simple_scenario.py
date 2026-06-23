from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from graph.network_graph import MultiLayerTopology
from inputs.scenarios.simple_sat_hap_gs_scenario import build_scenario
from milp.milp_data import build_milp_input


def main() -> None:
    scenario = build_scenario()
    graph = MultiLayerTopology(scenario)
    milp_input = build_milp_input(scenario)
    print(f"Scenario: {scenario.scenario_id}")
    print(f"Nodes: {len(scenario.nodes)}")
    print(f"Links: {len(scenario.links)}")
    print(f"Demands: {len(scenario.demands)}")
    for t in scenario.time_slots:
        active = [link.link_id for link in graph.get_active_links(t)]
        print(f"t={t}: {active}")
    print(f"MILP capacity entries: {len(milp_input.capacity_bits)}")


if __name__ == "__main__":
    main()
