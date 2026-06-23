from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from entities.links.base_link import BaseLink
from entities.links.link_type import LinkType
from entities.nodes.base_node import BaseNode
from entities.nodes.node_type import NodeType
from qkp.key_pool import KeyPool
from services.service_demand import Demand


@dataclass
class Scenario:
    """Complete input instance for topology, MILP, and later DRL modules."""

    scenario_id: str
    nodes: Dict[str, BaseNode]
    links: Dict[str, BaseLink]
    demands: Dict[str, Demand]
    key_pools: Dict[str, KeyPool]
    time_slots: List[int]
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for link_id, key_pool in self.key_pools.items():
            link = self.links.get(link_id)
            if link is not None:
                link.key_pool = key_pool

    def get_nodes_by_type(self, node_type: NodeType) -> List[BaseNode]:
        return [node for node in self.nodes.values() if node.node_type == node_type]

    def get_links_by_type(self, link_type: LinkType) -> List[BaseLink]:
        return [link for link in self.links.values() if link.link_type == link_type]

    def get_active_links(self, time_slot: int) -> List[BaseLink]:
        return [link for link in self.links.values() if link.is_available(time_slot)]

    def get_demands_at(self, time_slot: int) -> List[Demand]:
        return [
            demand
            for demand in self.demands.values()
            if demand.get_requested_keys(time_slot) > 0.0
        ]

    def get_time_slot_duration_seconds(self) -> float:
        if "time_slot_duration_seconds" in self.parameters:
            return float(self.parameters["time_slot_duration_seconds"])
        if "time_slot_duration_minutes" in self.parameters:
            return float(self.parameters["time_slot_duration_minutes"]) * 60.0
        return 1.0

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
