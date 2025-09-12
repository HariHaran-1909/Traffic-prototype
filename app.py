from flask import Flask, render_template, jsonify, request
import threading
import cv2
import time
import pandas as pd
import joblib
import os
from datetime import datetime

app = Flask(__name__)

vehicle_count_global = 0
model = joblib.load('congestion_model.pkl')
label_map = {0: 'low', 1: 'medium', 2: 'high'}
CSV_FILE = 'traffic_history.csv'
reports = []  # Store user reports
signal_override = False  # Manual signal override status

def save_traffic_entry(vehicle_count):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        if not file_exists:
            f.write('timestamp,vehicle_count\n')
        ts = datetime.now().strftime('%H:%M:%S')
        f.write(f'{ts},{vehicle_count}\n')

def load_recent_entries(n=20):
    if not os.path.isfile(CSV_FILE):
        return [], []
    df = pd.read_csv(CSV_FILE)
    df = df.tail(n)
    return list(df['timestamp']), list(df['vehicle_count'])

def vehicle_detection_thread():
    global vehicle_count_global
    car_cascade = cv2.CascadeClassifier('cars.xml')
    cap = cv2.VideoCapture('traffic_video2.mp4')
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 2)
        vehicle_count_global = len(cars)
        save_traffic_entry(vehicle_count_global)
        time.sleep(2)

    cap.release()

@app.route('/')
def dashboard():
    avg_speed = 45
    X_pred = [[vehicle_count_global, avg_speed]]
    pred = model.predict(X_pred)[0]
    congestion = label_map[pred]

    # Alert logic with signal override consideration
    if signal_override:
        alert_message = "🔧 Manual signal override active. Operator control enabled."
        alert_class = "alertmedium"
    elif congestion == 'high':
        alert_message = "⚠️ Heavy congestion detected. Please consider alternate routes!"
        alert_class = "alerthigh"
    elif congestion == 'medium':
        alert_message = "⚡ Moderate congestion. Drive carefully."
        alert_class = "alertmedium"
    else:
        alert_message = "✅ Traffic is smooth. No delays!"
        alert_class = "alertlow"

    time_labels, vehicle_counts = load_recent_entries(20)

    return render_template(
        'dashboard.html',
        vehicle_count=vehicle_count_global,
        avg_speed=avg_speed,
        congestion_level=congestion,
        alert_message=alert_message,
        alert_class=alert_class,
        time_labels=time_labels,
        historical_vehicle_counts=vehicle_counts,
        signal_override=signal_override,
        reports_count=len(reports)
    )

@app.route('/vehicle_count')
def vehicle_count_api():
    return jsonify(count=vehicle_count_global)

@app.route('/search_traffic')
def search_traffic():
    query = request.args.get('q', '').lower()
    time_labels, vehicle_counts = load_recent_entries(50)
    
    if not query:
        return jsonify(labels=time_labels, data=vehicle_counts)
    
    # Filter data based on search query
    filtered_labels = []
    filtered_data = []
    
    for i, label in enumerate(time_labels):
        if (query in label.lower() or 
            query in str(vehicle_counts[i]) or
            (query == 'high' and vehicle_counts[i] > 15) or
            (query == 'medium' and 5 <= vehicle_counts[i] <= 15) or
            (query == 'low' and vehicle_counts[i] < 5)):
            filtered_labels.append(label)
            filtered_data.append(vehicle_counts[i])
    
    return jsonify(labels=filtered_labels, data=filtered_data)

@app.route('/report_congestion', methods=['POST'])
def report_congestion():
    global reports
    user_report = {
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'message': 'User reported unusual congestion',
        'location': request.json.get('location', 'Unknown')
    }
    reports.append(user_report)
    return jsonify(status='success', message='Report submitted successfully!')

@app.route('/signal_override', methods=['POST'])
def toggle_signal_override():
    global signal_override
    signal_override = not signal_override
    status = 'activated' if signal_override else 'deactivated'
    return jsonify(status='success', message=f'Signal override {status}', override_active=signal_override)

@app.route('/get_reports')
def get_reports():
    return jsonify(reports=reports[-5:])  # Return last 5 reports


if __name__ == "__main__":
    t = threading.Thread(target=vehicle_detection_thread)
    t.daemon = True
    t.start()
    app.run(debug=True)





