"""
# Agent Snapper Library

This library provides the `AgentSnapper` class that provides all the event handling
and operations logic needed to run a Snapped Vantage Agent within a charm. This
allows the Charm for a Snapped Vantage Agent to be very minimalist and avoid
repeating a lot of boilerplate code.
"""

# The unique Charmhub library identifier, never change it
LIBID = "155db2f7cb1f43f2bfbac3be9c9289ab"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 2

import logging
import shlex
import subprocess
from pathlib import Path
from typing import Any

from ops import ConfigChangedEvent, InstallEvent, RemoveEvent, StartEvent, StopEvent, Object
from ops.charm import CharmBase
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus, WaitingStatus

logger = logging.getLogger()


class AgentSnapper(Object):

    def __init__(self, charm: CharmBase, snap_name: str):
        super().__init__(charm, None)

        self._charm = charm
        self._snap_path = Path("/usr/bin/snap")
        self._snap_name = snap_name

        event_handler_bindings = {
            self._charm.on.install: self.handle_install,
            self._charm.on.config_changed: self.handle_config_changed,
            self._charm.on.stop: self.handle_stop,
            self._charm.on.start: self.handle_start,
            self._charm.on.remove: self.handle_remove,
        }
        for event, handler in event_handler_bindings.items():
            self._charm.framework.observe(event, handler)

    ## Event Handlers
    def handle_install(self, event: InstallEvent):
        logger.debug(f"## Processing install event for {self._snap_name}.")
        self._charm.unit.status = WaitingStatus(f"Installing snap for {self._snap_name}")
        try:
            self.install_snap()
        except Exception as e:
            logger.error(f"## Error installing {self._snap_name}: {e}")
            self._charm.unit.status = BlockedStatus("Error installing the snap for {self._snap_name}")
            event.defer()
            return

        logger.debug(f"Snap for {self._snap_name} installed")

    def handle_config_changed(self, event: ConfigChangedEvent):
        logger.debug(f"## Processing config changed event for {self._snap_name}.")
        if not self.is_snap_installed():
            logger.debug(f"## Snap for {self._snap_name} not installed, deferring event")
            event.defer()
            return

        logger.info(f"## Updating config for {self._snap_name}")
        self.configure_snap()

        if self.is_snap_active():
            self.run_snap_service("restart")

    def handle_start(self, event: StopEvent):
        logger.debug(f"## Processing start event for {self._snap_name}.")
        self.run_snap_service("start")
        self._charm.unit.status = ActiveStatus()

    def handle_stop(self, event: StopEvent):
        logger.debug(f"## Processing stop event for {self._snap_name}.")
        self.run_snap_service("stop")
        self._charm.unit.status = MaintenanceStatus()

    def handle_remove(self, event: RemoveEvent):
        logger.debug(f"## Processing remove event for {self._snap_name}.")
        self.remove_snap()

    ## Operations
    def is_snap_installed(self) -> bool:
        cmd = [
            self._snap_path,
            "list",
            self._snap_name,
        ]

        try:
            subprocess.check_output(cmd)
            return True
        except subprocess.CalledProcessError:
            return False

    def is_snap_active(self) -> bool:
        logger.debug(f"### Checking active status for {self._snap_name}.daemon")
        cmd = [
            self._snap_path,
            "services",
            f"{self._snap_name}.daemon",
        ]

        try:
            status_output = subprocess.check_output(cmd).decode("utf-8")
            status_line = status_output.split("\n")[1]
            status = status_line.split()[2]
            return status == "active"
        except subprocess.CalledProcessError:
            return False

    def install_snap(self) -> None:
        channel = self._charm.config["snap-channel"]
        assert isinstance(channel, str)

        confinement = self._charm.config["snap-confinement"]
        assert isinstance(confinement, str)

        if not self.is_snap_installed():
            logger.debug(f"### Installing {self._snap_name}.")
            self._sys_exec(
                self._snap_path,
                "install",
                "--channel",
                channel,
                f"--{confinement}",
                self._snap_name,
            )
        else:
            logger.debug(f"### Refreshing {self._snap_name} (already installed).")
            self._sys_exec(
                self._snap_path,
                "refresh",
                "--channel",
                channel,
                f"--{confinement}",
                self._snap_name,
            )

    def configure_snap(self) -> None:
        logger.debug(f"### Configuring {self._snap_name}.")
        raw_config = self._charm.config["snap-config"]
        assert isinstance(raw_config, str)

        snap_config = {}
        for line in raw_config.splitlines():
            if line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            snap_config[key.strip()] = value.strip()

        for key, value in snap_config.items():
            self._sys_exec(
                self._snap_path,
                "set",
                self._snap_name,
                f"{key}={value}",
            )

    def remove_snap(self) -> None:
        logger.debug(f"### Removing {self._snap_name}.")
        self._sys_exec(
            self._snap_path,
            "remove",
            self._snap_name,
        )

    def run_snap_service(self, service: str) -> None:
        logger.debug(f"### Running {self._snap_name}.{service}")
        self._sys_exec(
            self._snap_path,
            "run",
            f"{self._snap_name}.{service}",
        )

    @staticmethod
    def _sys_exec(*cmd: Any) -> None:
        try:
            subprocess.call([str(p) for p in cmd])
        except subprocess.CalledProcessError as exc:
            logger.error(f"Error executing command {shlex.join(cmd)} - {exc}")
            raise exc
