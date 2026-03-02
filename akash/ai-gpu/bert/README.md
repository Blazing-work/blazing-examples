# BERT


This repository contains the necessary files to deploy a Flask application that uses the BERT language model . BERT is a powerful language model that can understand and generate text in English.

Link to original Google Research Repo: https://github.com/google-research/bert

## Files

- `Dockerfile`: This file is used to build the Docker image for the application. It sets up an environment with Python and all the necessary libraries to run the application.
- `requirements.txt`: This file lists the Python packages that need to be installed in the Docker image. This includes Flask for the web application and the Transformers library for the BERT model.
- `app.py`: This is the main application file. It creates a Flask web application that uses the BERT model to predict the masked words in a sentence.

## Deployment


1. Build the Docker image: `docker build -t your-dockerhub-username/bert-base-uncased:0.0.1 .`
2. Push the Docker image: `docker push your-dockerhub-username/bert-base-uncased:0.0.1`


## Usage

The application listens on port 80 and accepts POST requests to the `/predict` endpoint. The POST request should contain a JSON object with a single attribute 'text' that contains the sentence with a word replaced by '[MASK]'. The application will return the sentence with the '[MASK]' replaced by the predicted word.

For example, you can use curl to send a POST request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"This [MASK] model can understand and generate text in multiple languages."}' http://{SERVICE_URI}/predict
```
