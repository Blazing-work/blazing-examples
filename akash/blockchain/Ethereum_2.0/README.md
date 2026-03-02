# Ethereum 2.0 Node Deployment

> If you don't have validator keys, see [how to create them](/Ethereum_2.0/create_validator_key_en(Linux).md).

## Environment Variables

| Variable | Description |
|:--------:|:-----------:|
| `DEPOSIT_JSON_BASE64` | Base64-encrypted **deposit_data_xxxxxxx.json** ([generation instructions](/Ethereum_2.0/create_validator_key_en(Linux).md#encrypt-json-files)) |
| `DEPOSIT_FILE_NAME` | Full deposit_data filename with .json extension, e.g. `deposit_data-1679338505.json` |
| `KEYSTORE_JSON_BASE64` | Base64-encrypted **keystore_xxxxx.json** ([generation instructions](/Ethereum_2.0/create_validator_key_en(Linux).md#encrypt-json-files)) |
| `KEYSTORE_FILE_NAME` | Full keystore filename with .json extension, e.g. `keystore-m_12381_3600_0_0_0-1679338504.json` |
| `ACCOUNT_ETH_PASS` | Password for the validator keys ([step 8](/Ethereum_2.0/create_validator_key_en(Linux).md)) |
| `RECEPIENT` | Recipient address for staking rewards |
| `SNAP_URL` | State sync checkpoint URL, e.g. `https://prater-checkpoint-sync.stakely.io` for Goerli |

## Resources

Choose resources based on your requirements:

- With `state sync` on the Goerli network: ~**300 GB** disk
- Full archive of Ethereum mainnet: up to **1.5 TB** disk

Use `state sync` if your application does not need historical network data.

```yaml
resources:
  cpu:
    units: 4.0
  memory:
    size: 9Gi
  storage:
    - size: 300Gi
```
