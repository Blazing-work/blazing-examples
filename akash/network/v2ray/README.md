# V2RAY Server Deployment

| [V2RAY Website](https://www.v2fly.org/en_US) | [V2RAY GitHub](https://github.com/v2fly) |
|:--:|:--:|

## Step 1: Create and Share Your config.json

You can use the default `config.json` included in the container. Set the `ID` in the SDL using a [UUID generator](https://www.uuidgenerator.net/), or leave it unchanged.

Alternatively, create your own `config.json` using the [V2RAY documentation](https://www.v2fly.org/en_US/guide/start.html). Host your `config.json` on any platform with direct download support (GitHub, Google Drive, etc.).

## Step 2: Deploy

Deploy the `core.yaml` file via Blazing Core. Select a provider and wait for the deployment to complete.

## Step 3: Usage

You can use **V2RAY** as a `socks` proxy for your browser or application, or as a VPN connection.

**Browser setup:** Configure your proxy settings to `socks` with your provider's address and the forwarded port from the **LEASES** tab.

**Android:** Use the [V2RAY NG](https://play.google.com/store/apps/details?id=com.v2ray.ang) app. Create a new profile specifying the provider's address, the `vmess` forwarded port, and the `UUID` from your `config.toml`.

More client applications are available on the [V2RAY GitHub releases](https://github.com/v2fly/v2ray-core/releases) page. See the [V2RAY client docs](https://www.v2fly.org/en_US/guide/start.html#client) for setup instructions.
