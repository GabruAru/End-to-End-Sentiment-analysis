# <div align="center">Sentiment Analysis Project Documentation</div>

## Overview
This project is a Sentiment Analysis API built using  [FastAPI](https://fastapi.tiangolo.com/). The API analyzes text input and predicts the sentiment, classifying it as negative, neutral, or positive. The application is containerized using Docker and deployed with Kubernetes.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Deploy with Kubernetes](#deploy-with-kubernetes)
- [API Usage](#api-usage)
  - [Endpoint](#endpoint)
  - [Request](#request)
  - [Response](#response)
- [Logging](#logging)
- [Docker Usage](#docker-usage)

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Access to a Kubernetes cluster- Enable Kubernetes From Dokcer Desktop setting

##  Getting Started
  
### Clone the Repository

```bash
git clone https://github.com/GabruAru/Sentiment-analysis.git
cd Sentiment-analysis
```

### Deploy with Kubernetes


  
1. Deploy Database
    ```bash
    kubectl apply -f db-data-persistentvolumeclaim.yaml
    kubectl apply -f db-deployment.yaml  
    ```

2. Get POD IP as highlighted
    ```bash
    kubectl get pods -o wide    
    ```

![image](https://github.com/GabruAru/Sentiment-analysis/assets/84130891/7d892c24-a330-42fc-a957-7f8547fa6815)

 3. Edit app-deployment.yaml with your-ip from above
    ```bash
    env:
      - name: DATABASE_URL
        value: mysql+mysqlconnector://root:admin@<Your-IP>:3306/sentiment   
    ```
   

 4. Deploy FastAPI web service

    ```bash
    kubectl apply -f app-deployment.yaml     
    kubectl apply -f app-service.yaml
    ```
5. Stop the cluster with
   ```bash
   kubectl scale deployment app --replicas=0
   kubectl scale deployment db --replicas=0
   ```



##  API Usage

  ```bash
    kubectl get services
  ```

![image](https://github.com/GabruAru/Sentiment-analysis/assets/84130891/e22415fc-024a-4b7d-8fbf-53f8368b1766)

### Endpoint
    
    The Sentiment Analysis FastAPI Swagger UI is available at:
    
    ```bash
    http://localhost:<node_port>/docs
    ```
    Replace <node_port> with the actual node port assigned to the app-service in your Kubernetes cluster.

### Request 

    Send a POST request to the /predict endpoint with a JSON payload:
    
    ``` bash
    {
      "text": "Your text for sentiment analysis."
    }
    ```

### Response 

  The API will respond with a JSON object containing the predicted sentiment:
  
  ``` bash
  {
    "sentiment_class": "positive"
  }
  ```

##  Logging

The application logs each sentiment analysis request and response to a MySQL database. You can access the logs using the /logs/ endpoint.

##  Docker Usage

1. Build with Docker 

    Use this application and deploy it yourself on local machine, save you model in saved_model directory 
    
    ```bash
    docker-compose build
    ```

2. Deploy locally with 

    ```bash
    docker-compose up
    ```

Use the API on localhost:8000

3. CleanUp

    ```bash
    docker-compose down
    ```

4. Pull the already build image from Docker Hub

    ```bash
    docker pull aryan381/senitment-analysis-app:latest
    docker pull aryan381/sentiment-analysis-db:lastest
    ```
















