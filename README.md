Smart Traffic Congestion Monitoring & Prediction System
📌 Overview

The Smart Traffic Congestion Monitoring & Prediction System is an AI-powered traffic management solution that uses computer vision and machine learning to detect vehicles, predict congestion levels, and dynamically optimize traffic signal timing.

This system aims to reduce traffic congestion, improve urban mobility, and enable data-driven traffic management.

🎯 Problem Statement

Traditional traffic signals operate on fixed timers and do not adapt to real-time traffic conditions. This results in:

Increased congestion

Fuel wastage

Higher pollution levels

Longer commute times

This project introduces an intelligent, adaptive traffic control system.

🧠 System Architecture
Live Video Feed
       ↓
Vehicle Detection (OpenCV)
       ↓
Vehicle Count Extraction
       ↓
ML Model Prediction (Congestion Level)
       ↓
Adaptive Signal Control
       ↓
Dashboard Visualization
🔍 Key Features

🚗 Real-time vehicle detection from video feed

📊 Traffic data logging and historical analysis

🤖 ML-based congestion prediction (Low / Medium / High)

🚦 Dynamic traffic signal adjustment

📈 Interactive dashboard with charts and alerts

👤 Role-based access (Citizen / Operator)

🛠 Manual signal override option for operators

🛠 Tech Stack
🔹 Backend

Python

Flask

Pandas

OpenCV

Joblib

🔹 Machine Learning

Random Forest Classifier

Logistic Regression (Experimented)

Pretrained model saved as .pkl

🔹 Frontend

HTML

CSS

JavaScript

Chart.js

🔹 Data Storage

CSV (traffic_history.csv)

🖥 How It Works
1️⃣ Vehicle Detection

Using OpenCV, video frames are processed to detect and count vehicles in real time.

2️⃣ Data Processing

Vehicle count and average speed are recorded with timestamps using Pandas.

3️⃣ Congestion Prediction

A trained ML model predicts congestion levels based on:

Vehicle count

Speed

4️⃣ Adaptive Signal Control

Signal timing dynamically adjusts:

High congestion → Increase green duration

Low congestion → Normal timing

5️⃣ Dashboard

The Flask web dashboard displays:

Vehicle count

Congestion status

Historical trends

Alerts

📊 Machine Learning Details

Type: Supervised Classification

Algorithms Used:

Random Forest

Logistic Regression

Evaluation Metrics:

Accuracy

Confusion Matrix
