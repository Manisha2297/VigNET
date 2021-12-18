# VigNET
VigNET is a **Visual Question Answering application (VQA)**. The application has 3 major components:
1. **API service** - API is built using FastAPI to get predictions from the trained model. The deployed application is currently using **ViLT (Vision Language Transformer) model for performing VQA task**.
2. **Data collector** - This component keeps track of all the experiments done on various models and fetches the latest model weights.
3. **Frontend Simple** - This is the UI component of the application built using HTML, CSS and Javascript.

All these components are containerised and deployed on **Google Compute Engine**. The end to end application is hosted on GCP using the NGNIX container. Deployment on GCP is done using Ansible playbook script. 


