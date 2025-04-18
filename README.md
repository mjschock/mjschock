# Michael James Schock

<!-- |   |   |
|---|---|
| Email | m@mjschock.com |
| GitHub | mjschock |
| LinkedIn | in/mjschock |
| Phone | +1 925 878 5408 |
| Web | mjschock.com | -->

<!-- | Email: m@mjschock | GitHub: mjschock | LinkedIn: in/mjschock | Phone: +1 925 878 5408 -->
Email: m@mjschock | LinkedIn: in/mjschock | Phone: +1 925 878 5408

## Professional Experience

### Founding Engineer
**ArchiLabs** | San Francisco, CA (Hybrid) | *Mar. 2025 - Present*

* Working on ArchiLabs' mission to create the first AI Architect to make all new construction faster & more affordable
* Developing across the full stack, including Revit integrations, React frontend, Supabase, and AI agents powered by LangGraph
* Working directly with the CEO and CTO founders and the BIM specialist
* Contributing to a fast-moving YC-backed startup focused on solving critical problems in the construction industry
* Improving the AI capabilities to enhance construction planning and design efficiency

### Software Engineer (AI/ML Platform)
**Phaidra** | Seattle, WA (Remote) | *Oct. 2022 - Jan. 2024*

<!-- * Spearheaded orchestration and automation of AI agent training (with each agent an ensemble of PyTorch models) into an MLOps pipeline backed by a self-hosted in-cluster duo of Prefect Server and Agent to run training ad-hoc and on-schedule, with follow-up work demonstrating the migration path from the deprecated Prefect Agent to Kubernetes-native Prefect Worker. -->
<!-- * Rapidly prototyped a working MVP showcasing how we could easily scale the training runs via the Prefect-Ray integration and an in-cluster or Anyscale Cluster, also presenting SkyPilot as a way to abstract Ray and cloud computing resources, optimizing for minimal computational cost or time. -->
<!-- * Modernized the developer experience for the AI Platform team by bringing in Tilt to watch for changes in the Kubernetes manifests for full Docker build/pushes, thereafter updating pods without reload for fast iteration, and providing custom functionality to run data preparation, agent training, and inference pipelines via configurable buttons in the Tilt UI. -->
* Spearheaded orchestration and automation of AI agent training (with each agent an ensemble of PyTorch models) into an MLOps pipeline using Prefect Server and Agent, demonstrating scalability using the Prefect-Ray integration and Ray.
* Modernized the developer experience by implementing Tilt for Kubernetes manifest changes, enabling rapid iteration with custom functionality for running ad-hoc data preparation, agent training, and inference pipelines.
* Pioneered a proof-of-concept for cost-efficient scaling using SkyPilot to abstract Ray and cloud computing resources, optimizing for minimal computational cost and time.

<!-- **Technologies**: Cloud SQL for PostgreSQL, Docker, Google Cloud Platform (GCP), Google Kubernetes Engine (GKE), gRPC, Prefect, Python, PyTorch, Ray, SkyPilot, Tilt -->

### Teaching Assistant
**Georgia Institute of Technology** | Atlanta, GA (Part-Time; Remote) | *Aug. 2022 - Dec. 2022*

* Served as a Teaching Assistant (TA) for CS 7639: Cyber-Physical Systems Design & Analysis.

### Machine Learning Engineer
**Greyscale AI** | San Carlos, CA | *Oct. 2021 - Jul. 2022*

<!-- * Created a proof of concept (POC) for a data engineering pipeline to extract, transform, and load images and their corresponding labels from various data sources and formats into the COCO dataset format with k-fold train-validation-test splits using the FiftyOne and Albumentations libraries. -->
<!-- * Constructed a POC for a data modeling pipeline to train and validate a PyTorch Faster R-CNN model with various modifications for computer vision tasks such as object detection and image segmentation from a train-validation split output by the data engineering pipeline. -->
<!-- * Assembled a POC for a model deployment pipeline to deploy a model produced by the data modeling pipeline into a local docker container running TorchServe (or SageMaker) to run inference tests upon that model and to trigger the creation of a function that ran on schedule to monitor the deployed model.
* Designed a dashboard using Amazon QuickSite to automatically generate visualizations, including emails pointing to those visualizations, that displayed the performance of the served model and assigned SageMaker GroundTruth jobs for our internal teams to help with data labeling. -->
<!-- * Built a POC framework using Kedro and DVC to join the data engineering, data modeling, and model deployment pipelines, running pipeline components only when artifacts tracked by DVC changed. -->
* Developed an end-to-end data engineering pipeline to process diverse image sources into the COCO dataset format with k-fold train-validation-test splits using the FiftyOne and Albumentations libraries.
* Architected and implemented a data modeling pipeline for training PyTorch Faster R-CNN models for computer vision tasks, incorporating advanced object detection and image segmentation capabilities.
* Created an automated model deployment pipeline using Docker and TorchServe/SageMaker, including scheduled model monitoring and performance visualization through Amazon QuickSight.
* Unified the data engineering, modeling, and deployment pipelines using Kedro and DVC, implementing intelligent artifact tracking for efficient pipeline execution.

<!-- **Technologies**: Albumentations, Amazon QuickSite, Amazon SageMaker Ground Truth, Docker, DVC, Faster R-CNN, FiftyOne, Kedro, Matplotlib, MobileNet, NumPy, pandas, Python, PyTorch, scikit-learn, TorchServe, torchvision -->

### Machine Learning Engineer
**Ople.AI** | San Mateo, CA | *Sep. 2018 - Oct. 2021*

<!-- * Refactored the data ingestion pipeline into more modular components.
* Drove the model explainability implementation.
* Led the development of the forecasting service.
* Built a worker service that operated on graph structures representing machine learning tasks and states.
* Developed various features and addressed bugs in our systems. -->
* Refactored the data ingestion pipeline into modular components, improving system maintainability and scalability.
* Led the development and implementation of the forecasting service using Amazon Forecast, enhancing predictive capabilities.
* Architected and built a distributed worker service operating on graph structures for complex machine learning tasks and state management.
* Drove the implementation of model explainability features using SHAP (SHapley Additive exPlanations).

<!-- **Technologies**: Amazon Forecast, Amazon Web Services (AWS), Docker, Docker Compose, JavaScript, LightGBM, Matplotlib, NumPy, pandas, Python, SHAP (SHapley Additive exPlanations), Tableau -->

<!-- ### Software Engineer
**BigCommerce** | San Francisco, CA | *Nov. 2016 - Sep. 2018*

* Engineered features for the BigCommerce storefront platform.
* Wrote unit tests for all new and changed code, increasing code coverage.
* While taking the lead on building out a new feature, discovered an opportunity to improve the codebase by refactoring the code into an easier-to-reason-about structure such that future additions wouldn't require as much overhead.

* Engineered critical features for BigCommerce storefront platform using React, gRPC, and microservices architecture.
* Implemented comprehensive unit testing strategy for new and modified code, significantly increasing code coverage.
* Led architectural improvements through strategic code refactoring, reducing technical debt and streamlining future feature development.

**Technologies**: Amazon Web Services (AWS), Docker, gRPC, hapi, JavasScript/TypeScript, Laravel, PHP, React, Ruby, Ruby on Rails

### Software Engineer
**Autodesk (via Globant)** | San Francisco, CA | *May 2014 - Oct. 2016*

* Implemented features for the Customer Enterprise Portal for Autodesk.
* Caught up to speed quickly, diving into the codebase with minimal support.
* Formed a POC to re-architect a centerpiece of the Portal, refactoring spaghetti code and building a more well-organized system that can easily accommodate new types of Autodesk products and services along with their associated data and functionality.
* Taught and led other developers with patience and a desire to improve their understanding.
* Responded to bugs, defects, and applicable business concerns with a strong sense of urgency.

* Implemented key features for Autodesk's Customer Enterprise Portal using Java Servlets and Backbone.js.
* Led architectural redesign of Portal's core components, transforming legacy code into a scalable system supporting diverse product types.
* Mentored development team while maintaining rapid response to critical bugs and business requirements.

**Technologies**: Amazon Relational Database Service (RDS), Apache Tomcat, Backbone.js, Docker, Java, Java Servlets, JavasScript/TypeScript

### Software Engineer
**PlantLog** | Pleasanton, CA | *Aug. 2012 - May 2014*

* Converted features from the legacy implementation of PlantLog, which ran only on Windows as a native application, to a web and mobile application hosted in the cloud. Re-architected the backend to be RESTful, refactoring a single large switch case into resource-specific endpoint logic.
* Converted legacy reporting components for use in the new system.
* Rebuilt the mobile app, using the BackboneJS framework to organize the application.
* Added barcode scanning/lighting functionality to the mobile app.

* Led migration of Windows-based PlantLog to cloud-hosted web and mobile application using AWS and Apache Cordova.
* Redesigned backend architecture from monolithic to RESTful API, improving system modularity and maintainability.
* Integrated advanced mobile features including barcode scanning and reporting components using Backbone.js and JasperReports.

**Technologies**: Amazon Web Services (AWS), Apache Cordova/PhoneGap, Backbone.js, Google Web Toolkit (GWT), iOS, JasperReports, Java, JavasScript -->

## Education

### Master Of Science In Computer Science
<!-- **Georgia Institute of Technology** | Atlanta, GA (Less-than-Part-Time; Remote) | *Jan. 2018 - May 2025* -->
**Georgia Institute of Technology** | Atlanta, GA | *Jan. 2018 - May 2026*
<!-- Specialization in Computational Perception and Robotics -->

### Bachelor Of Arts In Physics
**University Of California, Berkeley** | Berkeley, CA

## Coursework & Certifications

<!-- | Course/Certification | Institution | Date |
|---------------------|-------------|------|
| CS 7650: Natural Language Processing | Georgia Tech | Fall 2024 |
| Practical Multi AI Agents and Advanced Use Cases with crewAI | DeepLearning.AI | Nov. 2024 |
| Introducing Multimodal Llama 3.2 | DeepLearning.AI | Oct. 2024 |
| AI Agents in LangGraph | DeepLearning.AI | Sep. 2024 |
| Function-calling and data extraction with LLMs | DeepLearning.AI | Sep. 2024 |
| Pretraining LLMs | DeepLearning.AI | Sep. 2024 |
| AI Agentic Design Patterns with AutoGen | DeepLearning.AI | Jul. 2024 |
| Generative AI Nanodegree | Udacity | May 2024 |
| Multi AI Agent Systems with crewAI | DeepLearning.AI | May 2024 |
| CS 6603: AI, Ethics, and Society | Georgia Tech | Spring 2024 |
| CS 7646: Machine Learning for Trading | Georgia Tech | Fall 2023 |
| Prefect Associate Certification | Prefect | Apr. 2023 |
| CS 7643: Deep Learning | Georgia Tech | Fall 2022 |
| Machine Learning Engineer Skill Set Certification | Workera | Aug. 2022 |
| CS 7639: Cyber-Physical Systems Design & Analysis | Georgia Tech | Spring 2021 |
| CS 7642: Reinforcement Learning & Decision Making | Georgia Tech | Fall 2019 |
| Deep Reinforcement Learning Nanodegree | Udacity | Jul. 2019 |
| CS 7641: Machine Learning | Georgia Tech | Spring 2019 |
| Math for Machine Learning Specialization | Coursera | Jan. 2019 |
| Deep Learning Part I Certificate | The Data Institute, USF | Dec. 2018 |
| CS 6601: Artificial Intelligence | Georgia Tech | Fall 2018 |
| Deep Learning Specialization | Coursera/DeepLearning.AI | Sep. 2018 |
| CS 7638: Artificial Intelligence Techniques for Robotics | Georgia Tech | Spring 2018 |
| Deep Learning Foundation Nanodegree | Udacity | Jan. 2018 |
| React Nanodegree | Udacity | Dec. 2017 |
| Artificial Intelligence Nanodegree and Specializations | Udacity | Oct. 2017 |
| Machine Learning Specialization | Coursera | Feb. 2017 |
| CSCI E-160: Java for Distributed Computing | Harvard Extension School | 2012 | -->

| Course/Certification | Institution | Date |
|---------------------|-------------|------|
| CS 7650: Natural Language Processing | Georgia Tech | Fall 2024 |
| Practical Multi AI Agents and Advanced Use Cases | DeepLearning.AI | Nov. 2024 |
| Introducing Multimodal Llama 3.2 | DeepLearning.AI | Oct. 2024 |
| AI Agents in LangGraph | DeepLearning.AI | Sep. 2024 |
| Function-calling and data extraction with LLMs | DeepLearning.AI | Sep. 2024 |
| Pretraining LLMs | DeepLearning.AI | Sep. 2024 |
| AI Agentic Design Patterns with AutoGen | DeepLearning.AI | Jul. 2024 |
| Generative AI Nanodegree | Udacity | May 2024 |
| Multi AI Agent Systems with crewAI | DeepLearning.AI | May 2024 |
| CS 6603: AI, Ethics, and Society | Georgia Tech | Spring 2024 |
| CS 7646: Machine Learning for Trading | Georgia Tech | Fall 2023 |
| Prefect Associate Certification | Prefect | Apr. 2023 |
| CS 7643: Deep Learning | Georgia Tech | Fall 2022 |
| Machine Learning Engineer Skill Set Certification | Workera | Aug. 2022 |
| CS 7639: Cyber-Physical Systems Design & Analysis | Georgia Tech | Spring 2021 |
| CS 7642: Reinforcement Learning & Decision Making | Georgia Tech | Fall 2019 |
| Deep Reinforcement Learning Nanodegree | Udacity | Jul. 2019 |
| CS 7641: Machine Learning | Georgia Tech | Spring 2019 |
| Math for Machine Learning Specialization | Coursera | Jan. 2019 |
| Deep Learning Part I Certificate | The Data Institute, USF | Dec. 2018 |
| CS 6601: Artificial Intelligence | Georgia Tech | Fall 2018 |
| Deep Learning Specialization | Coursera/DeepLearning.AI | Sep. 2018 |
| CS 7638: AI Techniques for Robotics | Georgia Tech | Spring 2018 |
| Deep Learning Foundation Nanodegree | Udacity | Jan. 2018 |
| Artificial Intelligence Nanodegree and Specializations | Udacity | Oct. 2017 |
| Machine Learning Specialization | Coursera | Feb. 2017 |

<!-- ## Skills

Accelerate, Agent Protocol, AutoGen, AutoGPT, bitsandbytes, Computer Vision, ControlFlow, crewAI, DataDreamer, Datasets, Diffusers, Evaluate, Function/Tool Calling, JavaScript/TypeScript, LangChain, LangGraph, llama.cpp, LlamaIndex, Marvin, Multimodal LLM/VLMs, NumPy, OpenAI, PEFT (Parameter-Efficient Fine-Tuning), pandas, PostgreSQL, Prefect, Python, PyTorch, Ray, Reflex, scikit-learn, SkyPilot, smolagents, SQL, Supabase, Swarms, Tokenizers, timm, Transformers, TRL, ... -->
