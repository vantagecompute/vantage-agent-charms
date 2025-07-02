#!/usr/bin/env python3
"""This module provides the implementation for Vantage Agent Charm."""

from agent_snapper import AgentSnapper
from ops import main
from ops.charm import CharmBase


class VantageAgentCharm(CharmBase):
    """Facilitate agent life-cycle."""

    def __init__(self, *args):
        """Initialize and observe."""
        super().__init__(*args)
        self._snapper = AgentSnapper(self, "vantage-agent", ["cluster-name"])


if __name__ == "__main__":
    main(VantageAgentCharm)
