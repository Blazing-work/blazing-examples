# ruby-on-rails

[Ruby](https://rubyonrails.org/) is a dynamic, reflective, object-oriented, general-purpose, open-source programming language.
This template is a demonstration of the Ruby web framework . Check out [Ruby on Docker Hub](https://hub.docker.com/_/ruby) to learn how to Dockerize your project.
The SDL configuration from this repository uses the `nomorelies/rubyonakash:0.4` image, which is based on the official Ruby image `ruby:3.5-rc-alpine3.22`. Ruby is used to run the `server.rb` script, which uses the `webrick` library to serve a static site on port 8000.

## Use Cases

- Web application hosting
- API serving
- Full-stack deployment

## Getting Started

1. Deploy the template and wait for the service to reach "Running" status
2. Send HTTP requests to `http://{SERVICE_URI}:8000/`
3. Check the service documentation for available API endpoints

## Accessing the Service

Send requests to `http://{SERVICE_URI}:8000/`.

Example:
```bash
curl http://{SERVICE_URI}:8000/
```

## Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `nomorelies/rubyonakash:0.4` |
| CPU | 0.5 |
| Memory | 512Mi |
| Storage | 1Gi |
| Exposed Ports | 8000 |
