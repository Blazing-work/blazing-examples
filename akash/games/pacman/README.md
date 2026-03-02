# pacman

Pac-Man Game
Pac-Man is a maze chase video game; the player controls the eponymous character through an enclosed maze. The objective of the game is to eat all of the dots placed in the maze while avoiding four colored ghosts — Blinky (red), Pinky (pink), Inky (cyan), and Clyde (orange) — that pursue him. When all of the dots are eaten, the player advances to the next level. If Pac-Man makes contact with a ghost, he will lose a life; the game ends when all lives are lost.
This is accurate remake of the original game. The Docker image built from [this](https://github.com/masonicGIT/pacman) GitHub repository.

## Use Cases

- Game server hosting
- Multiplayer gaming
- Community servers

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Open the web interface at `http://{SERVICE_URI}:80/`
3. Follow any on-screen setup instructions

## Accessing the Service

Open `http://{SERVICE_URI}/` in your browser.

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `yuravorobei/pacman-web` |
| CPU | 1.0 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 80 |
