# tensorflow-webapp-mnist

For more information, see the [GitHub repo](https://github.com/wlouie1/mnist-app), and this guide titled [Machine Learning  DeCloud (Part 3/3): Deploying a Deep Learning Web Application](https://wilsonlouie.medium.com/machine-learning-on-Blazing Core-decloud-part-3-3-deploying-a-deep-learning-web-application-6a9e71e71dd1).


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `wlouie1/mnist-tf-serve:1.0` |
| CPU | 0.2 |
| Memory | 512Mi |
| Storage | 512Mi |
| Exposed Ports | 8501 |


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `wlouie1/mnist-flask-serve:1.0` |
| CPU | 0.2 |
| Memory | 256Mi |
| Storage | 1Gi |
| Exposed Ports | 5000 |


### Deployment Specs

| Resource | Value |
|----------|-------|
| Image | `wlouie1/mnist-app:1.0` |
| CPU | 0.1 |
| Memory | 256Mi |
| Storage | 512Mi |
| Exposed Ports | 80 |
