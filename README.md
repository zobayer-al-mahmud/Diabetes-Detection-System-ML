# Diabetes Prediction Web App

A full-stack web application for diabetes risk prediction using machine learning. The app features a glass morphism UI design and automatically selects the best performing model from multiple trained algorithms.

![Diabetes Predictor](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20JS-yellow)

## 🎯 Features

- **Machine Learning Pipeline**: Trains and evaluates 4 different models (Logistic Regression, KNN, Decision Tree, Random Forest)
- **Automatic Model Selection**: Chooses the best model based on accuracy with intelligent tie-breaking
- **Glass Morphism UI**: Modern, responsive design with purple-to-blue gradient background
- **Real-time Predictions**: Fast API responses with probability scores and risk labels
- **Data Preprocessing**: Handles missing values with median imputation
- **Comprehensive Metrics**: Confusion Matrix, Precision, Recall, F1-Score for all models

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

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd diabetes-web/backend
   pip install -r requirements.txt
   ```

2. **Train Models**
   ```bash
   python train_export.py
   ```
   This will:
   - Load and preprocess the diabetes dataset
   - Train 4 different ML models with proper pipelines
   - Evaluate each model on the test set
   - Automatically select the best model by accuracy
   - Save all models and metadata

3. **Start API Server**
   ```bash
   uvicorn server:app --reload --port 8000
   ```
   Server will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to Frontend**
   ```bash
   cd diabetes-web/frontend/public
   ```

2. **Start Development Server**
   ```bash
   python -m http.server 5500
   ```
   Frontend will be available at: `http://localhost:5500`

3. **Open in Browser**
   Visit `http://localhost:5500` to use the application

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
  "label": "Positive"
}
```

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

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the console for error messages
2. Verify all dependencies are installed correctly
3. Ensure both backend and frontend servers are running
4. Check that the model files were generated successfully

---

**Built with ❤️ for educational purposes**