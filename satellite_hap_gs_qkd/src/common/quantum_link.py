"""Compatibility exports for link models.

New code should import from ``entities.links``.
"""

from entities.links.base_link import BaseLink
from entities.links.inter_layer_link import InterLayerLink
from entities.links.platform_ground_link import PlatformGroundLink
from entities.links.satellite_ground_link import SatelliteGroundLink

Link = BaseLink

__all__ = [
    "BaseLink",
    "InterLayerLink",
    "Link",
    "PlatformGroundLink",
    "SatelliteGroundLink",
]
