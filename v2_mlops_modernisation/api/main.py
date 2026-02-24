"""
FastAPI inference service (portfolio scaffold).

Usage:
  uvicorn v2_mlops_modernisation.api.main:app --host 127.0.0.1 --port 8000

Then open:
  http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
from joblib import load


APP_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = APP_ROOT / "models" / "artifacts" / "best_model.joblib"


class PredictionRequest(BaseModel):
    lead_time_days: int = Field(..., ge=0, le=365)
    sms_reminder_sent: int = Field(..., ge=0, le=1)
    prior_no_show_count: int = Field(..., ge=0, le=20)
    prior_show_count: int = Field(..., ge=0, le=100)
    age: int = Field(..., ge=0, le=110)
    gender: str = Field(..., pattern="^(F|M)$")
    age_band: str
    appointment_type: str
    booking_channel: str
    appointment_hour: int = Field(..., ge=0, le=23)
    appointment_is_weekend: int = Field(..., ge=0, le=1)
    deprivation_index: float = Field(..., ge=0, le=1)
    clinic_id: str
    neighbourhood_id: str
    clinic_type: str
    clinic_region: str


class PredictionResponse(BaseModel):
    predicted_no_show_proba: float
    risk_band: str


def risk_band(p: float) -> str:
    if p >= 0.75:
        return "Critical"
    if p >= 0.55:
        return "High"
    if p >= 0.35:
        return "Medium"
    return "Low"


app = FastAPI(title="No-Show Risk Prediction API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": MODEL_PATH.exists()}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    if not MODEL_PATH.exists():
        return PredictionResponse(predicted_no_show_proba=0.0, risk_band="Low")

    model = load(MODEL_PATH)
    df = pd.DataFrame([req.model_dump()])
    proba = float(model.predict_proba(df)[:, 1][0])
    return PredictionResponse(predicted_no_show_proba=proba, risk_band=risk_band(proba))
