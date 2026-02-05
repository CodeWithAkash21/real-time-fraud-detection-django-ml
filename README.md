<h1 align="center">🚨 Real-Time Fraud Detection System</h1>

<p align="center">
A production-grade Machine Learning fraud detection system built with Django, Django REST Framework, and Scikit-learn.
</p>

<p align="center">
  <img src="screenshots/dashboard.png" width="90%">
</p>

---

## 🎯 Overview

This project is a **real-time fraud detection system** designed to identify fraudulent credit card transactions using Machine Learning.  

The system integrates a trained ML model into a Django backend, exposing REST APIs for real-time prediction while storing transaction data and analytics for monitoring.

The model is trained using the **Kaggle Credit Card Fraud Detection dataset** containing over **284,000 transactions** with highly imbalanced classes.

---

## 📸 Project Screenshots

### 🔹 Live Transaction Detection
<p align="center">
  <img src="screenshots/live-detection.png" width="90%">
</p>

### 🔹 Executive Dashboard
<p align="center">
  <img src="screenshots/dashboard.png" width="90%">
</p>

---

## 🚀 Features

- ✅ Real-time fraud prediction (<100ms inference)
- ✅ RandomForestClassifier-based ML model
- ✅ Handles class imbalance using `class_weight='balanced'`
- ✅ Feature scaling using RobustScaler
- ✅ REST API powered by Django REST Framework
- ✅ Transaction storage and prediction logging
- ✅ Dockerized deployment
- ✅ Modular ML pipeline
- ✅ Dashboard for monitoring transactions

---

## 🧠 Machine Learning Pipeline

1. Dataset preprocessing and cleaning
2. Feature scaling using RobustScaler
3. Handling imbalanced dataset
4. Model training using Random Forest
5. Model serialization (`fraud_model.pkl`)
6. Real-time inference via API

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django, Django REST Framework |
| Machine Learning | Scikit-learn |
| Database | PostgreSQL / SQLite |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Docker, Gunicorn |
| Version Control | Git & GitHub |

---

## 📂 Project Structure
