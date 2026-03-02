# Sentinel dVPN Node

| [Sentinel](https://sentinel.co/) | [Discord](https://discord.gg/HPW52yQuQJ) | [Telegram](https://t.me/SentinelNodeNetwork) |
|:--:|:--:|:--:|

## About

Sentinel dVPN allows users to deploy decentralized VPN servers worldwide. Node owners earn DVPN tokens for every gigabyte of traffic routed through their node. Users choose nodes based on speed, geographic location, and price.

This guide covers deploying the server-side Sentinel dVPN node.

## Preparation

1. Create a separate `Keplr` account for the dVPN node
2. Encode the mnemonic phrase using Base64 (use [Notepad++](https://notepad-plus-plus.org/downloads/) or a secure online encoder)
3. Fund the account with at least `1500 DVPN` for gas fees (available on OSMOSIS or KUCOIN)

## Deployment

Replace `your_endpoint_name` in the `endpoints` and `expose` sections with a unique name (**lowercase Latin characters only**).

### Required Variables

| Variable | Description |
|----------|-------------|
| `MNEMONIC_BASE64` | Base64-encoded mnemonic from your Sentinel account |
| `MONIKER` | Unique name for your node |
| `IPV4_ADDRESS` | Leave blank initially; fill in after provider assigns an IP |

> If you change `LISTEN_PORT` or `REMOTE_PORT`, update the corresponding `EXPOSE` section entries as well.

Variables must be inside quotes, e.g.: `"MONIKER=dVPN v2RAY"`

## Post-Deployment

1. Deploy with an empty `IPV4_ADDRESS`
2. After the provider assigns an IPv4 address (visible in the **LEASES** tab), update your deployment with the assigned IP
3. Deployment takes about 2 minutes before the node starts working
4. Verify by checking your Sentinel address in [Mintscan Explorer](https://www.mintscan.io/sentinel) for status update transactions

For advanced configuration options, see the [variables reference](/Sentinel-dVPN-node/VARIABLES.md).
