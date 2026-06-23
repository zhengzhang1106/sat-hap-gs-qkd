from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from common.network_types import LinkId, LinkType, NodeId, TimeSlot


@dataclass
class Link:
    link_id: LinkId
    source: NodeId
    target: NodeId
    link_type: LinkType
    distance_km: float = 0.0
    capacity_by_time: Dict[TimeSlot, float] = field(default_factory=dict)
    availability_by_time: Dict[TimeSlot, bool] = field(default_factory=dict)
    directed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_capacity(self, time_slot: TimeSlot) -> float:
        if not self.is_available(time_slot):
            return 0.0
        return float(self.capacity_by_time.get(time_slot, 0.0))

    def is_available(self, time_slot: TimeSlot) -> bool:
        if time_slot in self.availability_by_time:
            return self.availability_by_time[time_slot]
        return self.capacity_by_time.get(time_slot, 0.0) > 0.0

    def endpoints(self) -> Tuple[NodeId, NodeId]:
        return self.source, self.target
