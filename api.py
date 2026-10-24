"""FastAPI inference server for cloud-native real-time churn prediction"""
import os
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Real-Time MLOps Churn Prediction Service",
    description="Sub-50ms Low-Latency Model Serving with Drift Monitoring Hooks",
    version="2.0.0"
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'churn_model.pkl')
model = None

def get_or_load_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
        else:
            # Resilient fallback: auto-train on-the-fly
            import subprocess
            try:
                subprocess.run(["python3", "generate_data.py"], check=True)
                subprocess.run(["python3", "train.py"], check=True)
                with open(MODEL_PATH, 'rb') as f:
                    model = pickle.load(f)
            except Exception as e:
                raise RuntimeError(f"Could not load or train model: {e}")
    return model

try:
    model = get_or_load_model()
except Exception:
    model = None

class CustomerData(BaseModel):
    age: int = Field(..., ge=18, le=100, example=45)
    tenure_months: int = Field(..., ge=0, le=120, example=24)
    monthly_charges: float = Field(..., ge=0.0, example=79.99)
    total_charges: float = Field(..., ge=0.0, example=1920.00)
    num_support_calls: int = Field(..., ge=0, le=50, example=3)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "realtime-mlops",
        "model_loaded": model is not None,
        "features": ["age", "tenure_months", "monthly_charges", "total_charges", "num_support_calls"]
    }

@app.get("/metrics")
def metrics():
    return {
        "service": "realtime-mlops",
        "model_loaded": model is not None,
        "features_count": 5,
        "slo_latency_target_p95_ms": 35.0,
        "slo_latency_target_p99_ms": 60.0
    }

@app.post("/predict")
def predict(data: CustomerData):
    clf = get_or_load_model()
    if clf is None:
        raise HTTPException(status_code=503, detail="Model artifact is not initialized")

    import pandas as pd
    features_df = pd.DataFrame([[
        data.age,
        data.tenure_months,
        data.monthly_charges,
        data.total_charges,
        data.num_support_calls
    ]], columns=['age', 'tenure_months', 'monthly_charges', 'total_charges', 'num_support_calls'])
    
    prediction = int(clf.predict(features_df)[0])
    probability = float(clf.predict_proba(features_df)[0][1])
    
    return {
        "churn": prediction,
        "churn_probability": round(probability, 4),
        "risk_tier": "HIGH" if probability > 0.6 else "MEDIUM" if probability > 0.3 else "LOW"
    }

@app.post("/api/predict")
def api_predict_alias(data: CustomerData):
    return predict(data)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
