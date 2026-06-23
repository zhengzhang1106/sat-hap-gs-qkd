from __future__ import annotations

from drl.environment import DRLAction, DRLState


class BaseAgent:
    """Base interface for future DRL link-activation agents."""

    def select_action(self, state: DRLState) -> DRLAction:
        raise NotImplementedError("Agent action selection is not implemented in phase 1.")

