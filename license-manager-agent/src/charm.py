#!/usr/bin/env python3
"""This module provides the implementation for License Manager Agent Charm."""

from ops import main
from ops.charm import CharmBase

from charms.vantage_agent.v0.agent_snapper import AgentSnapper

class LicenseManagerAgentCharm(CharmBase):
    """Facilitate agent life-cycle."""

    def __init__(self, *args):
        """Initialize and observe."""
        super().__init__(*args)
        self._snapper = AgentSnapper(self, "license-manager-agent")


if __name__ == "__main__":
    main(LicenseManagerAgentCharm)
