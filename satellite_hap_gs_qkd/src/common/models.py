"""Compatibility exports.

Canonical imports now live under ``entities/``, ``qkp/``, ``services/``, and
``scenario/``. This module is kept to avoid breaking old examples.
"""

from common.network_types import DemandId, LinkId, LinkType, NodeId, NodeType, Position, TimeSlot
from entities.links.base_link import BaseLink as Link
from entities.nodes.base_node import BaseNode as Node
from qkp.key_pool import KeyPool
from scenario.network_scenario import Scenario
from services.service_demand import Demand

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
