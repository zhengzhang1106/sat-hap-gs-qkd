from __future__ import annotations

from typing import List, Optional

import networkx as nx

from entities.links.base_link import BaseLink
from entities.links.link_type import LinkType
from entities.nodes.base_node import BaseNode
from entities.nodes.node_type import NodeType
from scenario.network_scenario import Scenario


class MultiLayerNetworkGraph:
    """NetworkX graph view for a Satellite-HAP-GS QKD scenario."""

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

    def get_node(self, node_id: str) -> Optional[BaseNode]:
        return self.scenario.nodes.get(node_id)

    def get_link(self, link_id: str) -> Optional[BaseLink]:
        return self.scenario.links.get(link_id)

    def get_nodes(self) -> List[str]:
        return list(self.graph.nodes)

    def get_links(self) -> List[BaseLink]:
        return list(self.scenario.links.values())

    def get_nodes_by_type(self, node_type: NodeType) -> List[BaseNode]:
        return self.scenario.get_nodes_by_type(node_type)

    def get_links_by_type(self, link_type: LinkType) -> List[BaseLink]:
        return self.scenario.get_links_by_type(link_type)

    def get_outgoing_links(self, node_id: str) -> List[BaseLink]:
        return [link for link in self.scenario.links.values() if link.source == node_id]

    def get_incoming_links(self, node_id: str) -> List[BaseLink]:
        return [link for link in self.scenario.links.values() if link.target == node_id]

    def get_neighbors(self, node_id: str) -> List[str]:
        return list(self.graph.neighbors(node_id))

    def get_active_links(self, time_slot: int) -> List[BaseLink]:
        return self.scenario.get_active_links(time_slot)

    def get_link_capacity(self, link_id: str, time_slot: int) -> float:
        return self.scenario.links[link_id].get_capacity(time_slot)

    def get_link_capacity_bits(self, link_id: str, time_slot: int) -> float:
        return self.scenario.links[link_id].capacity_bits_at(
            time_slot,
            self.scenario.get_time_slot_duration_seconds(),
        )

    def to_networkx(self) -> nx.MultiGraph:
        return self.graph.copy()


MultiLayerTopology = MultiLayerNetworkGraph
