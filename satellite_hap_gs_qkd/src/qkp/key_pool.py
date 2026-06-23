from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class KeyPool:
    """Pairwise key storage associated with a physical QKD link.

    All quantities in this class are key bits. Link objects hold the physical
    key-rate profile and can reference this key pool.
    """

    link_id: str
    capacity: float
    stored_keys_by_time: Dict[int, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def capacity_bits(self) -> float:
        return float(self.capacity)

    def get_stored_keys(self, time_slot: int) -> float:
        return float(self.stored_keys_by_time.get(time_slot, 0.0))

    def set_stored_keys(self, time_slot: int, amount: float) -> None:
        self.stored_keys_by_time[time_slot] = min(float(amount), self.capacity_bits)

    def add_keys(self, time_slot: int, amount: float) -> float:
        current = self.get_stored_keys(time_slot)
        updated = min(current + float(amount), self.capacity_bits)
        self.stored_keys_by_time[time_slot] = updated
        return updated

    def consume_keys(self, time_slot: int, amount: float) -> bool:
        current = self.get_stored_keys(time_slot)
        amount = float(amount)
        if current < amount:
            return False
        self.stored_keys_by_time[time_slot] = current - amount
        return True
