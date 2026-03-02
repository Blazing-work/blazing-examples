# supermario

Supermario  Game
The Super Mario games follow Mario's adventures, typically in the fictional Mushroom Kingdom with Mario as the player character.

## Use Cases

- Game server hosting
- Multiplayer gaming
- Community servers

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:8080/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}:8080/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `pengbai/docker-supermario` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 8080 |
