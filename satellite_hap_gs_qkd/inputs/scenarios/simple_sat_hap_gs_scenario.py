from __future__ import annotations

from common.key_pool import KeyPool
from common.network_demand import Demand
from common.network_node import Node
from common.network_scenario import Scenario
from common.network_types import LinkType, NodeType
from common.quantum_link import Link


def build_scenario() -> Scenario:
    time_slots = [0, 1, 2]

    nodes = {
        "GS_A": Node(
            node_id="GS_A",
            node_type=NodeType.GS,
            position=(0.0, 0.0, 0.0),
            rx_tx_limit=2,
            storage_capacity=5000.0,
        ),
        "GS_B": Node(
            node_id="GS_B",
            node_type=NodeType.GS,
            position=(100.0, 0.0, 0.0),
            rx_tx_limit=2,
            storage_capacity=5000.0,
        ),
        "SAT_1": Node(
            node_id="SAT_1",
            node_type=NodeType.SAT,
            position=(50.0, 0.0, 567.0),
            rx_tx_limit=1,
            storage_capacity=3000.0,
            metadata={"orbit": "placeholder"},
        ),
        "HAP_1": Node(
            node_id="HAP_1",
            node_type=NodeType.HAP,
            position=(70.0, 0.0, 20.0),
            rx_tx_limit=1,
            storage_capacity=3000.0,
            metadata={"trajectory": "placeholder"},
        ),
    }

    links = {
        "L_SAT1_GSA": Link(
            link_id="L_SAT1_GSA",
            source="SAT_1",
            target="GS_A",
            link_type=LinkType.SAT_GS,
            distance_km=570.0,
            capacity_by_time={0: 1000.0, 1: 800.0, 2: 0.0},
            availability_by_time={0: True, 1: True, 2: False},
        ),
        "L_SAT1_HAP1": Link(
            link_id="L_SAT1_HAP1",
            source="SAT_1",
            target="HAP_1",
            link_type=LinkType.SAT_HAP,
            distance_km=550.0,
            capacity_by_time={0: 900.0, 1: 900.0, 2: 500.0},
            availability_by_time={0: True, 1: True, 2: True},
        ),
        "L_HAP1_GSB": Link(
            link_id="L_HAP1_GSB",
            source="HAP_1",
            target="GS_B",
            link_type=LinkType.HAP_GS,
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
