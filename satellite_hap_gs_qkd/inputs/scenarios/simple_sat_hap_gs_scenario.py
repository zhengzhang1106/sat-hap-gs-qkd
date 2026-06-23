from __future__ import annotations

from entities.links.inter_layer_link import InterLayerLink
from entities.links.platform_ground_link import PlatformGroundLink
from entities.links.satellite_ground_link import SatelliteGroundLink
from entities.nodes.air_platform import HighAltitudePlatform
from entities.nodes.ground_station import GroundStation
from entities.nodes.satellite import Satellite
from qkp.key_pool import KeyPool
from scenario.network_scenario import Scenario
from services.service_demand import Demand


def build_scenario() -> Scenario:
    time_slots = [0, 1, 2]

    nodes = {
        "GS_A": GroundStation(
            node_id="GS_A",
            position=(0.0, 0.0, 0.0),
            rx_tx_limit=2,
            storage_capacity=5000.0,
        ),
        "GS_B": GroundStation(
            node_id="GS_B",
            position=(100.0, 0.0, 0.0),
            rx_tx_limit=2,
            storage_capacity=5000.0,
        ),
        "SAT_1": Satellite(
            node_id="SAT_1",
            position=(50.0, 0.0, 567.0),
            rx_tx_limit=1,
            storage_capacity=3000.0,
            altitude_km=567.0,
            metadata={"orbit": "placeholder"},
        ),
        "HAP_1": HighAltitudePlatform(
            node_id="HAP_1",
            position=(70.0, 0.0, 20.0),
            rx_tx_limit=1,
            storage_capacity=3000.0,
            altitude_km=20.0,
            metadata={"trajectory": "placeholder"},
        ),
    }

    links = {
        "L_SAT1_GSA": SatelliteGroundLink(
            link_id="L_SAT1_GSA",
            source="SAT_1",
            target="GS_A",
            distance_km=570.0,
            capacity_by_time={0: 1000.0, 1: 800.0, 2: 0.0},
            availability_by_time={0: True, 1: True, 2: False},
        ),
        "L_SAT1_HAP1": InterLayerLink(
            link_id="L_SAT1_HAP1",
            source="SAT_1",
            target="HAP_1",
            distance_km=550.0,
            capacity_by_time={0: 900.0, 1: 900.0, 2: 500.0},
            availability_by_time={0: True, 1: True, 2: True},
        ),
        "L_HAP1_GSB": PlatformGroundLink(
            link_id="L_HAP1_GSB",
            source="HAP_1",
            target="GS_B",
            distance_km=75.0,
            capacity_by_time={0: 850.0, 1: 700.0, 2: 650.0},
            availability_by_time={0: True, 1: True, 2: True},
        ),
    }

    key_pools = {
        link_id: KeyPool(
            link_id=link_id,
            capacity=5000.0,
            stored_keys_by_time={0: 0.0, 1: 0.0, 2: 0.0},
        )
        for link_id in links
    }

    demands = {
        "D_GSA_GSB": Demand(
            demand_id="D_GSA_GSB",
            source_gs="GS_A",
            target_gs="GS_B",
            requested_keys_by_time={0: 500.0, 1: 500.0, 2: 500.0},
        )
    }

    scenario = Scenario(
        scenario_id="simple_sat_hap_gs",
        nodes=nodes,
        links=links,
        demands=demands,
        key_pools=key_pools,
        time_slots=time_slots,
        parameters={
            "description": "Minimal SAT-HAP-GS scenario for phase 1 framework checks.",
            "time_slot_duration_minutes": 10,
        },
    )
    scenario.validate()
    return scenario


if __name__ == "__main__":
    demo_scenario = build_scenario()
    print(f"Scenario: {demo_scenario.scenario_id}")
    print(f"Nodes: {list(demo_scenario.nodes)}")
    print(f"Links: {list(demo_scenario.links)}")
    print(f"Demands: {list(demo_scenario.demands)}")
