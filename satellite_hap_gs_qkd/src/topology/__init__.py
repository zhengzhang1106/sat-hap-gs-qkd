"""Topology helpers for multi-layer QKD networks."""

from topology.network_topology import MultiLayerTopology
from topology.source_adapters import (
    HAP_QKD_REPO,
    SATELLITE_QKD_REPO,
    availability_from_capacity,
    build_ground_station_node,
    build_hap_gs_link,
    build_hap_node,
    build_key_pools_for_links,
    build_sat_gs_link,
    build_sat_hap_placeholder_link,
    build_satellite_node,
    capacity_list_to_time_dict,
)

__all__ = [
    "HAP_QKD_REPO",
    "MultiLayerTopology",
    "SATELLITE_QKD_REPO",
    "availability_from_capacity",
    "build_ground_station_node",
    "build_hap_gs_link",
    "build_hap_node",
    "build_key_pools_for_links",
    "build_sat_gs_link",
    "build_sat_hap_placeholder_link",
    "build_satellite_node",
    "capacity_list_to_time_dict",
]
