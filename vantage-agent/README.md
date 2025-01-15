# Vantage Agent Charm

## Usage

Follow the steps below to get started.


### Build the charm

Running the following command will produce a .charm file, `vantage-agent.charm`

```bash
charmcraft build
```


### Create the vantage-agent charm config

Create a new config file named `vantage-agent.yaml`. It should be structured like this:

```yaml
vantage-agent:
  snap-config: |
    oidc-domain=<oidc-domain>
    oidc-client-id=<oidc-client-id>
    oidc-client-secret=<oidc-client-secret>
    cluster-name=<custer-name>
```

A fully populated config script might look like:

```yaml
vantage-agent:
  snap-config: |
    base-api-url=https://apis.vantagehpc.io
    oidc-domain=auth.vantagehpc.io/realms/vantage
    oidc-client-id=ae4e7c40-7889-45ae-bd36-1ad2f25dc679
    oidc-client-secret=LMmPxusATyKz_dp63hjeJO7cFUayiYvudGv4r3gUk_4
```
For a complete listing of the configuration options, see
[vantage-agent](https://snapcraft.io/vantage-agent) on the Snap Store.


### Deploy the charm

Using the built charm and the defined config file, run this command to deploy the charm:

```bash
juju deploy ./vantage-agent.charm \
    --config ./vantage-agent.yaml
```

Note: the `./` is needed before the charm filename.

Next, relate the vantage-agent app to the slurmctld app in juju:

```bash
juju integrate vantage-agent slurmctld
```


## License

Distributed under the MIT License. See `LICENSE` for more information.
