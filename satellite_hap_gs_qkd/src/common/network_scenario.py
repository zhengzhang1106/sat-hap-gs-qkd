from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from common.key_pool import KeyPool
from common.network_demand import Demand
from common.network_node import Node
from common.network_types import DemandId, LinkId, NodeId, LinkType, NodeType, TimeSlot
from common.quantum_link import Link


@dataclass
class Scenario:
    scenario_id: str
    nodes: Dict[NodeId, Node]
    links: Dict[LinkId, Link]
    demands: Dict[DemandId, Demand]
    key_pools: Dict[LinkId, KeyPool]
    time_slots: List[TimeSlot]
    parameters: Dict[str, Any] = field(default_factory=dict)

    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        return [node for node in self.nodes.values() if node.node_type == node_type]

    def get_links_by_type(self, link_type: LinkType) -> List[Link]:
        return [link for link in self.links.values() if link.link_type == link_type]

    def get_active_links(self, time_slot: TimeSlot) -> List[Link]:
        return [link for link in self.links.values() if link.is_available(time_slot)]

    def get_demands_at(self, time_slot: TimeSlot) -> List[Demand]:
        return [
            demand
            for demand in self.demands.values()
            if demand.get_requested_keys(time_slot) > 0.0
        ]

    def validate(self) -> None:
        for link in self.links.values():
            if link.source not in self.nodes:
                raise ValueError(f"Link {link.link_id} has unknown source {link.source}.")
            if link.target not in self.nodes:
                raise ValueError(f"Link {link.link_id} has unknown target {link.target}.")

        for demand in self.demands.values():
            for node_id in (demand.source_gs, demand.target_gs):
                node = self.nodes.get(node_id)
                if node is None:
                    raise ValueError(f"Demand {demand.demand_id} uses unknown GS {node_id}.")
                if node.node_type != NodeType.GS:
                    raise ValueError(f"Demand {demand.demand_id} endpoint {node_id} is not GS.")

        for link_id in self.key_pools:
            if link_id not in self.links:
                raise ValueError(f"KeyPool references unknown link {link_id}.")
