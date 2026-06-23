from __future__ import annotations

from typing import Any

from milp.milp_data import MILPInput, MILPResult


class MILPSolver:
    """
    Placeholder solver interface for the future joint MILP model.

    The first phase only fixes the contract between scenario data and the MILP
    route. Full Gurobi model construction will be added later.
    """

    def __init__(self, milp_input: MILPInput):
        self.milp_input = milp_input
        self.model: Any = None

    def build_model(self) -> Any:
        raise NotImplementedError("MILP model construction is not implemented in phase 1.")

    def solve(self) -> MILPResult:
        raise NotImplementedError("MILP solving is not implemented in phase 1.")

