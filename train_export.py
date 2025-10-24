#!/usr/bin/env python3
"""
Diabetes Detection Training Script
Trains 4 models (LR, KNN, DT, RF), evaluates them, and selects the best one by accuracy.
"""

import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Feature order as specified
FEATURE_ORDER = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

def load_and_clean_data():
    """Load diabetes dataset and clean zeros as missing values for specific features."""
    print("Loading and cleaning dataset...")
    
    # Load data
    data_path = Path(__file__).parent / "data" / "diabetes.csv"
    df = pd.read_csv(data_path)
    
    print(f"Loaded dataset: {df.shape}")
    print(f"Features: {list(df.columns)}")
    
    # Features where 0 should be treated as missing
    zero_to_nan_features = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    
    # Replace zeros with NaN for specific features
    for feature in zero_to_nan_features:
        if feature in df.columns:
            df.loc[df[feature] == 0, feature] = np.nan
            missing_count = df[feature].isna().sum()
            print(f"  {feature}: {missing_count} values set to NaN")
    
    # Separate features and target
    X = df[FEATURE_ORDER]
    y = df["Outcome"]
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    return X, y

def create_model_pipelines():
    """Create the 4 model pipelines as specified."""
    pipelines = {}
    
    # Logistic Regression (scaled)
    pipelines['lr'] = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ])
    
    # KNN (scaled)
    pipelines['knn'] = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', KNeighborsClassifier(n_neighbors=11))
    ])
    
    # Decision Tree (unscaled)
    pipelines['dt'] = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('classifier', DecisionTreeClassifier(random_state=42))
    ])
    
    # Random Forest (unscaled)
    pipelines['rf'] = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('classifier', RandomForestClassifier(n_estimators=200, random_state=42))
    ])
    
    return pipelines

def evaluate_model(model, X_test, y_test):
    """Evaluate a trained model and return metrics."""
    # Get predictions and probabilities
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]  # Probability of positive class
    
    # Confusion matrix (TN, FP, FN, TP)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    
    # Calculate metrics for positive class (1)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)
    
    return {
        'confusion_matrix': {'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp)},
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }

def select_best_model(model_metrics):
    """Select best model by accuracy (tie-breakers: precision -> recall)."""
    best_model = None
    best_name = None
    best_accuracy = -1
    best_precision = -1
    best_recall = -1
    
    for name, metrics in model_metrics.items():
        accuracy = metrics['accuracy']
        precision = metrics['precision']
        recall = metrics['recall']
        
        is_better = False
        
        if accuracy > best_accuracy:
            is_better = True
        elif accuracy == best_accuracy:
            if precision > best_precision:
                is_better = True
            elif precision == best_precision:
                if recall > best_recall:
                    is_better = True
        
        if is_better:
            best_model = name
            best_name = name
            best_accuracy = accuracy
            best_precision = precision
            best_recall = recall
    
    return best_name

def main():
    """Main training pipeline."""
    print("=== Diabetes Detection Model Training ===\n")
    
    # Load and prepare data
    X, y = load_and_clean_data()
    
    # Split data
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Create pipelines
    pipelines = create_model_pipelines()
    
    # Train and evaluate models
    print("\nTraining and evaluating models...")
    trained_models = {}
    model_metrics = {}
    
    model_names = {
        'lr': 'Logistic Regression',
        'knn': 'K-Nearest Neighbors',
        'dt': 'Decision Tree',
        'rf': 'Random Forest'
    }
    
    for model_key, pipeline in pipelines.items():
        print(f"\nTraining {model_names[model_key]}...")
        
        # Train model
        pipeline.fit(X_train, y_train)
        trained_models[model_key] = pipeline
        
        # Evaluate model
        metrics = evaluate_model(pipeline, X_test, y_test)
        model_metrics[model_key] = metrics
        
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1-Score: {metrics['f1_score']:.4f}")
        print(f"  Confusion Matrix: TN={metrics['confusion_matrix']['TN']}, "
              f"FP={metrics['confusion_matrix']['FP']}, "
              f"FN={metrics['confusion_matrix']['FN']}, "
              f"TP={metrics['confusion_matrix']['TP']}")
    
    # Select best model
    best_model_name = select_best_model(model_metrics)
    print(f"\n=== Best Model Selected: {model_names[best_model_name]} ===")
    print(f"Accuracy: {model_metrics[best_model_name]['accuracy']:.4f}")
    
    # Save models
    print("\nSaving models...")
    model_dir = Path(__file__).parent / "model"
    
    # Save individual models
    for model_key, model in trained_models.items():
        model_path = model_dir / f"{model_key}.pkl"
        joblib.dump(model, model_path)
        print(f"  Saved {model_names[model_key]} to {model_path}")
    
    # Save best model
    best_model_path = model_dir / "best_model.pkl"
    joblib.dump(trained_models[best_model_name], best_model_path)
    print(f"  Saved best model ({model_names[best_model_name]}) to {best_model_path}")
    
    # Create metadata
    metadata = {
        'feature_order': FEATURE_ORDER,
        'best_model_name': best_model_name,
        'model_names': model_names,
        'models': model_metrics
    }
    
    # Save metadata
    meta_path = model_dir / "meta.json"
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"  Saved metadata to {meta_path}")
    
    print("\n=== Training Complete ===")
    print(f"Best model: {model_names[best_model_name]}")
    print(f"Best accuracy: {model_metrics[best_model_name]['accuracy']:.4f}")

if __name__ == "__main__":
    main()