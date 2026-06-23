from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from common.network_types import LinkId, TimeSlot


@dataclass
class KeyPool:
    link_id: LinkId
    capacity: float
    stored_keys_by_time: Dict[TimeSlot, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_stored_keys(self, time_slot: TimeSlot) -> float:
        return float(self.stored_keys_by_time.get(time_slot, 0.0))

    def set_stored_keys(self, time_slot: TimeSlot, amount: float) -> None:
        self.stored_keys_by_time[time_slot] = min(float(amount), self.capacity)

    def add_keys(self, time_slot: TimeSlot, amount: float) -> float:
        current = self.get_stored_keys(time_slot)
        updated = min(current + float(amount), self.capacity)
        self.stored_keys_by_time[time_slot] = updated
        return updated

    def consume_keys(self, time_slot: TimeSlot, amount: float) -> bool:
        current = self.get_stored_keys(time_slot)
        amount = float(amount)
        if current < amount:
            return False
        self.stored_keys_by_time[time_slot] = current - amount
        return True
