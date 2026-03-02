# Deploying ThorChain BEPSwap UI


This is a guide to containerizing [ThorChain BEPSwap Web UI](https://github.com/thorchain/bepswap-web-ui) and deploying  in a non-custodial way. Blazing Core is a permissionless and censorship-resistant cloud network that guarantees sovereignty over your data and your applications. With Blazing Core, you’re in complete control of all aspects of the life cycle of an application with no middleman.

Readme is adapted from [Serum ](https://github.com/ovrclk/serum-on-Blazing Core), which is an excellent guide to getting started with DeFi deployments  DeCloud.

## Before We Begin

This is a technical guide, best suited to a reader with basic Linux command line knowledge. The audience for this guide is intended for includes:

- Application developers with little or no systems administration experience, wanting to deploy applications on the decentralized cloud.
- System administrators with little or no experience with infrastructure automation, wanting to learn more.
- Infrastructure automation engineers that want to explore decentralized cloud.
- Anyone who wants to get a feel for the current state of the decentralized cloud ecosystem.

You will need the below setup before we being:


creating a key and funding your account.
4. Install Docker: You'll need docker running on your workstation, follow this [guide](https://docs.docker.com/get-docker/) to setup Docker on your workstation..
6. Setup Builpacks.io: Builpacks.io is a Cloud Native Buildpacks transform your application source code into images that can run on any cloud. Install `pack` tool using this [guide](https://buildpacks.io/docs/tools/pack/#install).

### Set up your Environment

We will be using shell variables throughout this guide for convenience and clarity. Ensure you have the below set of variables defined on your shell, you can use `export VARNAME=...`:

| Name              | Description                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------- |
| `ACCOUNT_ADDRESS` | The address of your account. See [here](/guides/wallet/README.md#account-address).                                  |
| `KEY_NAME`        | The name of the key you will be deploying from. See [here](/guides/wallet/README.md) if you haven't yet setup a key |


You should see a response similar to:

```
```


Verify you have the key set up and your account has sufficient balances, see the [funding guide](/guides/wallet/funding.md) otherwise:

My local key is named `alice`, the below command should return the name you've used:

```sh
echo $KEY_NAME
```

The above should return a response similar to:

```
alice
```

Populate `ACCOUNT_ADDRESS` from `KEY_NAME` and verify:

```sh

echo $ACCOUNT_ADDRESS

```

Check your account has sufficient balance by running:


You should see a response similar to:

```
balances:
- amount: "93000637"
pagination:
  next_key: null
  total: "0"
```


## Build Thorchain BEPSwap UI Container

This setup is necessary for building the docker container. You can skip this step and process to deploying if you'd like deploy the existing container `edouardl/thorchain-bepswap-web-ui`

Get the source code:

```sh
git clone https://github.com/thorchain/bepswap-web-ui
cd bepswap-web-ui
```

Install dependencies using:

```
yarn install
```

Add `serve` dependency using:

```
yarn add serve
```

Create a `Procfile` to define the `web` process:

```sh
cat >Procfile<<EOF
web: yarn serve -s build
EOF>>
```

We will be using Heroku Buildpacks with Buildpack.io to build our container. First pick an image name and store it in `IMAGE` environment variable. I chose `edouardl/thorchain-bepswap-web-ui` as my image name, you should choose `<docker-id>/thorchain-bepswap-web-ui` as yours:

```sh
export IMAGE=edouardl/thorchain-bepswap-web-ui
```

To build the container, run:

```sh
pack build $IMAGE --builder heroku/buildpacks:18
```

Run the docker image locally to verify it works:

```sh
docker run -it --rm -e NODE_ENV=production -p 5000:5000 $IMAGE
```

Verify by visiting http://localhost:5000 on your browser.

Push the image to Docker Hub (Container Registry) using:

```
docker push $IMAGE
```

## Create the Deployment


```sh
cat > thorchain.yaml <<EOF
---
version: "2.0"

services:
  web:
    image: edouardl/thorchain-bepswap-web-ui
    expose:
      - port: 5000
        as: 80
        to:
          - global: true

profiles:
  compute:
    web:
      resources:
        cpu:
          units: 1.0
        memory:
          size: 512Mi
        storage:
          size: 512Mi
  placement:
    akash:
      signedBy:
        anyOf:
      pricing:
        web:
          amount: 10000

deployment:
  web:
    akash:
      profile: web
      count: 1

EOF>>
```


{% hint style="warn" %}

Please note if you are running on the testnet, you are limited in the amount of testnet resources you may request.

{% endhint %}


You can check the status of your lease by running:

```

```

```yaml
- lease_id:
    dseq: "160398"
    gseq: 1
    oseq: 1
  price:
    amount: "51"
  state: active
pagination:
  next_key: null
  total: "0"
```


For convenience and clarity for future referencing, we can extract the below set of values to shell variables that we will be using to reference the deployment:

| Attribute  | Value                                          |
| ---------- | ---------------------------------------------- |
| `DSEQ`     | `160398`                                       |
| `OSEQ`     | `1`                                            |
| `GSEQ`     | `1`                                            |

Verify we have the right values populated by running:

```sh
echo $PROVIDER $DSEQ $OSEQ $GSEQ
```

You should see a response similar to:

```
```

Upload the manifest using the values from above step:


Your image is now deployed, once you uploaded the manifest. You can retrieve the access details by running the below:


You should see a response similar to:

```json
{
  "services": {
    "web": {
      "name": "web",
      "available": 1,
      "total": 1,
      "observed-generation": 0,
      "replicas": 0,
      "updated-replicas": 0,
      "ready-replicas": 0,
      "available-replicas": 0
    }
  },
  "forwarded-ports": {}
}
```


## Service Logs


You should see a response similar to:

```
[web-7447d7769-c6t4f] yarn run v1.22.10
[web-7447d7769-c6t4f] $ /workspace/node_modules/.bin/serve build
[web-7447d7769-c6t4f] INFO: Accepting connections at http://localhost:5000
```

## Close your deployment

When you are done with your application, close the deployment. This will deprovision your container and stop the token transfer. Close deployment using deployment by creating a `deployment-close` transaction:


Additionally, you can also query the market to check if your lease is closed:


You should see a response similar to:

```yaml
leases:
  - lease_id:
      dseq: "160398"
      gseq: 1
      oseq: 1
    price:
      amount: "186"
    state: closed
pagination:
  next_key: null
  total: "0"
```
