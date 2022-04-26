# VigNET

## 1. Introduction
VigNET is a **Visual Question Answering application (VQA)**. VQA is a system that attempts to give an answer given an image and a question related to the image. This app also has speech-to-text and text-to-speech capabilities to make the app more accessible.

The application has 3 major components:
1. [**API service**](https://github.com/Manisha2297/VigNET/tree/main/api-service) - API is built using FastAPI to get predictions from the trained model. The deployed application is currently using **ViLT (Vision Language Transformer) model for performing VQA task**.
2. [**Data collector**](https://github.com/Manisha2297/VigNET/tree/main/data-collector) - This component keeps track of all the experiments done on various models and fetches the latest model weights.
3. [**Frontend Simple**](https://github.com/Manisha2297/VigNET/tree/main/frontend-simple) - This is the UI component of the application built using HTML, CSS and Javascript.
4. [**Frontend React**](https://github.com/Manisha2297/VigNET/tree/main/frontend-new) - This is the UI component of the application built using React. This is more responsive, fast and rich compared to frontend-simple.

**Note: Use either the Frontend Simple or Frontend React component for UI.** 

API service and Frontend React has been containerised and deployed on Google Kuberenetes Engine. The end to end application is hosted on GCP (Google Cloud Platform) using the NGNIX container.

All these components can also be containerised and deployed on **Google Compute Engine**. Deployment on GCP can be done using Ansible playbook script. We have followed the instructions in [dlops-io/mushroom-app](https://github.com/dlops-io/mushroom-app/tree/06-deployment) repository for deploying the application on GCP.

We have referred [ViLT](https://github.com/dandelin/ViLT) repository and [paper](https://arxiv.org/pdf/2102.03334.pdf) for solving visual question answering task.

## 2. How to get VigNET app working?
Follow the steps mentioned below to get the VigNET app working:

**Step 1: Create a docker container for API service**
 - Go to api-service folder and execute the following command in your terminal ```sh docker-shell.sh```. This will create an api-service container.
 - Run ```uvicorn_server``` in the terminal to get the api-service up and running on port 9000. You can browse http://localhost:9000/docs to see the API documentation.
 
**Step 2: Create a docker container for Data collector service**
- You can create this container if you want to experiment with different models for performing VQA task. This service will download the latest model weights from the path mentioned.
- Go to data-collector folder and execute the following command in your terminal ```sh docker-shell.sh```. This will create data-collector container.

**Step 3: Create a docker container for Frontend service**
- If you want to plugin frontend-simple, do the following:
  - Go to frontend-simple folder and execute the following command in your terminal ```sh docker-shell.sh```. This will create front-end container.
  - Run ```http-server``` in the terminal to get the frontend service up and running on port 8080. 
- If you want to plugin frontend-react, do the following:
  - Go to frontend-new folder and execute the following command in your terminal ```sh docker-shell.sh```. This will create front-end container.
  - This will build and run the container.

Now, the application will be ready to use. Browse http://localhost:8080 for the application.

For deploying and hosting the application on GCP, please refer [dlops-io/mushroom-app](https://github.com/dlops-io/mushroom-app/tree/06-deployment) repository.
