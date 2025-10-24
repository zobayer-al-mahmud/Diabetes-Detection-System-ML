# Diabetes Prediction Web App

A full-stack web application for diabetes risk prediction using machine learning. The app features a glass morphism UI design, Redis caching, and is production-ready with Docker support.

![Diabetes Predictor](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D)

## 🎯 Features

- **Machine Learning Pipeline**: Trains and evaluates 4 different models (Logistic Regression, KNN, Decision Tree, Random Forest)
- **Automatic Model Selection**: Chooses the best model based on accuracy with intelligent tie-breaking
- **Redis Caching**: Fast predictions with 24-hour cache, metrics cached for 1 hour
- **Docker Support**: Multi-stage Dockerfile and Docker Compose for easy deployment
- **Render Ready**: One-click deployment to Render with free tier support
- **Glass Morphism UI**: Modern, responsive design with purple-to-blue gradient background
- **Real-time Predictions**: Fast API responses with probability scores and risk labels
- **Data Preprocessing**: Handles missing values with median imputation
- **Comprehensive Metrics**: Confusion Matrix, Precision, Recall, F1-Score for all models
- **Production Grade**: Gunicorn + Uvicorn ASGI server, health checks, logging

## 📁 Project Structure

```
diabetes-web/
├── README.md
├── backend/
│   ├── data/
│   │   └── diabetes.csv           # Training dataset
│   ├── model/
│   │   ├── lr.pkl                 # Trained Logistic Regression
│   │   ├── knn.pkl                # Trained K-Nearest Neighbors
│   │   ├── dt.pkl                 # Trained Decision Tree
│   │   ├── rf.pkl                 # Trained Random Forest
│   │   ├── best_model.pkl         # Best performing model
│   │   └── meta.json              # Model metadata & metrics
│   ├── train_export.py            # Model training script
│   ├── server.py                  # FastAPI server
│   └── requirements.txt           # Python dependencies
└── frontend/
    └── public/
        ├── index.html             # Main HTML page
        ├── styles.css             # Glass morphism styling
        ├── app.js                 # Frontend JavaScript
        └── assets/                # Static assets
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

The fastest way to get started with all services:

```bash
# Start the application and Redis
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Access the API at http://localhost:8000
```

### Option 2: Local Development

#### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Redis (optional, for caching)

#### Backend Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis (Optional)**
   ```bash
   # Use Docker
   docker run -d -p 6379:6379 redis:7-alpine
   
   # Or install Redis locally and run
   redis-server
   ```

3. **Train Models**
   ```bash
   python train_export.py
   ```
   This will:
   - Load and preprocess the diabetes dataset
   - Train 4 different ML models with proper pipelines
   - Evaluate each model on the test set
   - Automatically select the best model by accuracy
   - Save all models and metadata

4. **Start API Server**
   ```bash
   # Development
   uvicorn server:app --reload --port 8000
   
   # Production
   gunicorn server:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```
   Server will be available at: `http://localhost:8000`

### Option 3: Deploy to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy**:
1. Push code to GitHub
2. Connect repository to Render
3. Render detects `render.yaml` and deploys automatically
4. Free tier includes Redis cache!

## 🐳 Docker Commands

### Build and Run
```bash
# Build image
docker build -t diabetes-prediction .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Testing
```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Glucose": 120, "BMI": 31.6, "Age": 45, "Insulin": 130}'
```

## 💾 Redis Caching

The application uses Redis for performance optimization:

- **Prediction Cache**: 24-hour TTL for identical predictions
- **Metrics Cache**: 1-hour TTL for model metrics
- **Graceful Fallback**: Works without Redis if unavailable
- **Cache Hit Indicator**: Response includes `"cached": true/false`

Check cache status:
```bash
curl http://localhost:8000/
# Returns: "cache_enabled": true/false
```

## 📖 Frontend Setup

The frontend is a standalone HTML/CSS/JS application:

1. **Open in Browser**
   ```bash
   # Simple HTTP server
   python -m http.server 5500
   
   # Or just open index.html in browser
   ```

2. **Update API URL** (if needed)
   Edit `app.js` and change:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000';
   ```

## 🔧 API Documentation

### Endpoints

#### `GET /health`
Check API health and get best model info.

**Response:**
```json
{
  "ok": true,
  "best_model": "Random Forest"
}
```

#### `GET /metrics`
Get detailed metrics for all trained models.

**Response:**
```json
{
  "feature_order": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
  "best_model_name": "rf",
  "model_names": {
    "lr": "Logistic Regression",
    "knn": "K-Nearest Neighbors", 
    "dt": "Decision Tree",
    "rf": "Random Forest"
  },
  "models": {
    "lr": {
      "confusion_matrix": {"TN": 94, "FP": 17, "FN": 23, "TP": 20},
      "accuracy": 0.7403,
      "precision": 0.5405,
      "recall": 0.4651,
      "f1_score": 0.5000
    }
    // ... other models
  }
}
```

#### `POST /predict`
Make a diabetes prediction.

**Request Body:**
```json
{
  "Glucose": 120,
  "Insulin": 130, 
  "BMI": 31.6,
  "Age": 45,
  "Pregnancies": null,
  "BloodPressure": null,
  "SkinThickness": null,
  "DiabetesPedigreeFunction": null
}
```

**Response:**
```json
{
  "best_model": "Random Forest",
  "prob": 0.82,
  "label": "Positive",
  "cached": false
}
```

### API Documentation (Interactive)

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 🧠 Machine Learning Details

### Models Trained

1. **Logistic Regression** (with scaling)
   - Pipeline: Median Imputer → Standard Scaler → Logistic Regression
   - Parameters: `max_iter=1000, random_state=42`

2. **K-Nearest Neighbors** (with scaling)  
   - Pipeline: Median Imputer → Standard Scaler → KNN
   - Parameters: `n_neighbors=11`

3. **Decision Tree** (without scaling)
   - Pipeline: Median Imputer → Decision Tree
   - Parameters: `random_state=42`

4. **Random Forest** (without scaling)
   - Pipeline: Median Imputer → Random Forest  
   - Parameters: `n_estimators=200, random_state=42`

### Data Preprocessing

- **Missing Value Handling**: Zeros in `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, and `BMI` are treated as missing values
- **Imputation**: Median imputation for all missing values
- **Scaling**: Applied only to Logistic Regression and KNN models
- **Train/Test Split**: 80/20 split with stratification (`random_state=42`)

### Model Selection Logic

1. **Primary**: Highest accuracy on test set
2. **Tie-breaker 1**: Higher precision for positive class
3. **Tie-breaker 2**: Higher recall for positive class

### Evaluation Metrics

For each model, the following metrics are calculated on the test set:
- **Confusion Matrix**: True Negatives, False Positives, False Negatives, True Positives
- **Accuracy**: Overall classification accuracy
- **Precision**: Precision for positive class (diabetes)
- **Recall**: Recall for positive class (diabetes) 
- **F1-Score**: F1-score for positive class (diabetes)

## 🎨 UI Design

The frontend features a modern glass morphism design:

- **Background**: Purple to blue gradient (`#36223b → #2b3351 → #0e3b5a`)
- **Glass Card**: Semi-transparent with backdrop blur and subtle borders
- **Responsive**: Works on desktop and mobile devices
- **Accessible**: Proper focus management and keyboard navigation
- **Interactive**: Smooth animations and hover effects

### Input Fields

The UI provides 4 main input fields matching the most important diabetes risk factors:
- **Glucose**: Blood glucose level
- **Insulin**: Insulin level  
- **BMI**: Body Mass Index
- **Age**: Patient age

All fields are optional - the model's imputer will handle missing values.

## 🧪 Testing

### Manual Testing

1. **Test Training Script**
   ```bash
   cd backend
   python train_export.py
   # Verify models are created in model/ directory
   ```

2. **Test API Endpoints**
   ```bash
   # Start server
   uvicorn server:app --reload --port 8000
   
   # Test health endpoint
   curl http://localhost:8000/health
   
   # Test prediction endpoint  
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"Glucose": 120, "BMI": 31.6, "Age": 45, "Insulin": 130}'
   ```

3. **Test Frontend**
   - Open `http://localhost:5500`
   - Fill in some health parameters
   - Click "Predict" 
   - Verify results display correctly

## 🔐 Security & Limitations

### Security Considerations
- CORS is configured for development (`localhost:5500` and `*`)
- For production, restrict CORS origins to your domain
- Consider adding rate limiting for the prediction endpoint
- Input validation is performed on both frontend and backend

### Medical Disclaimer
⚠️ **IMPORTANT**: This application is for educational and demonstration purposes only. It should not be used for actual medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals for medical advice.

### Model Limitations
- Trained on a limited dataset (768 samples)
- May not generalize to all populations
- Requires validation on larger, more diverse datasets for clinical use
- Missing values are imputed, which may affect prediction accuracy

## 📊 Dataset Information

The diabetes dataset contains 768 samples with the following features:
- **Pregnancies**: Number of pregnancies
- **Glucose**: Plasma glucose concentration  
- **BloodPressure**: Diastolic blood pressure (mm Hg)
- **SkinThickness**: Triceps skin fold thickness (mm)
- **Insulin**: 2-Hour serum insulin (mu U/ml)
- **BMI**: Body mass index (weight in kg/(height in m)^2)
- **DiabetesPedigreeFunction**: Diabetes pedigree function
- **Age**: Age in years
- **Outcome**: Diabetes diagnosis (0: No, 1: Yes)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## � Deployment

### Render (Recommended)

This project is optimized for Render deployment with free tier support:

1. **Push to GitHub**
2. **Connect to Render** and select your repository
3. **Render auto-detects** `render.yaml` configuration
4. **Two services deploy**:
   - Web Service (FastAPI app)
   - Redis Cache (free 25MB)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Other Platforms

- **Railway**: Use `Dockerfile` for deployment
- **Heroku**: Add `Procfile` (not included)
- **AWS/GCP/Azure**: Use Docker container
- **DigitalOcean**: App Platform with Dockerfile

### Environment Variables

Required for deployment:
- `REDIS_URL`: Redis connection string (auto-configured on Render)
- `PORT`: Application port (auto-configured on most platforms)

## �📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment troubleshooting
2. Review Docker logs: `docker-compose logs -f app`
3. Verify all dependencies are installed correctly
4. Check that Redis is running if caching is enabled
5. Ensure model files were generated successfully
6. Open an issue on GitHub

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Complete deployment guide for Docker and Render
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Redis Guide**: See caching section in DEPLOYMENT.md

---

**Built with ❤️ for educational purposes**