from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from adapters.source_adapters import HAP_QKD_REPO, SATELLITE_QKD_REPO
from entities.links.link_type import LinkType
from entities.nodes.node_type import NodeType
from graph.network_graph import MultiLayerTopology
from inputs.scenarios.source_mapped_multilayer_scenario import build_scenario
from milp.milp_data import build_milp_input


def test_source_mapped_nodes_and_links_exist() -> None:
    scenario = build_scenario()
    assert len(scenario.get_nodes_by_type(NodeType.GS)) == 2
    assert len(scenario.get_nodes_by_type(NodeType.SAT)) == 1
    assert len(scenario.get_nodes_by_type(NodeType.HAP)) == 1
    assert len(scenario.get_links_by_type(LinkType.SAT_GS)) == 4
    assert len(scenario.get_links_by_type(LinkType.HAP_GS)) == 4
    assert len(scenario.get_links_by_type(LinkType.SAT_HAP)) == 2


def test_source_repository_labels_are_corrected() -> None:
    scenario = build_scenario()
    sat_gs_sources = {link.metadata["source_repository"] for link in scenario.get_links_by_type(LinkType.SAT_GS)}
    hap_gs_sources = {link.metadata["source_repository"] for link in scenario.get_links_by_type(LinkType.HAP_GS)}
    sat_hap_sources = {link.metadata["source_repository"] for link in scenario.get_links_by_type(LinkType.SAT_HAP)}
    assert sat_gs_sources == {SATELLITE_QKD_REPO}
    assert hap_gs_sources == {HAP_QKD_REPO}
    assert sat_hap_sources == {"placeholder"}


def test_directional_queries_and_milp_input() -> None:
    scenario = build_scenario()
    graph = MultiLayerTopology(scenario)
    milp_input = build_milp_input(scenario)
    assert len(graph.get_outgoing_links("GS_TIMMINS")) == 2
    assert len(graph.get_incoming_links("GS_TIMMINS")) == 2
    assert "L_SAT1_TO_GS_TIMMINS" not in milp_input.active_links_by_time[3]
    assert milp_input.capacity[("L_SAT1_TO_HAP1", 0)] == 600.0
    assert milp_input.capacity_bits[("L_SAT1_TO_HAP1", 0)] == 600.0 * 1800.0
    assert milp_input.demand[("D_TIMMINS_IROQUOIS", 2)] == 700.0


def test_sat_hap_is_explicitly_placeholder() -> None:
    scenario = build_scenario()
    for link in scenario.get_links_by_type(LinkType.SAT_HAP):
        assert link.metadata["model_status"] == "missing_source_model"
        assert "placeholder" in link.metadata["capacity_source"]
