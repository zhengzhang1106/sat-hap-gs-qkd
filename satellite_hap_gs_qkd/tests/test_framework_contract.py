from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from common.network_types import LinkType, NodeType
from drl.environment import MultiLayerQKDEnv
from inputs.scenarios.simple_sat_hap_gs_scenario import build_scenario
from milp.milp_data import build_milp_input
from topology.network_topology import MultiLayerTopology


def test_simple_scenario_contract() -> None:
    scenario = build_scenario()

    assert scenario.scenario_id == "simple_sat_hap_gs"
    assert len(scenario.nodes) == 4
    assert len(scenario.links) == 3
    assert len(scenario.demands) == 1
    assert len(scenario.key_pools) == 3
    assert len(scenario.get_nodes_by_type(NodeType.GS)) == 2
    assert len(scenario.get_links_by_type(LinkType.SAT_HAP)) == 1


def test_topology_contract() -> None:
    scenario = build_scenario()
    topology = MultiLayerTopology(scenario)

    assert sorted(topology.get_nodes()) == ["GS_A", "GS_B", "HAP_1", "SAT_1"]
    assert len(topology.get_active_links(0)) == 3
    assert len(topology.get_active_links(2)) == 2
    assert topology.get_link_capacity("L_SAT1_GSA", 2) == 0.0


def test_milp_input_contract() -> None:
    scenario = build_scenario()
    milp_input = build_milp_input(scenario)

    assert milp_input.scenario_id == scenario.scenario_id
    assert milp_input.capacity[("L_SAT1_HAP1", 1)] == 900.0
    assert milp_input.demand[("D_GSA_GSB", 0)] == 500.0
    assert "L_SAT1_GSA" not in milp_input.active_links_by_time[2]


def test_drl_environment_contract() -> None:
    scenario = build_scenario()
    env = MultiLayerQKDEnv(scenario)
    state = env.reset()

    assert state.time_slot == 0
    assert state.link_capacity["L_SAT1_GSA"] == 1000.0
    assert state.link_availability["L_SAT1_GSA"] is True
    assert state.demand["D_GSA_GSB"] == 500.0
    assert state.node_status["SAT_1"] == "active"
