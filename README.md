## <div align="center">Sentiment Analysis Project Documentation</div>

### Overview
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
- [Deployment](#deployment)
  - [Docker](#docker)
  - [Kubernetes](#kubernetes)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Access to a Kubernetes cluster

## Getting Started

### Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```
### Deploy with Kubernetes

#### 1. Deploy Database
```bash
kubectl apply -f db-data-persistentvolumeclaim.yaml
kubectl apply -f db-deployment.yaml  
```

#### 2. Get POD IP 
```bash
kubectl get pods -o wide    
```

![image](https://github.com/GabruAru/Sentiment-analysis/assets/84130891/7d892c24-a330-42fc-a957-7f8547fa6815)


Get the IP address as highlighted from your terminal 

#### 3. Edit app-deployment.yaml
```bash
env:
  - name: DATABASE_URL
    value: mysql+mysqlconnector://root:admin@<Your-IP>:3306/sentiment   
```

![image](https://github.com/GabruAru/Sentiment-analysis/assets/84130891/0d9b5132-8121-4803-abe4-fec16504bb93)

Edit that IP address on app-deployement. 



#### 4. Deploy FastAPI web service

```bash
kubectl apply -f app-deployment.yaml     
kubectl apply -f app-service.yaml        
```

### API Usage 

```bash
kubectl get services
```







