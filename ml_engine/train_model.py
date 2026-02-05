import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'creditcard.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'ml_engine', 'fraud_model.pkl')
RANDOM_STATE = 42

def train():
    print("Loading dataset...")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Please ensure 'data/creditcard.csv' exists.")
        
    df = pd.read_csv(DATA_PATH)
    
    # Feature Selection: Time, Amount, V1-V28
    # Users asked for: Time, Amount, V1-V28.
    X = df.drop(columns=['Class'])
    y = df['Class']

    print(f"Dataset Shape: {df.shape}")
    print(f"Fraud Rate: {y.mean():.4%}")

    # Stratified Split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    # Pipeline: Scaler + Classifier
    # RobustScaler is good for 'Amount' which likely has outliers.
    pipeline = Pipeline([
        ('scaler', RobustScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            class_weight='balanced',
            n_jobs=-1,
            random_state=RANDOM_STATE,
            verbose=1
        ))
    ])

    print("Training Random Forest Classifier (this may take a while)...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # Metrics
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    auc = roc_auc_score(y_test, y_proba)
    print(f"ROC-AUC Score: {auc:.4f}")
    
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    # Save Model
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Done!")

if __name__ == "__main__":
    train()
