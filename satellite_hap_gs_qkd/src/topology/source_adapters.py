from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from common.key_pool import KeyPool
from common.network_node import Node
from common.network_types import LinkType, NodeType, TimeSlot
from common.quantum_link import Link


SATELLITE_QKD_REPO = "zhengzhang1106/satellite-QKD"
HAP_QKD_REPO = "zhengzhang1106/HAP-QKD"


def capacity_list_to_time_dict(time_slots: Iterable[TimeSlot], values: Iterable[float]) -> Dict[TimeSlot, float]:
    return {int(t): float(v) for t, v in zip(time_slots, values)}


def availability_from_capacity(capacity_by_time: Dict[TimeSlot, float]) -> Dict[TimeSlot, bool]:
    return {t: capacity > 0.0 for t, capacity in capacity_by_time.items()}


def build_ground_station_node(
    node_id: str,
    longitude_deg: float,
    latitude_deg: float,
    rx_limit: int,
    tx_limit: int,
    storage_capacity: float,
    source_repository: str,
    tag: Optional[str] = None,
) -> Node:
    return Node(
        node_id=node_id,
        node_type=NodeType.GS,
        position=(float(longitude_deg), float(latitude_deg), 0.0),
        rx_tx_limit=min(rx_limit, tx_limit),
        rx_limit=rx_limit,
        tx_limit=tx_limit,
        storage_capacity=float(storage_capacity),
        metadata={
            "source_repository": source_repository,
            "tag": tag or node_id,
            "longitude_deg": float(longitude_deg),
            "latitude_deg": float(latitude_deg),
        },
    )


def build_hap_node(
    node_id: str,
    longitude_by_time: List[float],
    latitude_by_time: List[float],
    altitude_by_time_km: List[float],
    rx_limit: int,
    tx_limit: int,
    storage_capacity: float,
    tag: Optional[str] = None,
) -> Node:
    initial_position = (
        float(longitude_by_time[0]),
        float(latitude_by_time[0]),
        float(altitude_by_time_km[0]),
    )
    return Node(
        node_id=node_id,
        node_type=NodeType.HAP,
        position=initial_position,
        rx_tx_limit=min(rx_limit, tx_limit),
        rx_limit=rx_limit,
        tx_limit=tx_limit,
        storage_capacity=float(storage_capacity),
        metadata={
            "source_repository": HAP_QKD_REPO,
            "tag": tag or node_id,
            "longitude_by_time": [float(v) for v in longitude_by_time],
            "latitude_by_time": [float(v) for v in latitude_by_time],
            "altitude_by_time_km": [float(v) for v in altitude_by_time_km],
        },
    )


def build_satellite_node(
    node_id: str,
    altitude_km: float,
    rx_limit: int,
    tx_limit: int,
    storage_capacity: float,
    orbit_label: str,
    tag: Optional[str] = None,
) -> Node:
    return Node(
        node_id=node_id,
        node_type=NodeType.SAT,
        position=(0.0, 0.0, float(altitude_km)),
        rx_tx_limit=min(rx_limit, tx_limit),
        rx_limit=rx_limit,
        tx_limit=tx_limit,
        storage_capacity=float(storage_capacity),
        metadata={
            "source_repository": SATELLITE_QKD_REPO,
            "tag": tag or node_id,
            "orbit_label": orbit_label,
            "altitude_km": float(altitude_km),
        },
    )


def build_sat_gs_link(
    link_id: str,
    source: str,
    target: str,
    distance_km: float,
    capacity_by_time: Dict[TimeSlot, float],
    directed: bool = True,
) -> Link:
    return Link(
        link_id=link_id,
        source=source,
        target=target,
        link_type=LinkType.SAT_GS,
        distance_km=float(distance_km),
        capacity_by_time=dict(capacity_by_time),
        availability_by_time=availability_from_capacity(capacity_by_time),
        directed=directed,
        metadata={
            "source_repository": SATELLITE_QKD_REPO,
            "capacity_source": "satellite orbit/visibility/SatQuMA-style SKR",
        },
    )


def build_hap_gs_link(
    link_id: str,
    source: str,
    target: str,
    distance_km: float,
    capacity_by_time: Dict[TimeSlot, float],
    directed: bool = True,
) -> Link:
    return Link(
        link_id=link_id,
        source=source,
        target=target,
        link_type=LinkType.HAP_GS,
        distance_km=float(distance_km),
        capacity_by_time=dict(capacity_by_time),
        availability_by_time=availability_from_capacity(capacity_by_time),
        directed=directed,
        metadata={
            "source_repository": HAP_QKD_REPO,
            "capacity_source": "HAP-GS trajectory/channel/SKR",
        },
    )


def build_sat_hap_placeholder_link(
    link_id: str,
    source: str,
    target: str,
    distance_km: float,
    capacity_by_time: Dict[TimeSlot, float],
    directed: bool = True,
) -> Link:
    return Link(
        link_id=link_id,
        source=source,
        target=target,
        link_type=LinkType.SAT_HAP,
        distance_km=float(distance_km),
        capacity_by_time=dict(capacity_by_time),
        availability_by_time=availability_from_capacity(capacity_by_time),
        directed=directed,
        metadata={
            "source_repository": "placeholder",
            "capacity_source": "manual placeholder; SAT-HAP physical/SKR model not in source repos yet",
            "model_status": "missing_source_model",
        },
    )


def build_key_pools_for_links(
    links: Dict[str, Link],
    time_slots: Iterable[TimeSlot],
    capacity: float,
    initial_keys: float = 0.0,
) -> Dict[str, KeyPool]:
    stored = {int(t): float(initial_keys) for t in time_slots}
    return {
        link_id: KeyPool(
            link_id=link_id,
            capacity=float(capacity),
            stored_keys_by_time=dict(stored),
            metadata={
                "source_repository": link.metadata.get("source_repository"),
                "link_type": link.link_type.value,
            },
        )
        for link_id, link in links.items()
    }
