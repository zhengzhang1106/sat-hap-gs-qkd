"""Compatibility exports for the split common model files.

New code should import from the concept-specific files directly, for example
``common.network_node`` or ``common.quantum_link``.
"""

from common.key_pool import KeyPool
from common.network_demand import Demand
from common.network_node import Node
from common.network_scenario import Scenario
from common.network_types import DemandId, LinkId, LinkType, NodeId, NodeType, Position, TimeSlot
from common.quantum_link import Link

__all__ = [
    "Demand",
    "DemandId",
    "KeyPool",
    "Link",
    "LinkId",
    "LinkType",
    "Node",
    "NodeId",
    "NodeType",
    "Position",
    "Scenario",
    "TimeSlot",
]
