from __future__ import annotations

from enum import Enum
from typing import Tuple


class NodeType(str, Enum):
    GS = "GS"
    SAT = "SAT"
    HAP = "HAP"


class LinkType(str, Enum):
    SAT_GS = "SAT-GS"
    SAT_HAP = "SAT-HAP"
    HAP_GS = "HAP-GS"


Position = Tuple[float, float, float]
TimeSlot = int
NodeId = str
LinkId = str
DemandId = str
