from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from common.network_types import LinkType, NodeType
from inputs.scenarios.source_mapped_multilayer_scenario import build_scenario
from milp.milp_data import build_milp_input
from topology.network_topology import MultiLayerTopology


def main() -> None:
    scenario = build_scenario()
    topology = MultiLayerTopology(scenario)
    milp_input = build_milp_input(scenario)

    node_counts = Counter(node.node_type.value for node in scenario.nodes.values())
    link_counts = Counter(link.link_type.value for link in scenario.links.values())
    source_counts = Counter(link.metadata.get("source_repository", "unknown") for link in scenario.links.values())

    print("=" * 80)
    print(f"Scenario: {scenario.scenario_id}")
    print(f"Time slots: {scenario.time_slots}")
    print("-" * 80)
    print("Node counts:")
    for node_type in (NodeType.GS, NodeType.SAT, NodeType.HAP):
        print(f"  {node_type.value}: {node_counts[node_type.value]}")

    print("-" * 80)
    print("Logical link counts:")
    for link_type in (LinkType.SAT_GS, LinkType.SAT_HAP, LinkType.HAP_GS):
        print(f"  {link_type.value}: {link_counts[link_type.value]}")

    print("-" * 80)
    print("Links by source repository:")
    for source, count in sorted(source_counts.items()):
        print(f"  {source}: {count}")

    print("-" * 80)
    print("Active logical links by time slot:")
    for t in scenario.time_slots:
        active = [link.link_id for link in topology.get_active_links(t)]
        print(f"  t={t}: {active}")

    print("-" * 80)
    print("SAT-HAP model status:")
    for link in scenario.get_links_by_type(LinkType.SAT_HAP):
        print(f"  {link.link_id}: {link.metadata.get('capacity_source')}")

    print("-" * 80)
    print("MILP input dimensions:")
    print(f"  nodes={len(milp_input.node_ids)}")
    print(f"  logical_links={len(milp_input.link_ids)}")
    print(f"  demands={len(milp_input.demand_ids)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
