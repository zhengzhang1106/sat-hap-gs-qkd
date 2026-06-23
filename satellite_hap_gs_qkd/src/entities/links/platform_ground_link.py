from __future__ import annotations

from dataclasses import dataclass, field

from entities.links.base_link import BaseLink
from entities.links.link_type import LinkType


@dataclass
class PlatformGroundLink(BaseLink):
    link_type: LinkType = field(default=LinkType.HAP_GS, init=False)

    def key_rate_bps_at(self, time_slot: int) -> float:
        return super().key_rate_bps_at(time_slot)


HAPGSLink = PlatformGroundLink
