# 🏥 Diabetes Detection System

A full-stack web application for predicting diabetes risk using machine learning. Built with FastAPI backend and React frontend, deployed on Render using Docker containers.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://diabetes-detection-system-frontend.onrender.com)
[![Backend API](https://img.shields.io/badge/API-active-blue)](https://diabetes-detection-system-ml.onrender.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🌟 Live Application

- **Frontend:** [https://diabetes-detection-system-frontend.onrender.com](https://diabetes-detection-system-frontend.onrender.com)
- **Backend API:** [https://diabetes-detection-system-ml.onrender.com](https://diabetes-detection-system-ml.onrender.com)
- **API Documentation:** [https://diabetes-detection-system-ml.onrender.com/docs](https://diabetes-detection-system-ml.onrender.com/docs)

---

## � Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Local Development](#-local-development)
- [Docker Deployment](#-docker-deployment)
- [Render Deployment](#-render-deployment)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### 🎯 Core Functionality
- **Risk Prediction:** Calculates diabetes risk based on glucose, insulin, BMI, and age
- **Real-time Results:** Instant prediction with risk percentage
- **Responsive Design:** Works seamlessly on desktop, tablet, and mobile devices
- **Educational Tool:** Disclaimer that this is for educational purposes only

### 🔧 Technical Features
- **RESTful API:** FastAPI backend with automatic OpenAPI documentation
- **CORS Configuration:** Secure cross-origin resource sharing
- **Docker Containerization:** Consistent deployment across environments
- **Runtime Configuration:** Environment variables injected at container startup
- **Health Checks:** Built-in health monitoring endpoints
- **Modern UI:** Glass morphism design with smooth animations
- **Error Handling:** User-friendly error messages and loading states

---

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn (ASGI server)
- **Validation:** Pydantic 2.5.0
- **Language:** Python 3.11
- **Container:** Docker with Python 3.11-slim base image

### Frontend
- **Framework:** React 18.2.0
- **Build Tool:** Vite 5.0.0
- **Styling:** Custom CSS with glass morphism effects
- **HTTP Client:** Fetch API
- **Server:** Nginx Alpine (production)
- **Container:** Multi-stage Docker build (Node 20 + Nginx)

### DevOps
- **Containerization:** Docker & Docker Compose
- **Deployment:** Render.com (free tier)
- **CI/CD:** Automatic deployment on git push
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
Diabetes-Detection-System/
├── render.yaml                 # Render Blueprint configuration
├── docker-compose.yml          # Local Docker orchestration
├── README.md                   # Project documentation
│
├── backend/                    # FastAPI Backend
│   ├── Dockerfile             # Backend Docker image
│   ├── .dockerignore          # Docker ignore patterns
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React Frontend
│   ├── Dockerfile             # Frontend multi-stage build
│   ├── .dockerignore          # Docker ignore patterns
│   ├── nginx.conf.template    # Nginx configuration
│   ├── docker-entrypoint.sh   # Runtime config injection
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── index.html             # HTML entry point
│   ├── public/
│   │   └── config.js.template # Runtime API URL template
│   └── src/
│       ├── main.jsx           # React entry point
│       ├── App.jsx            # Main component
│       ├── App.css            # Component styles
│       └── index.css          # Global styles
│
├── model/                      # ML Model artifacts
│   └── meta.json              # Model metadata
│
└── data/                       # Dataset
    └── diabetes.csv           # Training data
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **Docker & Docker Compose** (optional, for containerized development)
- **Git**

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zobayer-al-mahmud/Diabetes-Detection-System-ML.git
   cd Diabetes-Detection-System-ML
   ```

2. **Choose your development method:**
   - [Local Development](#-local-development) - Run services directly
   - [Docker Development](#-docker-deployment) - Use Docker containers

---

## 💻 Local Development

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend will be available at:** http://localhost:5173

### Test the Application

1. Open http://localhost:5173 in your browser
2. Enter sample values:
   - Glucose: 120 mg/dL
   - Insulin: 80 µU/mL
   - BMI: 25 kg/m²
   - Age: 30 years
3. Click **"PREDICT"** to see results

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Frontend: http://localhost
- Backend: http://localhost:8000

### Manual Docker Build

#### Backend:
```bash
cd backend
docker build -t diabetes-backend .
docker run -p 8000:8000 -e FRONTEND_URL=http://localhost diabetes-backend
```

#### Frontend:
```bash
cd frontend
docker build -t diabetes-frontend .
docker run -p 80:80 -e API_BASE_URL=http://localhost:8000 diabetes-frontend
```

---

## ☁️ Render Deployment

### Automatic Deployment (Recommended)

1. **Fork/Clone this repository to your GitHub account**

2. **Go to [Render Dashboard](https://dashboard.render.com/)**

3. **Create New Blueprint:**
   - Click **"Blueprints"** → **"New Blueprint Instance"**
   - Connect your GitHub repository
   - Render will detect `render.yaml` automatically

4. **Deploy:**
   - Click **"Apply"**
   - Wait 5-10 minutes for Docker builds to complete

5. **Access your deployment:**
   - Frontend: `https://diabetes-detection-system-frontend.onrender.com`
   - Backend: `https://diabetes-detection-system-ml.onrender.com`

### Manual Deployment

#### Deploy Backend:
1. New Web Service → Connect Repository
2. Configure:
   - **Name:** `diabetes-backend`
   - **Environment:** Docker
   - **Dockerfile Path:** `./backend/Dockerfile`
   - **Health Check Path:** `/health`
3. Deploy

#### Deploy Frontend:
1. New Web Service → Connect Repository
2. Configure:
   - **Name:** `diabetes-frontend`
   - **Environment:** Docker
   - **Dockerfile Path:** `./frontend/Dockerfile`
3. Add Environment Variable:
   - **Key:** `API_BASE_URL`
   - **Value:** Your backend URL from step 1
4. Deploy

---

## 🔌 API Endpoints

### Base URL
```
Production: https://diabetes-detection-system-ml.onrender.com
Local: http://localhost:8000
```

### Endpoints

#### `GET /`
**Description:** Root endpoint with API information

**Response:**
```json
{
  "message": "FastAPI backend is running 🚀",
  "docs": "/docs",
  "frontend_url": "https://diabetes-detection-system-frontend.onrender.com"
}
```

#### `GET /health`
**Description:** Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "message": "Backend API is live",
  "frontend_url": "https://diabetes-detection-system-frontend.onrender.com"
}
```

#### `POST /api/predict`
**Description:** Predict diabetes risk based on health metrics

**Request Body:**
```json
{
  "glucose": 120.0,
  "insulin": 80.0,
  "bmi": 25.5,
  "age": 30
}
```

**Response:**
```json
{
  "prediction": "Low Risk",
  "risk_percentage": 45.25,
  "input_data": {
    "glucose": 120.0,
    "insulin": 80.0,
    "bmi": 25.5,
    "age": 30
  }
}
```

#### `GET /api/stats`
**Description:** Get mock statistics (demo endpoint)

**Response:**
```json
{
  "total_predictions": 1234,
  "average_risk": 45.6,
  "high_risk_count": 567
}
```

### Interactive API Documentation

Visit `/docs` endpoint for Swagger UI:
- Production: https://diabetes-detection-system-ml.onrender.com/docs
- Local: http://localhost:8000/docs

---

## 🔐 Environment Variables

### Backend (`backend/.env`)

```env
# Environment
ENV=production

# Frontend URL (for CORS)
FRONTEND_URL=https://diabetes-detection-system-frontend.onrender.com

# Server Port (Render provides this)
PORT=8000
```

### Frontend (`frontend/.env`)

```env
# Backend API URL
API_BASE_URL=https://diabetes-detection-system-ml.onrender.com

# Nginx Port (Render provides this)
PORT=80
```

**Note:** On Render, these are automatically injected via `render.yaml` using the `fromService` configuration.

---

## 📸 Screenshots

### Home Page / Prediction Form
![Diabetes Detection System Interface](assets/screenshot-home.png)

### Prediction Result - Low Risk
![Low Risk Result](assets/screenshot-low-risk.png)

### Prediction Result - High Risk
![High Risk Result](assets/screenshot-high-risk.png)

### API Documentation (Swagger UI)
![API Docs](assets/screenshot-api-docs.png)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes:**
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow existing code style
- Write meaningful commit messages
- Update documentation for new features
- Add tests for new functionality
- Ensure Docker builds succeed

---

## 🐛 Known Issues

- **Free Tier Limitations:** Render's free tier may experience cold starts (initial load can take 30-60 seconds)
- **Demo Algorithm:** Current risk calculation uses a simple weighted formula, not a trained ML model
- **Educational Only:** This is not a medical diagnostic tool

---

## 📝 Future Enhancements

- [ ] Integrate actual ML model (Random Forest/XGBoost)
- [ ] Add user authentication and prediction history
- [ ] Implement data visualization (charts/graphs)
- [ ] Add more health metrics (blood pressure, cholesterol)
- [ ] Create mobile app (React Native)
- [ ] Add multilingual support
- [ ] Implement PDF report generation
- [ ] Add unit and integration tests
- [ ] Set up CI/CD pipeline with GitHub Actions

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Zobayer Al Mahmud**

- GitHub: [@zobayer-al-mahmud](https://github.com/zobayer-al-mahmud)
- LinkedIn: [Zobayer Al Mahmud](https://linkedin.com/in/zobayer-al-mahmud)
- Email: zobayer.mahmud@example.com

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **React** - JavaScript library for building user interfaces
- **Render** - Cloud platform for deploying applications
- **Vite** - Next generation frontend tooling
- **Nginx** - High-performance HTTP server

---

## ⭐ Support

If you find this project helpful, please give it a ⭐ on GitHub!

**Educational Demo Only - Not for Medical Use**

© 2025 Developed by Zobayer Al Mahmud

## 📁 Project Structure

```
monorepo-example/
├── render.yaml                 # Render Blueprint (deploys both services)
├── backend/
│   ├── Dockerfile             # Backend Docker image
│   ├── .dockerignore
│   ├── main.py                # FastAPI application with CORS
│   └── requirements.txt       # Python dependencies
└── frontend/
    ├── Dockerfile             # Frontend Docker image (multi-stage)
    ├── .dockerignore
    ├── docker-entrypoint.sh   # Runtime config injection script
    ├── nginx.conf.template    # Nginx configuration
    ├── package.json           # Node.js dependencies
    ├── vite.config.js         # Vite configuration
    ├── index.html             # HTML entry point
    ├── public/
    │   └── config.js.template # Runtime API URL template
    └── src/
        ├── main.jsx           # React entry point
        ├── App.jsx            # Main React component
        ├── App.css            # Component styles
        └── index.css          # Global styles
```

---

## 🎯 Key Features

### ✅ Backend (FastAPI)
- **CORS middleware** configured to allow frontend domain
- Dynamic `FRONTEND_URL` from environment variable
- Health check endpoint at `/health`
- Example prediction API at `/api/predict`
- Docker containerized with Python 3.11

### ✅ Frontend (React + Vite)
- **Runtime API URL injection** (no rebuild needed for different environments)
- Nginx serves static files with proper caching
- Multi-stage Docker build (build + production)
- Responsive UI with gradient design
- Connects to backend API dynamically

### ✅ Render Deployment
- **Single `render.yaml`** for both services
- **`fromService` injection** - backend URL automatically passed to frontend
- **`rootDir`** for monorepo subfolder deployment
- **Free tier** plans configured by default
- Auto-deploy on git push

---

## 🚀 Deployment Steps

### Option 1: Deploy via Render Blueprint (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial monorepo setup"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Go to Render Dashboard:**
   - Navigate to: https://dashboard.render.com/
   - Click **"Blueprints"** → **"New Blueprint Instance"**

3. **Connect your repository:**
   - Select your GitHub repository
   - Render will automatically detect `render.yaml`

4. **Deploy:**
   - Click **"Apply"**
   - Render will deploy both services simultaneously
   - Wait 5-10 minutes for Docker builds

5. **Access your application:**
   - Backend: `https://diabetes-backend-xxxx.onrender.com`
   - Frontend: `https://diabetes-frontend-xxxx.onrender.com`

### Option 2: Manual Deployment

#### Deploy Backend First:
1. Go to Render Dashboard → **"New Web Service"**
2. Connect your repository
3. Configure:
   - **Name:** `diabetes-backend`
   - **Environment:** Docker
   - **Root Directory:** `backend`
   - **Dockerfile Path:** `./Dockerfile`
   - **Plan:** Free
4. Click **"Create Web Service"**

#### Deploy Frontend Second:
1. Go to Render Dashboard → **"New Web Service"**
2. Connect your repository
3. Configure:
   - **Name:** `diabetes-frontend`
   - **Environment:** Docker
   - **Root Directory:** `frontend`
   - **Dockerfile Path:** `./Dockerfile`
   - **Plan:** Free
4. Add environment variable:
   - **Key:** `API_BASE_URL`
   - **Value:** `https://diabetes-backend-xxxx.onrender.com` (your backend URL)
5. Click **"Create Web Service"**

---

## 🔧 Local Development

### Backend (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Frontend (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will be available at: http://localhost:5173

**Note:** Update the fallback API URL in `frontend/src/App.jsx` if needed:
```javascript
const API_BASE_URL = window.ENV_CONFIG?.API_BASE_URL || 'http://localhost:8000';
```

---

## 🐳 Docker Testing Locally

### Test Backend:
```bash
cd backend
docker build -t diabetes-backend .
docker run -p 8000:8000 -e FRONTEND_URL=http://localhost:80 diabetes-backend
```

### Test Frontend:
```bash
cd frontend
docker build -t diabetes-frontend .
docker run -p 80:80 -e API_BASE_URL=http://localhost:8000 diabetes-frontend
```

### Test Full Stack with Docker Compose:
Create `docker-compose.yml` in the root:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - FRONTEND_URL=http://localhost:80

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    environment:
      - API_BASE_URL=http://localhost:8000
    depends_on:
      - backend
```

Run:
```bash
docker-compose up --build
```

---

## 🔑 How Runtime Config Injection Works

### Problem:
React builds create static files. Environment variables are baked in at build time, making it impossible to change the API URL without rebuilding.

### Solution:
1. **`config.js.template`** contains placeholder:
   ```javascript
   window.ENV_CONFIG = {
     API_BASE_URL: '${API_BASE_URL}'
   };
   ```

2. **`docker-entrypoint.sh`** runs at container startup and replaces `${API_BASE_URL}` with the actual value from the environment variable:
   ```bash
   envsubst '${API_BASE_URL}' < /usr/share/nginx/html/config.js.template > /usr/share/nginx/html/config.js
   ```

3. **`index.html`** loads `config.js` before the React app:
   ```html
   <script src="/config.js"></script>
   <script type="module" src="/src/main.jsx"></script>
   ```

4. **`App.jsx`** reads the injected value:
   ```javascript
   const API_BASE_URL = window.ENV_CONFIG?.API_BASE_URL || 'http://localhost:8000';
   ```

This allows the same Docker image to work in any environment! 🎉

---

## 🔒 CORS Configuration

The backend's CORS middleware is configured in `backend/main.py`:

```python
# Get frontend URL from environment
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

origins = [
    FRONTEND_URL,
    "http://localhost:5173",  # Local dev
    "http://localhost:3000",  # Alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**On Render:** The `FRONTEND_URL` is automatically set via `fromService` in `render.yaml`.

---

## 📊 Monitoring & Debugging

### Check Health Endpoints:

**Backend:**
```bash
curl https://diabetes-backend-xxxx.onrender.com/health
```

**Frontend:**
```bash
curl https://diabetes-frontend-xxxx.onrender.com/health
```

### View Logs:
- Go to Render Dashboard
- Click on each service
- Navigate to **"Logs"** tab

### Common Issues:

1. **CORS errors:**
   - Verify `FRONTEND_URL` environment variable in backend
   - Check browser console for exact error

2. **API URL not injected:**
   - Check frontend logs for entrypoint script output
   - Verify `API_BASE_URL` environment variable
   - View generated `/config.js` in browser

3. **Container crashes:**
   - Check logs for build errors
   - Verify Dockerfile paths
   - Ensure health check endpoints return 200

---

## 🎨 Customization

### Update Backend Logic:
Edit `backend/main.py` → Add your ML model, database connections, etc.

### Update Frontend UI:
Edit `frontend/src/App.jsx` and `frontend/src/App.css` → Customize design and functionality

### Add Database:
1. Add a database service in `render.yaml`:
   ```yaml
   databases:
     - name: postgres-db
       databaseName: mydb
       user: myuser
       plan: free
   ```

2. Add environment variable to backend:
   ```yaml
   - key: DATABASE_URL
     fromDatabase:
       name: postgres-db
       property: connectionString
   ```

### Add Redis Cache:
```yaml
- type: redis
  name: redis-cache
  plan: free
  maxmemoryPolicy: allkeys-lru
```

---

## 📦 Production Checklist

- [x] Docker health checks configured
- [x] CORS properly configured
- [x] Environment variables set via `fromService`
- [x] Nginx caching rules configured
- [x] Security headers added
- [x] Multi-stage Docker builds for frontend
- [ ] Add authentication/authorization
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure custom domain
- [ ] Set up CI/CD pipeline
- [ ] Add rate limiting
- [ ] Implement logging

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📄 License

MIT License - feel free to use this template for your projects!

---

## 🙏 Support

If you find this helpful, please ⭐ star the repository!

**Happy Deploying! 🚀**
