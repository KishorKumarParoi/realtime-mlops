# Churn Model MLOps Demo

A simple demonstration of MLOps practices for a customer churn prediction model.

## What Does This Model Do?

**Real-World Example:**

Imagine you run a telecom company with thousands of customers. Some customers are happy and stay for years, while others leave (churn) after a few months. This model predicts which customers are likely to leave.

**Example Customer:**
- **Sarah** is 45 years old
- Been a customer for 24 months
- Pays $79.99/month
- Total spent: $1,920
- Called customer support 3 times this month

**Model Prediction:**
```json
{
  "churn": 1,
  "churn_probability": 0.73
}
```

**Translation:** Sarah has a **73% chance of canceling her subscription**. Why? She's calling support frequently (unhappy) and paying relatively high fees. Your business can now:
- Offer her a discount
- Reach out with personalized support
- Prevent losing her before she leaves

**The model looks at patterns** like:
- High monthly charges → More likely to churn
- More support calls → Customer is frustrated
- Low tenure → Haven't built loyalty yet

This helps businesses **save customers proactively** instead of reacting after they've already left!

## Project Structure

```
churn-model/
├── generate_data.py          # Generate synthetic churn dataset
├── train.py                   # Train the model
├── api.py                     # FastAPI inference server
├── pyproject.toml             # Project metadata and dependencies

```

## 1. Initial Setup

```bash
# Install dependencies
uv sync

# Generate dataset
uv run generate_data.py

# Train model
uv run train.py

# Test API locally
uv run api.py
# Visit http://localhost:8000/docs

# Run with Gunicorn and Uvicorn workers
uv run gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000 api:app
```

## API Usage

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

Response:
```json
{
  "churn": 1,
  "churn_probability": 0.73
}
```
## 🚀 Zero-Touch Instant Cloud & Workstation Deployment

Deploy this platform on **any fresh EC2 instance, cloud VM, or local machine with a single terminal command**:

```bash
curl -fsSL https://raw.githubusercontent.com/KishorKumarParoi/realtime-mlops/main/bootstrap.sh | bash
```

### 🆘 One-Click Link For Whom It Is Not Working (Zero-Docker Standalone Mode)
If Docker is not running or permissions are restricted, run this instant fail-safe native command:
```bash
curl -fsSL https://raw.githubusercontent.com/KishorKumarParoi/realtime-mlops/main/bootstrap.sh | bash -s -- --standalone
```

### 🧹 Zero-Cost Instant Teardown ($0.00/hr):
```bash
./clear.sh
```
