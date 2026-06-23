from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from entities.nodes.base_node import BaseNode
from entities.nodes.node_type import NodeType


@dataclass
class HighAltitudePlatform(BaseNode):
    node_type: NodeType = field(default=NodeType.HAP, init=False)
    altitude_km: Optional[float] = None
    trajectory_id: Optional[str] = None
