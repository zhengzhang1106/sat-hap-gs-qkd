from __future__ import annotations

from typing import List, Optional

import networkx as nx

from common.network_node import Node
from common.network_scenario import Scenario
from common.network_types import LinkId, LinkType, NodeId, NodeType, TimeSlot
from common.quantum_link import Link


class MultiLayerTopology:
    """
    Physical and logical topology for a satellite-HAP-GS QKD scenario.

    The graph uses link ids as MultiGraph edge keys so later modules can keep
    different link layers separate.
    """

    def __init__(self, scenario: Scenario):
        scenario.validate()
        self.scenario = scenario
        self.graph = nx.MultiGraph()
        self._build_graph()

    def _build_graph(self) -> None:
        for node in self.scenario.nodes.values():
            self.graph.add_node(
                node.node_id,
                node_type=node.node_type.value,
                position=node.position,
                rx_tx_limit=node.rx_tx_limit,
                storage_capacity=node.storage_capacity,
                status=node.status,
                metadata=node.metadata,
            )

        for link in self.scenario.links.values():
            self.graph.add_edge(
                link.source,
                link.target,
                key=link.link_id,
                link_id=link.link_id,
                link_type=link.link_type.value,
                distance_km=link.distance_km,
                capacity_by_time=link.capacity_by_time,
                availability_by_time=link.availability_by_time,
                directed=link.directed,
                metadata=link.metadata,
            )

    def get_node(self, node_id: NodeId) -> Optional[Node]:
        return self.scenario.nodes.get(node_id)

    def get_link(self, link_id: LinkId) -> Optional[Link]:
        return self.scenario.links.get(link_id)

    def get_nodes(self) -> List[NodeId]:
        return list(self.graph.nodes)

    def get_links(self) -> List[Link]:
        return list(self.scenario.links.values())

    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        return self.scenario.get_nodes_by_type(node_type)

    def get_links_by_type(self, link_type: LinkType) -> List[Link]:
        return self.scenario.get_links_by_type(link_type)

    def get_outgoing_links(self, node_id: NodeId) -> List[Link]:
        return [link for link in self.scenario.links.values() if link.source == node_id]

    def get_incoming_links(self, node_id: NodeId) -> List[Link]:
        return [link for link in self.scenario.links.values() if link.target == node_id]

    def get_neighbors(self, node_id: NodeId) -> List[NodeId]:
        return list(self.graph.neighbors(node_id))

    def get_active_links(self, time_slot: TimeSlot) -> List[Link]:
        return self.scenario.get_active_links(time_slot)

    def get_link_capacity(self, link_id: LinkId, time_slot: TimeSlot) -> float:
        link = self.scenario.links[link_id]
        return link.get_capacity(time_slot)

    def to_networkx(self) -> nx.MultiGraph:
        return self.graph.copy()

    def show_topology(self) -> None:
        print("Show the current satellite-HAP-GS topology:")
        print(f"  Nodes: {list(self.graph.nodes(data=True))}")
        print("  Links:")
        for u, v, key, data in self.graph.edges(keys=True, data=True):
            print(f"    ({u}, {v}, key={key}) -> {data}")
        print("\n")
