# jitsi-meet

[Jitsi Meet](https://jitsi.org/jitsi-meet/) is an open-source video conferencing solution.
- 80/443: Web interface
- 10000 UDP: Media streaming

## Use Cases

- Video calls
- Remote meetings
- Team collaboration

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.


### Environment Variables

| Variable | Default Value |
|----------|--------------|
| `PUBLIC_URL` | `https://your-domain.com` |
| `ENABLE_LETSENCRYPT` | `1` |
| `LETSENCRYPT_DOMAIN` | `your-domain.com` |
| `LETSENCRYPT_EMAIL` | `your-email@example.com` |
| `TZ` | `UTC` |
| `DOCKER_HOST_ADDRESS` | `your-public-ip` |
| `ENABLE_XMPP_WEBSOCKET` | `1` |
| `XMPP_SERVER` | `prosody` |
| `XMPP_DOMAIN` | `meet.jitsi` |
| `XMPP_AUTH_DOMAIN` | `auth.meet.jitsi` |
| `XMPP_MUC_DOMAIN` | `muc.meet.jitsi` |
| `JICOFO_AUTH_USER` | `focus` |
| `JVB_AUTH_USER` | `jvb` |
| `JVB_BREWERY_MUC` | `jvbbrewery` |
| `JVB_STUN_SERVERS` | `stun.l.google.com:19302` |

### Secrets

The following values are configured as secrets and should be set securely:

- `JICOFO_AUTH_PASSWORD`
- `JVB_AUTH_PASSWORD`


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `jitsi/web:stable` |
| CPU | 1.0 |
| Memory | 2Gi |
| Storage | 5Gi |
| Exposed Ports | 80 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `jitsi/prosody:stable` |
| CPU | 0.5 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 5222 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `jitsi/jicofo:stable` |
| CPU | 0.5 |
| Memory | 1Gi |
| Storage | 1Gi |
| Exposed Ports | 8888 |


## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `jitsi/jvb:stable` |
| CPU | 1.0 |
| Memory | 2Gi |
| Storage | 1Gi |
| Exposed Ports | 10000 |
