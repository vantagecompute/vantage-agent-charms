
<a href="https://www.vantagecompute.ai/">
  <img src="https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-black-horz.png" alt="Vantage Compute Logo" width="100" style="margin-bottom: 0.5em;"/>
</a>

# Vantage Agent Charm
[![Charmhub Latest Release Badge](https://charmhub.io/vantage-agent/badge.svg)](https://charmhub.io/vantage-agent)
## Overview

The [**Vantage Agent**](https://github.com/vantagecompute/vantage-agent) is the core agent for integrating Slurm clusters with the Vantage platform. It manages authentication, cluster registration, and communication with Vantage services. For more information, see the upstream [Documentation](https://docs.vantagecompute.ai).

---

## Getting Started Example
To use the vantage-agent, you must first have a Slurm cluster. The following example uses Juju and LXD containers.

### Install the Prerequisites
```bash
sudo snap install juju --channel=3/stable --classic
sudo snap install lxd --channel=latest/stable --classic
```

### Bootstrap Juju
```bash
juju bootstrap localhost
```

### Deploy Slurm
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


### Deploy and Integrate the Vantage Agent Charm
Visit the [Clusters](https://app.vantagecompute.ai/compute/clusters) dashboard in Vantage to obtain the cluster OIDC configuration.
Supply the cluster OIDC configuration to juju and deploy the vantage-agent.
```bash
juju deploy vantage-agent \
    --config vantage-agent-oidc-client-id=<OIDC_CLIENT_ID> \
    --config vantage-agent-oidc-client-secret=<OIDC_CLIENT_SECRET> \
    --config vantage-agent-cluster-name=<SLURM_CLUSTER_NAME>
```

Integrate the `vantage-agent` with `slurm-util` to install the snap, apply configuration, and connect to the Vantage platform:
```bash
juju integrate vantage-agent slurm-util
```

---

## Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes, improvements, or new features.

---

## License

Distributed under the MIT License. See the [LICENSE](../../LICENSE) file for details.

## Contact

For questions or support, email us at [info@vantagecompute.ai](mailto:info@vantagecompute.ai).

---

© 2025 Vantage Compute Corporation. All rights reserved.
