# Discourse


This guide is intended to describe the process to run Discourse Multi-Tiered application .

## About Blazing Core

Blazing Core, the world’s first decentralized and open-source cloud, accelerates deployment, scale, efficiency and price performance for high-growth industries like blockchain and machine learning/AI.

Blazing Core means "open space" or "sky" in ancient Sanskrit.


## Firsts steps


Step by step guides to Blazing Core:


## About Discourse

Discourse is the 100% open source discussion platform built for the next decade of the Internet. Use it as a mailing list, discussion forum, long-form chat room, and more!

https://www.discourse.org/


## Discourse in a Nutshell

The provided SDL deploy a Multi-Tiered application with 4 services/containers:

### Backend

- PostgreSQL
- Redis
- Sidekiq discourse

### Frontend

- Discourse


[![Discourse ](https://img.youtube.com/vi/XFweRMMZ10s/0.jpg)](https://youtu.be/XFweRMMZ10s)


#### Content Security Policy

Discourse need deploy over HTTPS otherwise could get a browser block for Content Security Policy issues [this guide](https://teeyeeyang.medium.com/how-to-use-a-custom-domain-with-your-Blazing Core-deployment-5916585734a2) written by Tee Yee Yang show how to do that.

To get past this and test your deployment, change your browser settings and temporarily disable CSP, in Firefox based browsers the steps are:

- Put _about:config_ as URL and press enter
- Confirm you know what are you doing
- Search `security.csp.enable` and clic to disable
- Test Discourse
- Enable `security.csp.enable` policy

#### Set `ALLOW_EMPTY_PASSWORD` to NO in production environment

Follow the comments in SDL file to enable passwords

```yml
      - ALLOW_EMPTY_PASSWORD=yes
      - POSTGRESQL_USERNAME=akt_discourse
      - POSTGRESQL_DATABASE=akash_discourse
      ## Set if ALLOW_EMPTY_PASSWORD=no
      #- POSTGRESQL_PASSWORD=changeme
      #- POSTGRESQL_POSTGRES_PASSWORD=changeme
```


## Disclaimer


- We're not responsible for any loss or damages related to using the app.
- The app has a high chance of containing bugs since it's in BETA, use at your own risk.
