# big-dipper

Big Dipper
=======
Big Dipper is a widely used blockchain explorer developed by [Forbole](https://www.forbole.com/).
This deployment consists of 2 containers, one running MongoDB, the other running the web frontend.
The image was built using the [Dockerfile](https://github.com/forbole/big-dipper/tree/akash-challenge-3) from github, and the SDL file adapted from the docker-compose file in the same repo.


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `mongo:latest` |
| CPU | 0.4 |
| Memory | 512Mi |
| Storage | 2Gi |
| Exposed Ports | 27017 |


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `raviforbole/bigdipper:Blazing Core` |
| CPU | 0.6 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 3000 |
