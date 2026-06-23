from __future__ import annotations

from enum import Enum


class LinkType(str, Enum):
    """Physical QKD link categories in the multi-layer network."""

    SAT_GS = "SAT-GS"
    SAT_HAP = "SAT-HAP"
    HAP_GS = "HAP-GS"
