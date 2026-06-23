from __future__ import annotations

from dataclasses import dataclass, field

from entities.nodes.base_node import BaseNode
from entities.nodes.node_type import NodeType


@dataclass
class GroundStation(BaseNode):
    """Terrestrial QKD node and GS-pair demand endpoint."""

    node_type: NodeType = field(default=NodeType.GS, init=False)
    data_center_count: int = 1
