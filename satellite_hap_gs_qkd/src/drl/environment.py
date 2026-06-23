from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from scenario.network_scenario import Scenario

DemandId = str
LinkId = str
NodeId = str
TimeSlot = int


@dataclass
class DRLState:
    time_slot: TimeSlot
    link_capacity: Dict[LinkId, float]
    link_availability: Dict[LinkId, bool]
    demand: Dict[DemandId, float]
    qkp_storage: Dict[LinkId, float]
    node_status: Dict[NodeId, str]


@dataclass
class DRLAction:
    active_link_ids: List[LinkId]


@dataclass
class DRLStepResult:
    state: DRLState
    reward: float
    done: bool
    info: Dict[str, object] = field(default_factory=dict)


class MultiLayerQKDEnv:
    """Placeholder environment for the future DRL route."""

    def __init__(self, scenario: Scenario):
        scenario.validate()
        self.scenario = scenario
        self.current_index = 0

    def reset(self) -> DRLState:
        self.current_index = 0
        return self._build_state(self.scenario.time_slots[self.current_index])

    def step(self, action: DRLAction) -> DRLStepResult:
        raise NotImplementedError("DRL environment dynamics are not implemented in phase 1.")

    def _build_state(self, time_slot: TimeSlot) -> DRLState:
        link_capacity = {
            link.link_id: link.get_capacity(time_slot)
            for link in self.scenario.links.values()
        }
        link_availability = {
            link.link_id: link.is_available(time_slot)
            for link in self.scenario.links.values()
        }
        demand = {
            demand.demand_id: demand.get_requested_keys(time_slot)
            for demand in self.scenario.demands.values()
        }
        qkp_storage = {
            link_id: key_pool.get_stored_keys(time_slot)
            for link_id, key_pool in self.scenario.key_pools.items()
        }
        node_status = {
            node.node_id: node.status
            for node in self.scenario.nodes.values()
        }

        return DRLState(
            time_slot=time_slot,
            link_capacity=link_capacity,
            link_availability=link_availability,
            demand=demand,
            qkp_storage=qkp_storage,
            node_status=node_status,
        )
