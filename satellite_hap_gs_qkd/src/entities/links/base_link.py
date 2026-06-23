from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from entities.links.link_type import LinkType
from qkp.key_pool import KeyPool


@dataclass
class BaseLink:
    """Common physical-link interface.

    ``capacity_by_time`` stores key generation rate in bps. MILP/QKP modules
    should call ``capacity_bits_at`` to convert rate into key bits per slot.
    """

    link_id: str
    source: str
    target: str
    link_type: LinkType
    distance_km: float = 0.0
    capacity_by_time: Dict[int, float] = field(default_factory=dict)
    availability_by_time: Dict[int, bool] = field(default_factory=dict)
    directed: bool = False
    key_pool: Optional[KeyPool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def key_rate_bps_at(self, time_slot: int) -> float:
        if not self.is_available(time_slot):
            return 0.0
        return float(self.capacity_by_time.get(time_slot, 0.0))

    def capacity_bits_at(self, time_slot: int, slot_duration_seconds: float) -> float:
        return self.key_rate_bps_at(time_slot) * float(slot_duration_seconds)

    def get_capacity(self, time_slot: int) -> float:
        """Backward-compatible alias returning key rate in bps."""

        return self.key_rate_bps_at(time_slot)

    def get_capacity_bits(self, time_slot: int, slot_duration_seconds: float) -> float:
        return self.capacity_bits_at(time_slot, slot_duration_seconds)

    def is_available(self, time_slot: int) -> bool:
        if time_slot in self.availability_by_time:
            return self.availability_by_time[time_slot]
        return self.capacity_by_time.get(time_slot, 0.0) > 0.0

    def endpoints(self) -> Tuple[str, str]:
        return self.source, self.target
