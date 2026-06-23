from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from common.network_types import DemandId, NodeId, TimeSlot


@dataclass
class Demand:
    demand_id: DemandId
    source_gs: NodeId
    target_gs: NodeId
    requested_keys_by_time: Dict[TimeSlot, float]
    priority: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_requested_keys(self, time_slot: TimeSlot) -> float:
        return float(self.requested_keys_by_time.get(time_slot, 0.0))
