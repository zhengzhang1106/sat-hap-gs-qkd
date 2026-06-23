from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from common.network_scenario import Scenario
from common.network_types import DemandId, LinkId, NodeId, TimeSlot


@dataclass
class MILPInput:
    scenario_id: str
    time_slots: List[TimeSlot]
    node_ids: List[NodeId]
    link_ids: List[LinkId]
    demand_ids: List[DemandId]
    active_links_by_time: Dict[TimeSlot, List[LinkId]]
    capacity: Dict[Tuple[LinkId, TimeSlot], float]
    capacity_bits: Dict[Tuple[LinkId, TimeSlot], float]
    demand: Dict[Tuple[DemandId, TimeSlot], float]
    initial_qkp: Dict[LinkId, float]
    slot_duration_seconds: float
    parameters: Dict[str, object] = field(default_factory=dict)


@dataclass
class MILPResult:
    status: str
    objective_value: float = 0.0
    served_keys_by_demand: Dict[DemandId, float] = field(default_factory=dict)
    selected_links_by_time: Dict[TimeSlot, List[LinkId]] = field(default_factory=dict)
    final_qkp: Dict[LinkId, float] = field(default_factory=dict)
    metadata: Dict[str, object] = field(default_factory=dict)


def build_milp_input(scenario: Scenario) -> MILPInput:
    scenario.validate()
    slot_duration_seconds = scenario.get_time_slot_duration_seconds()

    capacity = {}
    capacity_bits = {}
    active_links_by_time = {}
    for t in scenario.time_slots:
        active_links = []
        for link in scenario.links.values():
            capacity[(link.link_id, t)] = link.key_rate_bps_at(t)
            capacity_bits[(link.link_id, t)] = link.capacity_bits_at(t, slot_duration_seconds)
            if link.is_available(t):
                active_links.append(link.link_id)
        active_links_by_time[t] = active_links

    demand = {}
    for d in scenario.demands.values():
        for t in scenario.time_slots:
            demand[(d.demand_id, t)] = d.get_requested_keys(t)

    initial_time = scenario.time_slots[0] if scenario.time_slots else 0
    initial_qkp = {
        link_id: key_pool.get_stored_keys(initial_time)
        for link_id, key_pool in scenario.key_pools.items()
    }

    parameters = dict(scenario.parameters)
    parameters.setdefault("capacity_unit", "bps")
    parameters.setdefault("capacity_bits_unit", "bits_per_time_slot")
    parameters.setdefault("demand_unit", "bits_per_time_slot")
    parameters.setdefault("qkp_unit", "bits")

    return MILPInput(
        scenario_id=scenario.scenario_id,
        time_slots=list(scenario.time_slots),
        node_ids=list(scenario.nodes.keys()),
        link_ids=list(scenario.links.keys()),
        demand_ids=list(scenario.demands.keys()),
        active_links_by_time=active_links_by_time,
        capacity=capacity,
        capacity_bits=capacity_bits,
        demand=demand,
        initial_qkp=initial_qkp,
        slot_duration_seconds=slot_duration_seconds,
        parameters=parameters,
    )
