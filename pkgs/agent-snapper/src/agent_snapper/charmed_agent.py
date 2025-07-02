"""Agent Snapper Library.

This library provides the `AgentSnapper` class that encapsulates all event handling and operational logic required
to manage a Snapped Vantage Agent within a Juju charm. By using this library, charm authors can avoid boilerplate
charm code and focus on custom logic.
"""

import json
import logging
import shlex
import subprocess
from pathlib import Path
from typing import Any, List, Optional, Union

import ops

logger = logging.getLogger()


class AgentSnapperError(Exception):
    """Exception raised by the AgentSnapper."""

    pass


class SnapperSysCallError(Exception):
    """Raise exception from syscall execution."""

    pass


class AgentSnapper(ops.Object):
    """Vantage Snapped Agent Charm Operator."""

    _SNAP_REQUIRED_CONFIGS = [
        "base-api-url",
        "oidc-domain",
        "oidc-client-id",
        "oidc-client-secret",
    ]

    def __init__(
        self,
        charm: ops.CharmBase,
        snap_name: str,
        required_snap_config: Optional[List[str]] = None,
    ):
        """Initialize the AgentSnapper.

        Args:
            charm: The parent CharmBase instance.
            snap_name: The name of the snap to manage.
            required_snap_config: Additional required snap config keys (optional).
        """
        super().__init__(charm, None)
        self._charm = charm
        self._snap_path = Path("/usr/bin/snap")
        self._snap_name = snap_name
        self._required_snap_config = required_snap_config or []

        # Register event handlers
        for event, handler in [
            (self._charm.on.install, self._on_install),
            (self._charm.on.config_changed, self._on_config_changed),
            (self._charm.on.update_status, self._on_update_status),
            (self._charm.on.stop, self._on_stop),
            (self._charm.on.remove, self._on_remove),
        ]:
            self._charm.framework.observe(event, handler)

    @property
    def _required_snap_configs(self) -> List[str]:
        """Return the required snap config keys (default + user-specified)."""
        return self._SNAP_REQUIRED_CONFIGS + self._required_snap_config

    ## Event Handlers
    def _on_install(self, event: ops.InstallEvent) -> None:
        """Perform install operations for the snap."""
        logger.debug(f"## Processing install event for {self._snap_name}.")
        self._charm.unit.status = ops.WaitingStatus(f"Installing snap for {self._snap_name}")
        try:
            self.install_snap()
        except Exception as e:
            logger.error(f"## Error installing {self._snap_name}: {e}")
            self._charm.unit.status = ops.BlockedStatus(
                f"Error installing the snap for {self._snap_name}"
            )
            event.defer()
            return
        logger.debug(f"Snap for {self._snap_name} installed")

    def _on_config_changed(self, event: ops.ConfigChangedEvent) -> None:
        """Perform config-changed operations for the snap."""
        logger.debug(f"## Processing config changed event for {self._snap_name}.")
        if not self._is_snap_installed:
            logger.debug(f"## Snap for {self._snap_name} not installed, deferring event")
            event.defer()
            return

        prefix = f"{self._snap_name}-"
        snap_configs = {
            key.removeprefix(prefix): value
            for key, value in self._charm.config.items()
            if key.startswith(prefix)
        }
        logger.info(f"Snap configs: {snap_configs}")

        missing = [k for k in self._required_snap_configs if not snap_configs.get(k)]
        if not missing:
            self.run_snap_service("stop")
            for k, v in snap_configs.items():
                self._sys_exec(self._snap_path, "set", self._snap_name, f"{k}={v}")

            if self.model.unit.is_leader():
                self.run_snap_service("start")

            self._on_update_status(event)
            return

        missing_configs = [f"{prefix}{k}" for k in missing]
        self._charm.unit.status = ops.BlockedStatus(
            f"Cannot start {self._snap_name}. Missing Config: {', '.join(missing_configs)}"
        )

    def _on_stop(self, event: ops.StopEvent):
        """Perform stop operations."""
        logger.debug(f"## Processing stop event for {self._snap_name}.")
        self._charm.unit.status = ops.MaintenanceStatus()
        self.run_snap_service("stop")

    def _on_remove(self, event: ops.RemoveEvent):
        """Perform remove operations."""
        logger.debug(f"## Processing remove event for {self._snap_name}.")
        self.remove_snap()

    def _on_update_status(
        self, event: Union[ops.ConfigChangedEvent, ops.UpdateStatusEvent, ops.InstallEvent]
    ) -> None:
        """Update the charm status based on snap state."""
        if self.model.unit.is_leader():
            if self._is_snap_active:
                self._charm.unit.status = ops.ActiveStatus()
            else:
                self._charm.unit.status = ops.BlockedStatus("Cannot start snap.")
        else:
            self._charm.unit.status = ops.ActiveStatus(f"{self._snap_name} status: standby")

    ## Operations
    @property
    def _is_snap_installed(self) -> bool:
        """Return True if the snap is installed, else False."""
        logger.debug(f"### Checking if snap {self._snap_name} is installed")
        try:
            self._sys_exec(
                self._snap_path,
                "list",
                self._snap_name,
            )
            return True
        except SnapperSysCallError:
            return False

    @property
    def _is_snap_active(self) -> bool:
        """Return True if the snap service is active, else False."""
        logger.debug(f"### Checking active status for {self._snap_name}.daemon")
        try:
            status_output = self._sys_exec(
                self._snap_path,
                "services",
                f"{self._snap_name}.daemon",
            )
        except SnapperSysCallError:
            return False

        # Parse the output for the service status
        for line in status_output.splitlines():
            if line.startswith(f"{self._snap_name}.daemon"):
                parts = line.split()
                if len(parts) >= 4 and parts[2] == "active":
                    return True
        return False

    def install_snap(self) -> None:
        """Install or refresh the snap."""
        channel = self._charm.config["snap-channel"]
        if not self._is_snap_installed:
            logger.debug(f"### Installing {self._snap_name}.")
            self._sys_exec(
                self._snap_path,
                "install",
                "--channel",
                channel,
                "--classic",
                self._snap_name,
            )
        else:
            logger.debug(f"### Refreshing {self._snap_name} (already installed).")
            self._sys_exec(
                self._snap_path,
                "refresh",
                "--channel",
                channel,
                "--classic",
                self._snap_name,
            )

    def get_snap_config(self) -> dict:
        """Get the current snap configuration as a dictionary."""
        logger.debug(f"#### Fetching current config for {self._snap_name}.")
        try:
            config_output = self._sys_exec(
                self._snap_path,
                "get",
                "-d",
                self._snap_name,
            )
        except SnapperSysCallError:
            return {}
        try:
            snap_config = json.loads(config_output)
        except json.JSONDecodeError:
            logger.error("#### Error decoding snap config")
            return {}
        return snap_config

    def remove_snap(self) -> None:
        """Remove the snap from the system."""
        logger.debug(f"### Removing {self._snap_name}.")
        self._sys_exec(
            self._snap_path,
            "remove",
            self._snap_name,
        )

    def run_snap_service(self, service: str) -> None:
        """Run a snap service (e.g., start/stop daemon)."""
        logger.debug(f"### Running {self._snap_name}.{service}")
        try:
            self._sys_exec(
                self._snap_path,
                "run",
                f"{self._snap_name}.{service}",
            )
        except SnapperSysCallError as e:
            logger.error(f"Error running {self._snap_name}.{service}: {e}")

    @staticmethod
    def _sys_exec(*cmd: Any) -> str:
        """Execute a system command and return its output.

        Raises SnapperSysCallError on failure.
        """
        str_cmd = [str(p) for p in cmd]
        logger.debug(f"-----> Running command in subprocess: {shlex.join(str_cmd)}")
        try:
            result = subprocess.run(str_cmd, capture_output=True, check=False)
        except Exception as exc:
            message = f"{shlex.join(str_cmd)} - {exc}"
            logger.error(f"Invalid system command: {message}")
            raise SnapperSysCallError(f"System command failed: {message}")

        if result.returncode != 0:
            err = result.stderr.decode("utf-8")
            message = f"{shlex.join(str_cmd)} - {err}"
            logger.error(f"Error executing command: {message}")
            raise SnapperSysCallError(f"System command failed: {message}")

        out = result.stdout.decode("utf-8")
        logger.debug(f"-----> Command succeeded: {out.strip()}")
        return out
