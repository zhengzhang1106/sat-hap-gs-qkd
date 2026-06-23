from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from common.network_types import NodeId, NodeType, Position


@dataclass
class Node:
    node_id: NodeId
    node_type: NodeType
    position: Optional[Position] = None
    rx_tx_limit: int = 1
    rx_limit: Optional[int] = None
    tx_limit: Optional[int] = None
    storage_capacity: float = 0.0
    status: str = "active"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_available(self) -> bool:
        return self.status == "active"

    def get_rx_limit(self) -> int:
        return self.rx_limit if self.rx_limit is not None else self.rx_tx_limit

    def get_tx_limit(self) -> int:
        return self.tx_limit if self.tx_limit is not None else self.rx_tx_limit
