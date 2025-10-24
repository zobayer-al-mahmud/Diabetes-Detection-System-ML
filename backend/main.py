"""
FastAPI Backend with CORS Configuration
Supports dynamic frontend origin from environment variable
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(title="Monorepo Backend API")

# ============================================
# CORS Configuration for Frontend
# ============================================
# Get frontend URL from environment (set by Render)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Allow the frontend to make requests
origins = [
    FRONTEND_URL,
    "http://localhost:5173",  # Local Vite dev server
    "http://localhost:3000",  # Alternative local port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Request/Response Models
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
    """Root endpoint"""
    return {
        "message": "FastAPI Backend is running",
        "docs": "/docs",
        "frontend_url": FRONTEND_URL
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Backend API is running",
        "frontend_url": FRONTEND_URL
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(data: PredictionRequest):
    """
    Diabetes risk prediction endpoint
    Replace this with your actual ML model logic
    """
    try:
        # Example calculation (replace with your actual model)
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
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get some statistics"""
    return {
        "total_predictions": 1234,
        "average_risk": 45.6,
        "high_risk_count": 567
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
