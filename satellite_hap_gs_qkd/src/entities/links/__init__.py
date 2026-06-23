"""Physical QKD link models."""

from entities.links.base_link import BaseLink
from entities.links.hap_gs_link import HAPGSLink
from entities.links.link_type import LinkType
from entities.links.satellite_gs_link import SatelliteGSLink
from entities.links.satellite_hap_link import SatelliteHAPLink

__all__ = [
    "BaseLink",
    "HAPGSLink",
    "LinkType",
    "SatelliteGSLink",
    "SatelliteHAPLink",
]
