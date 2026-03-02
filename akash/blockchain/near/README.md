# What is NEAR?

NEAR is a [sharded](https://near.org/downloads/Nightshade.pdf), [proof-of-stake](https://en.wikipedia.org/wiki/Proof_of_stake), [layer-one](https://blockchain-comparison.com/blockchain-protocols/) blockchain that is simple to use, secure and scalable.


# Simple Steps

4. Deploy a NEAR node


# Deploy a NEAR node

2. create a certificate
3. create deployment

> Note:
>
> - adjusting the `account-id` if you want to run a validator node.


```
---
version: "2.0"

services:
  nearup:
    image: nearprotocol/nearup
    args:
      - run
      # Validators should use the account ID of the account you want to stake with. leave empty if not going to be a validator
      - --account-id=
      # Types of network: mainnet, testnet, betanet, guildnet, localnet
      - mainnet
    expose:
      - port: 3030
        as: 3030
        to:
          - global: true

profiles:
  compute:
    nearup:
      resources:
        # Near Nodes Minimal Hardware Specifications: 8 physical cores AND 8GB DDR4 RAM
        cpu:
          # Max cpu units is 10 on Blazing Core
          units: 8
        memory:
          size: 8Gi
        storage:
          size: 256Gi
  placement:
    akash:
      attributes:
        host: akash
      signedBy:
        anyOf:
      pricing:
        nearup:
          amount: 100

deployment:
  nearup:
    akash:
      profile: nearup
      count: 1
```
