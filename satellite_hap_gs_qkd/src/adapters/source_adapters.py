from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from entities.links.inter_layer_link import InterLayerLink
from entities.links.platform_ground_link import PlatformGroundLink
from entities.links.satellite_ground_link import SatelliteGroundLink
from entities.nodes.air_platform import HighAltitudePlatform
from entities.nodes.ground_station import GroundStation
from entities.nodes.satellite import Satellite
from qkp.key_pool import KeyPool

SATELLITE_QKD_REPO = "zhengzhang1106/satellite-QKD"
HAP_QKD_REPO = "zhengzhang1106/HAP-QKD"


def capacity_list_to_time_dict(time_slots: Iterable[int], values: Iterable[float]) -> Dict[int, float]:
    return {int(t): float(v) for t, v in zip(time_slots, values)}


def availability_from_capacity(capacity_by_time: Dict[int, float]) -> Dict[int, bool]:
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
) -> GroundStation:
    return GroundStation(
        node_id=node_id,
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
            "storage_unit": "bits",
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
) -> HighAltitudePlatform:
    return HighAltitudePlatform(
        node_id=node_id,
        position=(float(longitude_by_time[0]), float(latitude_by_time[0]), float(altitude_by_time_km[0])),
        rx_tx_limit=min(rx_limit, tx_limit),
        rx_limit=rx_limit,
        tx_limit=tx_limit,
        storage_capacity=float(storage_capacity),
        altitude_km=float(altitude_by_time_km[0]),
        trajectory_id=tag or node_id,
        metadata={
            "source_repository": HAP_QKD_REPO,
            "tag": tag or node_id,
            "longitude_by_time": [float(v) for v in longitude_by_time],
            "latitude_by_time": [float(v) for v in latitude_by_time],
            "altitude_by_time_km": [float(v) for v in altitude_by_time_km],
            "storage_unit": "bits",
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
) -> Satellite:
    return Satellite(
        node_id=node_id,
        position=(0.0, 0.0, float(altitude_km)),
        rx_tx_limit=min(rx_limit, tx_limit),
        rx_limit=rx_limit,
        tx_limit=tx_limit,
        storage_capacity=float(storage_capacity),
        altitude_km=float(altitude_km),
        orbit_label=orbit_label,
        metadata={
            "source_repository": SATELLITE_QKD_REPO,
            "tag": tag or node_id,
            "orbit_label": orbit_label,
            "altitude_km": float(altitude_km),
            "storage_unit": "bits",
        },
    )


def build_sat_gs_link(link_id: str, source: str, target: str, distance_km: float, capacity_by_time: Dict[int, float], directed: bool = True) -> SatelliteGroundLink:
    return SatelliteGroundLink(
        link_id=link_id,
        source=source,
        target=target,
        distance_km=float(distance_km),
        capacity_by_time=dict(capacity_by_time),
        availability_by_time=availability_from_capacity(capacity_by_time),
        directed=directed,
        metadata={"source_repository": SATELLITE_QKD_REPO, "capacity_source": "satellite visibility/weather/SatQuMA-style SKR", "capacity_unit": "bps"},
    )


def build_hap_gs_link(link_id: str, source: str, target: str, distance_km: float, capacity_by_time: Dict[int, float], directed: bool = True) -> PlatformGroundLink:
    return PlatformGroundLink(
        link_id=link_id,
        source=source,
        target=target,
        distance_km=float(distance_km),
        capacity_by_time=dict(capacity_by_time),
        availability_by_time=availability_from_capacity(capacity_by_time),
        directed=directed,
        metadata={"source_repository": HAP_QKD_REPO, "capacity_source": "HAP-GS trajectory/channel/SKR", "capacity_unit": "bps"},
    )


def build_sat_hap_placeholder_link(link_id: str, source: str, target: str, distance_km: float, capacity_by_time: Dict[int, float], directed: bool = True) -> InterLayerLink:
    return InterLayerLink(
        link_id=link_id,
        source=source,
        target=target,
        distance_km=float(distance_km),
        capacity_by_time=dict(capacity_by_time),
        availability_by_time=availability_from_capacity(capacity_by_time),
        directed=directed,
        metadata={"source_repository": "placeholder", "capacity_source": "manual placeholder; SAT-HAP physical/SKR model not in source repos yet", "capacity_unit": "bps", "model_status": "missing_source_model"},
    )


def build_key_pools_for_links(links: Dict[str, object], time_slots: Iterable[int], capacity: float, initial_keys: float = 0.0) -> Dict[str, KeyPool]:
    stored = {int(t): float(initial_keys) for t in time_slots}
    return {
        link_id: KeyPool(
            link_id=link_id,
            capacity=float(capacity),
            stored_keys_by_time=dict(stored),
            metadata={"source_repository": link.metadata.get("source_repository"), "link_type": link.link_type.value, "storage_unit": "bits"},
        )
        for link_id, link in links.items()
    }
