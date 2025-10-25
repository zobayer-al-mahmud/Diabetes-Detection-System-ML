"""
FastAPI Backend with CORS Configuration
Supports dynamic frontend origin from environment variable (Render-ready)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

# ============================================
# FastAPI App Initialization
# ============================================
app = FastAPI(title="Diabetes Detection Backend API")

# ============================================
# Dynamic Frontend CORS Configuration
# ============================================
# Render injects FRONTEND_URL automatically from render.yaml
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Allow multiple origins for dev and production
origins = [
    FRONTEND_URL,
    "http://localhost:5173",  # local dev
    "http://localhost:3000",  # alt local dev
    "http://localhost",  # local dev nginx
    "https://diabetes-detection-system-frontend.onrender.com",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Pydantic Models
# ============================================
class HealthResponse(BaseModel):
    status: str
    message: str
    frontend_url: Optional[str]


class PredictionRequest(BaseModel):
    glucose: float
    insulin: float
    bmi: float
    age: int


class PredictionResponse(BaseModel):
    prediction: str
    risk_percentage: float
    input_data: dict


# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """Root route"""
    return {
        "message": "FastAPI backend is running 🚀",
        "docs": "/docs",
        "frontend_url": FRONTEND_URL
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Render"""
    return {
        "status": "healthy",
        "message": "Backend API is live",
        "frontend_url": FRONTEND_URL
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(data: PredictionRequest):
    """
    Diabetes risk prediction (demo logic).
    Replace this with your ML model inference.
    """
    try:
        # Dummy weighted risk calculation
        risk_score = (
            (data.glucose * 0.3) +
            (data.insulin * 0.2) +
            (data.bmi * 0.3) +
            (data.age * 0.2)
        ) / 100

        risk_percentage = min(risk_score * 10, 99.9)
        prediction = "High Risk" if risk_percentage > 50 else "Low Risk"

        return {
            "prediction": prediction,
            "risk_percentage": round(risk_percentage, 2),
            "input_data": {
                "glucose": data.glucose,
                "insulin": data.insulin,
                "bmi": data.bmi,
                "age": data.age
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Mock statistics route"""
    return {
        "total_predictions": 1234,
        "average_risk": 45.6,
        "high_risk_count": 567
    }


# ============================================
# Local Development Entry Point
# ============================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
