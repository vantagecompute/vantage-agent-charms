#!/usr/bin/env python3
"""This module provides the implementation for License Manager Agent Charm."""

from agent_snapper import AgentSnapper
from ops import main
from ops.charm import CharmBase


class LicenseManagerAgentCharm(CharmBase):
    """Facilitate agent life-cycle."""

    def __init__(self, *args):
        """Initialize and observe."""
        super().__init__(*args)
        self._snapper = AgentSnapper(self, "license-manager-agent")


if __name__ == "__main__":
    main(LicenseManagerAgentCharm)
