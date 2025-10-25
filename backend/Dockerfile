# ============================================
# Backend Dockerfile (FastAPI for Render)
# ============================================
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/ .

# Render dynamically assigns PORT, so we don't hardcode 8000
ENV PORT=8000

# Start the app using Render's PORT variable with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
