from __future__ import annotations

from enum import Enum


class NodeType(str, Enum):
    """Physical node categories in the multi-layer QKD network."""

    GS = "GS"
    SAT = "SAT"
    HAP = "HAP"
