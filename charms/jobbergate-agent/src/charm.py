#!/usr/bin/env python3
"""This module provides the implementation for Jobbergate Agent Charm."""

from agent_snapper import AgentSnapper
from ops import main
from ops.charm import CharmBase


class JobbergateAgentCharm(CharmBase):
    """Facilitate agent life-cycle."""

    def __init__(self, *args):
        """Initialize and observe."""
        super().__init__(*args)
        self._snapper = AgentSnapper(self, "jobbergate-agent")


if __name__ == "__main__":
    main(JobbergateAgentCharm)
