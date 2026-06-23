"""Compatibility exports for node models.

New code should import from ``entities.nodes``.
"""

from entities.nodes.air_platform import HighAltitudePlatform
from entities.nodes.base_node import BaseNode, Position
from entities.nodes.ground_station import GroundStation
from entities.nodes.satellite import Satellite

Node = BaseNode
HAP = HighAltitudePlatform

__all__ = [
    "BaseNode",
    "GroundStation",
    "HAP",
    "HighAltitudePlatform",
    "Node",
    "Position",
    "Satellite",
]
