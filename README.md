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

**Vantage Agent Charms** are a collection of Juju charms that enable seamless integration of Slurm clusters with the Vantage platform. Each charm manages the deployment and lifecycle of its corresponding agent snap, providing automation and operational consistency for HPC environments.

### Supported Charms

- [vantage-agent](vantage-agent/README.md): Core agent for Vantage integration.
- [jobbergate-agent](jobbergate-agent/README.md): Manages job submission and orchestration.
- [license-manager-agent](license-manager-agent/README.md): Handles license management for cluster workloads.

> For detailed usage and configuration, see the README in each sub-project.

---

## Getting Started

### Prerequisites

Install the required tools:

```bash
sudo snap install charmcraft --channel=latest/stable --classic
sudo snap install juju --channel=3/stable --classic
sudo snap install just --classic
sudo snap install astral-uv --classic
sudo snap install lxd --channel=latest/stable --classic
```

### Building the Charms

To build all charms in the repository, run:

```bash
just repo build
```

After a successful build, the compiled charms will be available in the `_build/` directory:

```bash
ls -la _build/
```

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
