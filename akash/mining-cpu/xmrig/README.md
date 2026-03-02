# How to speed up mining?

The biggest factor to control speed of mining is using RANDOMX_MODE=fast or RANDOMX_MODE=light.

Set `RANDOMX_MODE=fast` to maximize your speed and use the most amount of resources possible / highest price.
Requires at least 3Gi of Memory for providers with = 1 NUMA node.
Requires at least 4.75Gi of Memory for providers with > 1 NUMA node.

Set `RANDOMX_MODE=light` to use the smallest amount of resources / lowest price.
Requires at least 0.1Gi of Memory for all providers.


## Configure xmrig options


Here are all available variables:
```
ALGO=
POOL=
WALLET=
WORKER=
PASS=
TLS=
TLS_FINGERPRINT=
DONATE_LEVEL=
RANDOMX_MODE=
CUSTOM_OPTIONS=
```

## Default pools

The default pool is [MoneroOcean](moneroocean.stream/).
Input your Monero wallet address in the `WALLET=` variable.

## Changing the pool

We recommend you use MoneroOcean for a reliable pool, however if you need to change it feel free using the `POOL=` and configure `WALLET=` and `PASSWORD=`.


## Startup checks

Enabling startup checks ensures that your deployment has the required CPU, memory, and configuration settings. It verifies resource availability and compatibility with the specified mining mode, optimizing performance and stability.
When startup check is set to false, mining will not be optimized as thread and core counts recognized by Xmrig will not bre precise.


## Increase the number of containers per deployment

You can deploy more CPU or more replicas to mine faster.

```
cpu:
  units: 1.0 # Max cpu units is 256
```

Or increase the replica count from `count: 1` to `count: 2`.

```
deployment:
  xmrig:
    akash:
      profile: xmrig
      count: 1 # Multiplier for cpu:units
```


### Check your miner's status

Just enter your deployment URI at http://workers.xmrig.info

### Check your miner's stats in the Hashvault pool

Enter your Monero address to see the stats at https://monero.hashvault.pro/en/dashboard

# Check your profitability

After your deployment has finished tuning or is displaying results on the pool you can check your profitability by inputing your hashrate from the log file.

[Minerstat profitability calculator](https://minerstat.com/coin/XMR)

# What is the best pool? Where do I solo mine?

We recommend you check MiningPoolStats for the most up-to-date list of mining pools.

[Mining Pool Stats](https://miningpoolstats.stream/monero)

# Additional guides

[How to mine Monero ](https://nixaid.com/mine-monero-Blazing Core)
