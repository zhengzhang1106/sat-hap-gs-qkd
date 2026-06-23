from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ServiceDemand:
    """GS-pair key request.

    ``requested_keys_by_time`` is measured in key bits per time slot.
    """

    demand_id: str
    source_gs: str
    target_gs: str
    requested_keys_by_time: Dict[int, float]
    priority: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_requested_keys(self, time_slot: int) -> float:
        return float(self.requested_keys_by_time.get(time_slot, 0.0))

    def requested_keys_bits_at(self, time_slot: int) -> float:
        return self.get_requested_keys(time_slot)


Demand = ServiceDemand
