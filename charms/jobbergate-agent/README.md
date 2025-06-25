# Jobbergate Agent Charm

## Usage

Follow the steps below to get started.


### Build the charm

Running the following command will produce a .charm file, `jobbergate-agent.charm`

```bash
charmcraft build
```


### Create the jobbergate-agent charm config

Create a new config file named `jobbergate-agent.yaml`. It should be structured like this:

```yaml
jobbergate-agent:
  snap-config: |
    base-api-url=<base-api-url>
    oidc-domain=<oidc-domain>
    oidc-client-id=<oidc-client-id>
    oidc-client-secret=<oidc-client-secret>
```

A fully populated config script might look like:

```yaml
jobbergate-agent:
  snap-config: |
    base-api-url=https://apis.vantagehpc.io
    oidc-domain=auth.vantagehpc.io/realms/vantage
    oidc-client-id=ae4e7c40-7889-45ae-bd36-1ad2f25dc679
    oidc-client-secret=LMmPxusATyKz_dp63hjeJO7cFUayiYvudGv4r3gUk_4
```
For a complete listing of the configuration options, see
[jobbergate-agent](https://snapcraft.io/jobbergate-agent) on the Snap Store.


### Deploy the charm

Using the built charm and the defined config file, run this command to deploy the charm:

```bash
juju deploy ./jobbergate-agent.charm \
    --config ./jobbergate-agent.yaml
```

Note: the `./` is needed before the charm filename.

Next, relate the jobbergate-agent app to the slurmctld app in juju:

```bash
juju integrate jobbergate-agent slurmctld
```


## License

Distributed under the MIT License. See `LICENSE` for more information.
