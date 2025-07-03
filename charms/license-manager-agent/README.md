
<a href="https://www.vantagecompute.ai/">
  <img src="https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-black-horz.png" alt="Vantage Compute Logo" width="100" style="margin-bottom: 0.5em;"/>
</a>

# License Manager Agent Charm
[![Charmhub Latest Release Badge](https://charmhub.io/license-manager-agent/badge.svg)](https://charmhub.io/license-manager-agent)



## Overview

The [**License Manager Agent**](https://github.com/omnivector-solutions/license-manager/tree/main/lm-agent) is the agent component of Vantage's license optimization mideleware, the [License Manager](https://github.com/omnivector-solutions/license-manager). The license-manager-agent sits (abstractly) between slurm, the application workload, and the software license servers, optimizing throughput through coordinated scheduling in multi-cluster environments. For additional information on how to use the License Manager, please see our upstream [Documentation](https://docs.vantagecompute.ai)

---

## Getting Started Example
To use the license-manager-agent, you must first have a slurm cluster. We will install one using juju in lxd containers for this example.

### Install the Prerequisites
Install the required tools:
```bash
sudo snap install juju --channel=3/stable --classic
sudo snap install lxd --channel=latest/stable --classic
```
### Bootstrap Juju
```bash
juju bootstrap localhost
```


### Deploy Slurm
Use Juju to add a model and deploy the slurm charms, adding a utility node to host the license-manager-agent.

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

### Deploy and Integrate the License Manager Agent Charm
Visit the [Clusters](https://app.vantagecompute.ai/compute/clusters) dashboard in Vantage to obtain the cluster oidc configuration.
Supply the cluster oidc configuration to juju and deploy the license-managera-agent.
```bash
juju deploy license-manager-agent \
    --config license-manager-agent-oidc-client-id=<OIDC_CLIENT_ID> \
    --config license-manager-agent-oidc-client-secret=<OIDC_CLIENT_SECRET>
```

Integrate the `license-manager-agent`  with `slurm-util` to install the `license-manager-agent` snap,
apply the configuration, and connect the agent to the [Vantage](https://vantagecompute.ai) platform.

```bash
juju integrate license-manager-agent slurm-util
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
