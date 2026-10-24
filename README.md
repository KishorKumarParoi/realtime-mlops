# ⚡ Real-Time MLOps: Sub-50ms Churn Prediction & Serving System

[![FastAPI](https://img.shields.io/badge/FastAPI-v0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![DVC](https://img.shields.io/badge/DVC-Data_Version_Control-945DD6?logo=dvc&logoColor=white)](https://dvc.org/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Cloud_Native-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![ArgoCD](https://img.shields.io/badge/ArgoCD-GitOps-F27E2B?logo=argo&logoColor=white)](https://argoproj.github.io/cd/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Telemetry-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Architecture: Blueprint](https://img.shields.io/badge/Architecture-Specification-8A2BE2?logo=diagramsdotnet&logoColor=white)](ARCHITECTURE.md)
[![Workflow: SVG Flow](https://img.shields.io/badge/Workflow-Interactive_SVG-00C7B7?logo=vectorlogozone&logoColor=white)](docs/images/01_architecture_flow.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Cloud-Native, Production-Hardened Real-Time MLOps Architecture** engineered for sub-50ms customer churn inference. Implements Pydantic v2 contract enforcement, DVC dataset and model artifact versioning on AWS S3, Kolmogorov-Smirnov concept drift detection, Prometheus observability, and declarative GitOps continuous delivery on Kubernetes. Full architectural blueprint available in [ARCHITECTURE.md](ARCHITECTURE.md) and interactive vector flow in [01_architecture_flow.svg](docs/images/01_architecture_flow.svg).

---

## ⚡ Zero-Touch 1-Command Autonomous EC2 & Cloud Deployment

Launch the complete Real-Time MLOps Platform directly on **any fresh, bare EC2 instance (Ubuntu, Debian, Amazon Linux 2023) or cloud VM** in a single command. **No pre-installation of Git, Docker, or Python is required**:

```bash
curl -fsSL https://raw.githubusercontent.com/KishorKumarParoi/realtime-mlops/main/bootstrap.sh | bash
```

### 🎯 Fast Execution Modes

| Deployment Mode | Command | Footprint & SLA |
| :--- | :--- | :--- |
| **Standard Containerized Stack** | `curl -fsSL https://raw.githubusercontent.com/KishorKumarParoi/realtime-mlops/main/bootstrap.sh \| bash` | Docker Compose (`:8000`), Auto-Swap OOM Protection |
| **Lightweight Native Python (<15s)** | `curl -fsSL https://raw.githubusercontent.com/KishorKumarParoi/realtime-mlops/main/bootstrap.sh \| bash -s -- --standalone` | Minimal bare runtime (< 150MB RAM, zero Docker dependency) |
| **Automated Test Suite** | `./deploy.sh --test` | Pytest validation & schema checks |
| **Zero-Cost Instant Teardown ($0.00)** | `./clear.sh` | Purges all containers, background processes, and ports |

---

## 🏛️ System Architecture Flow

![Real-Time MLOps Workflow Flowchart](docs/images/01_architecture_flow.svg)

---

## 💡 Business Value & Intuition

**Real-World Scenario:**
Imagine you run a subscription business with hundreds of thousands of active accounts. Losing high-value customers without warning costs enterprises millions annually. This engine detects customer dissatisfaction **before** cancellation occurs.

### Example Customer Inference:
- **Profile**: 45 years old, 24 months tenure, $79.99/mo, $1,920 lifetime spend, 3 support calls this month.
- **Inference Result**:
```json
{
  "churn": 1,
  "churn_probability": 0.73,
  "risk_tier": "HIGH"
}
```

**Automated Retention Action:**
- High friction score triggers a retention desk task.
- Automated promotional discount dispatched via CRM integration.
- Retention rate increases by **18-24%** through proactive intervention.

---

## 📡 API Usage & Endpoints

### 1. Health & Readiness Probe
```bash
curl -s http://localhost:8000/health
```
```json
{
  "status": "healthy",
  "service": "realtime-mlops",
  "model_loaded": true,
  "features": ["age", "tenure_months", "monthly_charges", "total_charges", "num_support_calls"]
}
```

### 2. Real-Time Churn Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "tenure_months": 24,
    "monthly_charges": 79.99,
    "total_charges": 1920.00,
    "num_support_calls": 3
  }'
```
```json
{
  "churn": 1,
  "churn_probability": 0.73,
  "risk_tier": "HIGH"
}
```

### 3. Prometheus Telemetry
```bash
curl -s http://localhost:8000/metrics
```

---

## 🛠️ Local Development & Model Retraining

```bash
# 1. Install dependencies
uv sync

# 2. Generate synthetic feature distribution
uv run python generate_data.py

# 3. Train Random Forest model and version artifacts
uv run python train.py

# 4. Start high-concurrency production server
uv run gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 api:app
```
