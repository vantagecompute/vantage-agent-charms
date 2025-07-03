<a href="https://www.vantagecompute.ai/">
  <img src="https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-black-horz.png" alt="Vantage Compute Logo" width="100" style="margin-bottom: 0.5em;"/>
</a>

<div align="center">

# Vantage Agent Charms


![Build Status](https://img.shields.io/github/actions/workflow/status/vantagecompute/vantage-agent-charms/test.yaml?branch=main&label=build&logo=github&style=plastic)
![GitHub Issues](https://img.shields.io/github/issues/vantagecompute/vantage-agent-charms?label=issues&logo=github&style=plastic)
![Pull Requests](https://img.shields.io/github/issues-pr/vantagecompute/vantage-agent-charms?label=pull-requests&logo=github&style=plastic)
![GitHub Contributors](https://img.shields.io/github/contributors/vantagecompute/vantage-agent-charms?logo=github&style=plastic)


</div>


## Overview

**Vantage Agent Charms** are a collection of Juju charms that enable seamless integration of Slurm clusters with the [Vantage](https://vantagecompute.ai) platform. Each charm manages the deployment and lifecycle of its corresponding agent snap, providing automation and operational consistency for HPC environments.

### Included Charms

- [vantage-agent](charms/vantage-agent/README.md): Core agent for Vantage integration.
- [jobbergate-agent](charms/jobbergate-agent/README.md): Manages job submission and orchestration.
- [license-manager-agent](charms/license-manager-agent/README.md): Handles license management for cluster workloads.

> For detailed usage and configuration, see the README in each sub-project.

---

## Getting Started

### Build
This project uses [`uv`](https://docs.astral.sh/uv/) in combination with [`just`](https://github.com/casey/just)
to drive [`charmcraft`](https://canonical-charmcraft.readthedocs-hosted.com/en/stable/) to build the [charms](https://juju.is/charms-architecture) in [`lxd`](https://canonical.com/lxd) containers.

Install the dependencies.

```bash
sudo snap install charmcraft --channel=latest/stable --classic
sudo snap install juju --channel=3/stable --classic
sudo snap install just --classic
sudo snap install astral-uv --classic
sudo snap install lxd --channel=latest/stable --classic
```
Once you have `charmcraft`, `lxd`, `just`, and `uv` installed you are ready to build.

Build the charms in this repository:

```bash
just repo build
```

After a successful build, the compiled charms will be available in the `_build/` directory:

```bash
ls -la _build/
```

### Deploy Slurm
[Bootstrap](https://documentation.ubuntu.com/juju/3.6/reference/juju-cli/list-of-juju-cli-commands/bootstrap/) a [juju controller](https://documentation.ubuntu.com/juju/3.6/reference/controller/) and
[add a model](https://documentation.ubuntu.com/juju/3.6/reference/model/).

#### Deploy Slurm
Use juju to deploy a slurm cluster.

```bash
juju add-model slurm

juju deploy mysql --channel 8.0/stable
juju deploy slurmdbd --channel edge
juju deploy slurmctld --channel edge
juju deploy slurmd --channel edge
juju deploy sackd slurm-util --channel edge

juju integrate slurmdbd mysql
juju integrate slurmdbd slurmctld
juju integrate slurmd slurmctld
juju integrate slurm-util slurmctld
```
> **Note:** For more information on deploying and managing Slurm with Juju, see the [slurm-charms upstream documentation](https://canonical-charmed-hpc.readthedocs-hosted.com/latest/).

### Deploy Vantage Agents
Visit the desired cluster in the [Vantage UI](https://vantagecompute.ai) to obtain the oidc configuration needed by each of the agents. 
Once you have your cluster oidc configuration, [deploy](https://documentation.ubuntu.com/juju/3.6/reference/juju-cli/list-of-juju-cli-commands/deploy/)
and [integrate](https://documentation.ubuntu.com/juju/3.6/reference/juju-cli/list-of-juju-cli-commands/integrate/) the vantage-agents we just built (in the `_build/` dir).

```bash
OIDC_CLIENT_SECRET=<oidc_client_secret>
OIDC_CLIENT_ID=<oidc_client_id>
SLURM_CLUSTER_NAME=<slurm_cluster_name>

juju deploy ./_build/license-manager-agent.charm \
    --config license-manager-agent-oidc-client-id=$OIDC_CLIENT_ID \
    --config license-manager-agent-oidc-client-secret=$OIDC_CLIENT_SECRET

juju deploy ./_build/jobbergate-agent.charm \
    --config jobbergate-agent-oidc-client-id=$OIDC_CLIENT_ID \
    --config jobbergate-agent-oidc-client-secret=$OIDC_CLIENT_SECRET

juju deploy ./_build/vantage-agent.charm \
    --config vantage-agent-oidc-client-id=$OIDC_CLIENT_ID \
    --config vantage-agent-oidc-client-secret=$OIDC_CLIENT_SECRET \
    --config vantage-agent-cluster-name=$SLURM_CLUSTER_NAME

for charm in license-manager-agent jobbergate-agent vantage-agent; do
    juju integrate slurm-util $charm;
done
```
Following these steps, your cluster will be ready for use with the Vantage platform.

---

## Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes, improvements, or new features.

---

## License

Distributed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

For questions or support, email us at [info@vantagecompute.ai](mailto:info@vantagecompute.ai).

---

© 2025 Vantage Compute Corporation. All rights reserved.
