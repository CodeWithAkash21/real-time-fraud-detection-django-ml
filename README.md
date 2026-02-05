# Real-Time Fraud Detection System

## 🎥 Demo Preview

<p align="center">
  <img src="screenshots/dashboard.png" width="90%">
</p>

A production-grade fraud detection system using Django and Scikit-learn, trained on the Kaggle Credit Card Fraud Detection dataset (284k transactions).

## 📸 Project Screenshots

### Live Transaction Detection
<p align="center">
  <img src="screenshots/live-detection.png" width="90%">
</p>

### Executive Dashboard
<p align="center">
  <img src="screenshots/dashboard.png" width="90%">
</p>

## Features
- **Real-Time Inference**: <100ms response time using `RandomForestClassifier`.
- **Handling Imbalance**: `class_weight='balanced'` and RobustScaler.
- **API**: RESTful endpoint via Django REST Framework.
- **Persistence**: Transactions and predictions stored in PostgreSQL.
- **Deployment**: Dockerized with Gunicorn.

## Setup

### 1. Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional but recommended)

### 2. Local Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Train Model**:
   ```bash
   # Ensure data/creditcard.csv exists
   python ml_engine/train_model.py
   ```
3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Create Superuser**:
   ```bash
   python create_superuser.py
   ```
5. **Start Server**:
   ```bash
   python manage.py runserver
   ```

### 3. Docker Deployment
```bash
docker-compose up --build
```

## API Usage
**POST** `/api/detect/`

**Request**:
```json
{
    "transaction_id": "tx_123",
    "amount": 250.00,
    "features": [0.1, -1.2, ... (V1-V28)]
}
```

**Response**:
```json
{
    "transaction_id": "tx_123",
    "fraud_probability": 0.052,
    "fraud_detected": false
}
```
