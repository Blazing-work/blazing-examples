# BERT Sentiment Analysis


This repository contains the necessary files to deploy a sentiment analysis model based on the BERT architecture . The model is capable of classifying text into five sentiment categories: very negative, negative, neutral, positive, and very positive.

## Model

The model used is the `nlptown/bert-base-multilingual-uncased-sentiment` model from Hugging Face. This model is capable of understanding and generating text in multiple languages, making it versatile for various use cases.

## Files

- `app.py`: This is the main application file. It uses Flask to create a web application that takes user input, passes it to the model, and returns the sentiment prediction.
- `Dockerfile`: This file contains the instructions to build the Docker image for the application.
- `requirements.txt`: This file lists the Python libraries required by the application.
- `index.html`: This file contains the HTML code for the application's user interface.

## Deployment


1. Clone this repository.
2. Build the Docker image and push it to a Docker registry.


## Testing the Application

Once the application is deployed, you can test it by sending a POST request to the `/predict` endpoint with a JSON payload containing the text to be analyzed. For example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"I love this product!"}' http://<{SERVICE_URI}>/predict
```

The application will return a JSON response with the sentiment prediction:

{"sentiment": "positive"}

## UI Interactivity
https://youtu.be/aXOdjNLQarw?t=456
