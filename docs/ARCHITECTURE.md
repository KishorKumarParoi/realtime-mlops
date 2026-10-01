# Real-Time MLOps Architecture & System Design
**Project**: Real-Time Customer Churn Prediction Engine  
**Lifecycle Stage**: Production Architecture & System Specifications  

---

## 1. High-Level Architecture Overview

The **Real-Time MLOps** platform is designed for sub-50ms inference latency, continuous model governance, automated training pipelines, and declarative GitOps delivery on Kubernetes.

```
+-----------------------------------------------------------------------------+
|                            Real-Time Client / App                           |
+-----------------------------------------------------------------------------+
                                      |  (HTTPS / REST POST /predict)
                                      v
+-----------------------------------------------------------------------------+
|                           Kubernetes Ingress / Service                      |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
|              FastAPI Microservice (Gunicorn + Uvicorn Workers)              |
|   - Request Validation (Pydantic Schema)                                    |
|   - Feature Scaling & Imputation Pipeline                                   |
|   - In-Memory Scikit-Learn Model Inference (<15ms)                          |
|   - Prometheus Telemetry & Latency Histogram                                |
+-----------------------------------------------------------------------------+
               ^                                               |
               | (Model Weights & Artifacts)                   | (Drift Logs)
               |                                               v
+-----------------------------+               +-------------------------------+
|      AWS S3 Model Store     |               |    CloudWatch / Prometheus    |
|   - DVC Versioned Checkpoints|               |   - Latency (p95, p99)        |
|   - Metadata & Feature Maps |               |   - Churn Probability Drift   |
+-----------------------------+               +-------------------------------+
```

---

## 2. Core Pillars of the Architecture

### A. Real-Time Inference Microservice
- **Runtime**: FastAPI powered by Uvicorn worker threads managed by Gunicorn.
- **Payload Schema**:
  ```json
  {
    "age": 45,
    "tenure_months": 24,
    "monthly_charges": 79.99,
    "total_charges": 1920.00,
    "num_support_calls": 3
  }
  ```
- **Response SLA**: Target p95 latency under `35ms`, p99 latency under `60ms`.

### B. Data & Model Version Control (DVC)
- Raw and processed training datasets (`churn_data.csv`) are versioned with DVC.
- Binary blobs and serialized pipelines (`models/model.pkl`) are backed by AWS S3 remote storage (`s3://...`).
- Git tracks `.dvc` hash pointer files, guaranteeing exact reproducibility across environments.

### C. Continuous Integration & GitOps Delivery
- **GitHub Actions**: Linting (`flake8`, `black`), testing (`pytest`), Docker image compilation, and security vulnerability scanning.
- **ArgoCD**: Declarative continuous deployment watching `k8s/` and syncing live Kubernetes cluster states.

### D. Governance & Drift Monitoring
- Prediction probabilities and incoming customer feature vectors are streamed to monitoring collectors to detect concept drift and covariate shift.
- Automated alert triggers pipeline execution when Kolmogorov-Smirnov drift threshold exceeds `0.05`.
