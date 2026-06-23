from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from entities.links.link_type import LinkType
from entities.nodes.node_type import NodeType
from graph.network_graph import MultiLayerTopology
from inputs.scenarios.simple_sat_hap_gs_scenario import build_scenario
from milp.milp_data import build_milp_input


def test_simple_scenario_contract() -> None:
    scenario = build_scenario()
    assert len(scenario.get_nodes_by_type(NodeType.GS)) == 2
    assert len(scenario.get_links_by_type(LinkType.SAT_HAP)) == 1


def test_graph_contract() -> None:
    graph = MultiLayerTopology(build_scenario())
    assert sorted(graph.get_nodes()) == ["GS_A", "GS_B", "HAP_1", "SAT_1"]
    assert len(graph.get_active_links(0)) == 3
    assert len(graph.get_active_links(2)) == 2


def test_milp_input_contract() -> None:
    milp_input = build_milp_input(build_scenario())
    assert milp_input.capacity[("L_SAT1_HAP1", 1)] == 900.0
    assert milp_input.capacity_bits[("L_SAT1_HAP1", 1)] == 900.0 * 600.0
    assert milp_input.demand[("D_GSA_GSB", 0)] == 500.0
