from __future__ import annotations

from typing import Tuple

from entities.links.link_type import LinkType
from entities.nodes.node_type import NodeType

Position = Tuple[float, float, float]
TimeSlot = int
NodeId = str
LinkId = str
DemandId = str

__all__ = [
    "DemandId",
    "LinkId",
    "LinkType",
    "NodeId",
    "NodeType",
    "Position",
    "TimeSlot",
]
