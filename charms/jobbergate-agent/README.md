
<a href="https://www.vantagecompute.ai/">
  <img src="https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-black-horz.png" alt="Vantage Compute Logo" width="100" style="margin-bottom: 0.5em;"/>
</a>

# Jobbergate Agent Charm
[![Charmhub Latest Release Badge](https://charmhub.io/jobbergate-agent/badge.svg)](https://charmhub.io/jobbergate-agent)

## Overview

The [**Jobbergate Agent**](https://github.com/omnivector-solutions/jobbergate) is the agent component for Vantage's job orchestration middleware. It manages job submission and orchestration for Slurm clusters integrated with the Vantage platform. For more information, visit our upstream [Documentation](https://docs.vantagecompute.ai).

---

## Getting Started Example
To use the jobbergate-agent, you must first have a Slurm cluster. The following example uses Juju and LXD containers.

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
> **Note:** For more information on deploying and managing Slurm with Juju, see the [Charmed HPC Documentation](https://canonical-charmed-hpc.readthedocs-hosted.com/latest/).


### Deploy and Integrate the Jobbergate Agent Charm
Visit the [Clusters](https://app.vantagecompute.ai/compute/clusters) dashboard in Vantage to obtain the cluster OIDC configuration.
Supply the cluster OIDC configuration to juju and deploy the jobbergate-agent.
```bash
juju deploy jobbergate-agent \
    --config jobbergate-agent-oidc-client-id=<OIDC_CLIENT_ID> \
    --config jobbergate-agent-oidc-client-secret=<OIDC_CLIENT_SECRET>
```

Integrate the `jobbergate-agent` with `slurm-util` to install the snap, apply configuration, and connect to the Vantage platform:
```bash
juju integrate jobbergate-agent slurm-util
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
