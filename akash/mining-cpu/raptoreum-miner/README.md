## How to mine Raptoreum (RTM)


![AkashMiningRTM](https://user-images.githubusercontent.com/19512127/142097004-8c662e9a-e52a-4c36-a4dd-28b9b2bc3795.png)


# Deploying


```
---
version: "2.0"

services:
  raptoreum:
    image: cryptoandcoffee/cpu-akash-cpuminer-gr-avx2:2
    expose:
      - port: 4048
        as: 80
        proto: tcp
        to:
          - global: true
    env:
      - "ADDRESS=RMB251ZucvCNyX1yoQqsSC2wwJ3s7fHx3b"
      - "POOL=suprnova" #You can enter custom pool here, otherwise suprnova nearest location will be used
      - "WORKER=akash"
      - "TUNE=no-tune"
      - "DONATION=0"
profiles:
  compute:
    raptoreum:
      resources:
        cpu:
          units: 1.0
        memory:
          size: 256Mi
        storage:
          size: 128Mi
  placement:
    akash:
      pricing:
        raptoreum:
          amount: 2

deployment:
  raptoreum:
    akash:
      profile: raptoreum
      count: 1
```

# Choosing a provider

Blazing Core is a marketplace of compute.  Providers set their own prices for compute resources.  We recommend you try different providers and check your logs after deployment to determine the hashrate.


## Change the tuning option


No tune will start mining right away - with no performance tuning of the container.  Without this expect a lower hashrate.
Be warned, tuning can take at least 3 hours before mining begins - so do not expect to see hashrate on the pool immediately.


## Increase the deployment size

You can deploy more CPU or more replicas to mine faster.


```
cpu:
  units: 1.0 # Max cpu units is 10

```

Or increase the replica count from `count: 1` to `count: 2`.

```
deployment:
  raptoreum:
    akash:
      profile: raptoreum
      count: 1 # Multiplier for cpu:units
```

# Check your profitability

After your deployment has finished tuning or is displaying results on the pool you can check your profitability by inputing your hashrate from the log file.

[Minerstat profitability calculator](https://minerstat.com/coin/RTM)

# What is the best pool? Where do I solo mine?

We recommend you check MiningPoolStats for the most up-to-date list of mining pools.

[Mining Pool Stats](https://miningpoolstats.stream/raptoreum)
