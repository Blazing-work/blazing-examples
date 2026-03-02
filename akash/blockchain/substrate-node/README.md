# Substrate Node


A fresh FRAME-based Substrate node, ready for hacking rocket :rocket:

## Docker images

* [ubinix5warun/substrate-node:v3-dev](https://hub.docker.com/layers/166944139/ubinix5warun/substrate-node/v3-dev/images/sha256-a2561b52172e902d4d63b265ba3379b53b633fc1b4289e3ed15ad35aa1146fde?context=repo)
    * [Dockerfile](https://github.com/ubinix-warun/substrate-node-template/blob/gr11-hackathon/container/Dockerfile)
    * [Build images](https://github.com/ubinix-warun/substrate-node-template/blob/gr11-hackathon/build-image.sh)

## Connect to WebSocket

Found host and externalPort from akask, use socat to proxy.

```

...
"forwarded_ports": {
    "web": [
      {
        "port": 9944,
        "externalPort": 30190,
      ....
}
```

```
```
