🚦 Smart Traffic Congestion Monitoring and Prediction System
📑 Table of Contents

Overview

Features

Architecture & Code Flow

Technologies Used

Setup & Usage

Expansion & Future Scope

Implementation Scenarios

Screenshots

References

License

📖 Overview

This project is an AI-powered traffic management system developed for Smart India Hackathon 2025.
It monitors, predicts, and optimizes urban traffic congestion using live camera feeds, computer vision, and machine learning.

✅ Key Capabilities:

Detects vehicles in real time.

Classifies congestion levels (low, medium, high).

Recommends adaptive traffic signal timings.

Provides an interactive dashboard for operators.

✨ Features

🎥 Real-time vehicle detection from live video feeds.

🤖 Congestion prediction using trained ML models.

🚦 Dynamic signal timing recommendations.

📊 Interactive dashboard with live data & charts.

📝 User congestion reports & manual signal override.

📈 Historical trend analysis and reports.

🏗️ Architecture & Code Flow

1. Vehicle Detection (OpenCV):

Background thread runs Haar Cascade (cars.xml) to detect vehicles.

Updates a global vehicle count variable.

Logs results with timestamps into CSV for analytics.

2. Backend (Flask):

/ route fetches vehicle count + optional average speed.

Data passed to ML model (congestion_model.pkl) for classification.

Determines signal recommendations & alert messages.

Sends processed data to frontend for rendering.

3. Frontend (HTML/JS):

Dashboard shows:

Live counts, congestion status, alerts.

Dynamic charts (Chart.js).

Signal suggestion with countdown timer.

JavaScript cycles signal status dynamically.

4. APIs:

Endpoints for:

Live vehicle count.

Historical logs & search.

User reports.

Signal override.

🛠️ Technologies Used

Python 3

Flask – Backend & APIs

OpenCV – Vehicle detection (Haar Cascade)

Scikit-learn – ML model for congestion prediction

Pandas – CSV analytics

HTML5, CSS3, JavaScript – Frontend

Chart.js – Dynamic charts

Material Icons – UI enhancements

⚙️ Setup & Usage
Prerequisites

Python 3.7+

pip package manager


Install dependencies:

pip install -r requirements.txt


Download Haar Cascade XML (cars.xml) and place it in the project directory.

Prepare a test video (e.g., traffic_video3.mp4).

(Optional) Train or use the provided ML model (congestion_model.pkl).

Running the App

Start Flask server:

python app.py


Open in browser:
👉 http://127.0.0.1:5000/

🚀 Expansion & Future Scope

🌐 Scale to multiple junctions / city-wide deployment.

🔗 Integrate IoT sensors & weather data.

🚑 Support emergency vehicle detection with adaptive signal priority.

☁️ Deploy cloud-based analytics & dashboards.

📱 Develop mobile app & operator dashboards.

📌 Implementation Scenarios

Municipality traffic management centers.

Smart city pilot projects.

Academic research & public infrastructure demos.

🖼️ Screenshots

<img width="1920" height="918" alt="Screenshot 2025-09-14 222922" src="https://github.com/user-attachments/assets/86a490ab-b239-48ca-af9e-ad58dfffef0f" />

📚 References

OpenCV Documentation

Scikit-learn Documentation

Research papers on traffic flow prediction using ML

📜 License

This project is licensed under the MIT License – feel free to use and modify.
