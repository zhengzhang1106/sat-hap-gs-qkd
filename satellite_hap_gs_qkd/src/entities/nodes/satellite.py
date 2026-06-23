from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from entities.nodes.base_node import BaseNode
from entities.nodes.node_type import NodeType


@dataclass
class Satellite(BaseNode):
    """Satellite trusted-relay node.

    Orbit-specific information is intentionally optional because the current
    framework can either read precomputed SatQuMA/SatQuMA-style key-rate traces
    or later compute them from orbit and weather inputs.
    """

    node_type: NodeType = field(default=NodeType.SAT, init=False)
    altitude_km: Optional[float] = None
    raan_deg: Optional[float] = None
    inclination_deg: Optional[float] = None
    orbit_label: Optional[str] = None
