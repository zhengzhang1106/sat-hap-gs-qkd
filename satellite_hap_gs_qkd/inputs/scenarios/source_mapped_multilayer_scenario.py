from __future__ import annotations

from adapters.source_adapters import (
    HAP_QKD_REPO,
    SATELLITE_QKD_REPO,
    build_ground_station_node,
    build_hap_gs_link,
    build_hap_node,
    build_key_pools_for_links,
    build_sat_gs_link,
    build_sat_hap_placeholder_link,
    build_satellite_node,
)
from entities.links.base_link import BaseLink
from scenario.network_scenario import Scenario
from services.service_demand import Demand


def _add_bidirectional_link(links: dict[str, BaseLink], forward: BaseLink, reverse: BaseLink) -> None:
    physical_link_id = forward.metadata.get("physical_link_id", forward.link_id)
    forward.metadata["physical_link_id"] = physical_link_id
    reverse.metadata["physical_link_id"] = physical_link_id
    links[forward.link_id] = forward
    links[reverse.link_id] = reverse


def build_scenario() -> Scenario:
    time_slots = [0, 1, 2, 3]

    nodes = {
        "GS_TIMMINS": build_ground_station_node(
            node_id="GS_TIMMINS",
            longitude_deg=278.6695,
            latitude_deg=48.4758,
            rx_limit=1,
            tx_limit=1,
            storage_capacity=1e9,
            source_repository=HAP_QKD_REPO,
            tag="Timmins",
        ),
        "GS_IROQUOIS": build_ground_station_node(
            node_id="GS_IROQUOIS",
            longitude_deg=279.3186,
            latitude_deg=48.7669,
            rx_limit=1,
            tx_limit=1,
            storage_capacity=1e9,
            source_repository=HAP_QKD_REPO,
            tag="Iroquois Falls",
        ),
        "HAP_1": build_hap_node(
            node_id="HAP_1",
            longitude_by_time=[278.95, 279.00, 279.06, 279.10],
            latitude_by_time=[48.70, 48.74, 48.78, 48.82],
            altitude_by_time_km=[20.0, 20.0, 20.0, 20.0],
            rx_limit=1,
            tx_limit=1,
            storage_capacity=1e9,
            tag="HAP_1",
        ),
        "SAT_1": build_satellite_node(
            node_id="SAT_1",
            altitude_km=567.0,
            rx_limit=1,
            tx_limit=1,
            storage_capacity=1e9,
            orbit_label="RAAN_placeholder",
            tag="SAT_1",
        ),
    }

    links: dict[str, BaseLink] = {}

    sat_timmins = {0: 1200.0, 1: 900.0, 2: 300.0, 3: 0.0}
    sat_iroquois = {0: 0.0, 1: 700.0, 2: 950.0, 3: 500.0}
    _add_bidirectional_link(
        links,
        build_sat_gs_link("L_SAT1_TO_GS_TIMMINS", "SAT_1", "GS_TIMMINS", 567.0, sat_timmins),
        build_sat_gs_link("L_GS_TIMMINS_TO_SAT1", "GS_TIMMINS", "SAT_1", 567.0, sat_timmins),
    )
    _add_bidirectional_link(
        links,
        build_sat_gs_link("L_SAT1_TO_GS_IROQUOIS", "SAT_1", "GS_IROQUOIS", 570.0, sat_iroquois),
        build_sat_gs_link("L_GS_IROQUOIS_TO_SAT1", "GS_IROQUOIS", "SAT_1", 570.0, sat_iroquois),
    )

    hap_timmins = {0: 1500.0, 1: 1450.0, 2: 1300.0, 3: 1100.0}
    hap_iroquois = {0: 900.0, 1: 1200.0, 2: 1400.0, 3: 1300.0}
    _add_bidirectional_link(
        links,
        build_hap_gs_link("L_HAP1_TO_GS_TIMMINS", "HAP_1", "GS_TIMMINS", 45.0, hap_timmins),
        build_hap_gs_link("L_GS_TIMMINS_TO_HAP1", "GS_TIMMINS", "HAP_1", 45.0, hap_timmins),
    )
    _add_bidirectional_link(
        links,
        build_hap_gs_link("L_HAP1_TO_GS_IROQUOIS", "HAP_1", "GS_IROQUOIS", 35.0, hap_iroquois),
        build_hap_gs_link("L_GS_IROQUOIS_TO_HAP1", "GS_IROQUOIS", "HAP_1", 35.0, hap_iroquois),
    )

    sat_hap = {0: 600.0, 1: 650.0, 2: 400.0, 3: 0.0}
    _add_bidirectional_link(
        links,
        build_sat_hap_placeholder_link("L_SAT1_TO_HAP1", "SAT_1", "HAP_1", 550.0, sat_hap),
        build_sat_hap_placeholder_link("L_HAP1_TO_SAT1", "HAP_1", "SAT_1", 550.0, sat_hap),
    )

    key_pools = build_key_pools_for_links(
        links=links,
        time_slots=time_slots,
        capacity=1e9,
        initial_keys=0.0,
    )

    demands = {
        "D_TIMMINS_IROQUOIS": Demand(
            demand_id="D_TIMMINS_IROQUOIS",
            source_gs="GS_TIMMINS",
            target_gs="GS_IROQUOIS",
            requested_keys_by_time={0: 500.0, 1: 600.0, 2: 700.0, 3: 600.0},
            metadata={
                "source_repository": HAP_QKD_REPO,
                "demand_style": "HAP-QKD demand(K_REQ, n1, n2)",
            },
        )
    }

    scenario = Scenario(
        scenario_id="source_mapped_multilayer_qkd",
        nodes=nodes,
        links=links,
        demands=demands,
        key_pools=key_pools,
        time_slots=time_slots,
        parameters={
            "time_slot_duration_minutes": 30,
            "source_repositories": {
                "satellite_gs": SATELLITE_QKD_REPO,
                "hap_gs": HAP_QKD_REPO,
                "satellite_hap": "placeholder",
            },
            "satellite_hap_status": "SAT-HAP topology is present; capacity is placeholder/manual.",
        },
    )
    scenario.validate()
    return scenario


if __name__ == "__main__":
    scenario = build_scenario()
    print(f"Scenario: {scenario.scenario_id}")
    print(f"Nodes: {list(scenario.nodes)}")
    print(f"Links: {list(scenario.links)}")
    print(f"Demands: {list(scenario.demands)}")
