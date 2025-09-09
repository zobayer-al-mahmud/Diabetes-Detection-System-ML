#!/usr/bin/env python3
"""
FastAPI Server for Diabetes Prediction
Provides endpoints for health check, metrics, and predictions using the best trained model.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import joblib
import json
import numpy as np
from pathlib import Path

app = FastAPI(title="Diabetes Prediction API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "*"],  # Allow frontend and dev access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and metadata
best_model = None
metadata = None
FEATURE_ORDER = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

class PredictionRequest(BaseModel):
    """Request model for predictions - all fields optional to handle missing values."""
    Pregnancies: Optional[float] = None
    Glucose: Optional[float] = None
    BloodPressure: Optional[float] = None
    SkinThickness: Optional[float] = None
    Insulin: Optional[float] = None
    BMI: Optional[float] = None
    DiabetesPedigreeFunction: Optional[float] = None
    Age: Optional[float] = None

class PredictionResponse(BaseModel):
    """Response model for predictions."""
    best_model: str
    prob: float
    label: str

@app.on_event("startup")
async def load_model_and_metadata():
    """Load the best model and metadata on startup."""
    global best_model, metadata
    
    try:
        model_dir = Path(__file__).parent / "model"
        
        # Load metadata
        meta_path = model_dir / "meta.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {meta_path}")
        
        with open(meta_path, 'r') as f:
            metadata = json.load(f)
        
        # Load best model
        best_model_path = model_dir / "best_model.pkl"
        if not best_model_path.exists():
            raise FileNotFoundError(f"Best model file not found: {best_model_path}")
        
        best_model = joblib.load(best_model_path)
        
        print(f"Loaded best model: {metadata['model_names'][metadata['best_model_name']]}")
        print("API server ready!")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if best_model is None or metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "ok": True,
        "best_model": metadata["model_names"][metadata["best_model_name"]]
    }

@app.get("/metrics")
async def get_metrics():
    """Get model evaluation metrics."""
    if metadata is None:
        raise HTTPException(status_code=503, detail="Metadata not loaded")
    
    return metadata

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction using the best model."""
    if best_model is None or metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert request to feature array
        feature_values = []
        for feature_name in FEATURE_ORDER:
            value = getattr(request, feature_name)
            # Convert None to NaN for proper handling by the imputer
            feature_values.append(float(value) if value is not None else np.nan)
        
        # Reshape for prediction (single sample)
        X = np.array(feature_values).reshape(1, -1)
        
        # Get prediction probability
        prob = best_model.predict_proba(X)[0, 1]  # Probability of positive class (diabetes)
        
        # Get prediction label (threshold = 0.5)
        label = "Positive" if prob >= 0.5 else "Negative"
        
        return PredictionResponse(
            best_model=metadata["model_names"][metadata["best_model_name"]],
            prob=float(prob),
            label=label
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Diabetes Prediction API",
        "endpoints": {
            "health": "/health - Check API health and best model",
            "metrics": "/metrics - Get model evaluation metrics",
            "predict": "/predict - Make diabetes prediction (POST)"
        },
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)