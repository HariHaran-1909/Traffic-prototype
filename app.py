from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import threading
import cv2
import time
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret123"  

# Users dictionary
users = {
    "citizen1": {"password": "citizen123", "role": "citizen"},
    "operator1": {"password": "operator123", "role": "operator"}
}

# Global variables
vehicle_count_global = 0
model = joblib.load('congestion_model.pkl')
label_map = {0: 'low', 1: 'medium', 2: 'high'}
CSV_FILE = 'traffic_history.csv'
reports = []  
signal_override = False  

# Save vehicle count to CSV
def save_traffic_entry(vehicle_count):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        if not file_exists:
            f.write('timestamp,vehicle_count\n')
        ts = datetime.now().strftime('%H:%M:%S')
        f.write(f'{ts},{vehicle_count}\n')

# Load recent traffic entries
def load_recent_entries(n=20):
    if not os.path.isfile(CSV_FILE):
        return [], []
    df = pd.read_csv(CSV_FILE)
    df = df.tail(n)
    return list(df['timestamp']), list(df['vehicle_count'])

# Vehicle detection thread
def vehicle_detection_thread():
    global vehicle_count_global
    car_cascade = cv2.CascadeClassifier('cars.xml')
    cap = cv2.VideoCapture('traffic_video3.mp4')
    
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

# Login route
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard route
@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    role = session.get('role', 'citizen')
    avg_speed = 45
    X_pred = [[vehicle_count_global, avg_speed]]
    pred = model.predict(X_pred)[0]
    congestion = label_map[pred]

    # Alert messages
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

    # Traffic signal info
    if congestion == 'high':
        signal_color = "🔴 Red"
        signal_time = "90 seconds"
    elif congestion == 'medium':
        signal_color = "🟡 Yellow"
        signal_time = "60 seconds"
    else:
        signal_color = "🟢 Green"
        signal_time = "30 seconds"

    time_labels, vehicle_counts = load_recent_entries(20)

    return render_template(
        'dashboard.html',
        role=role,
        vehicle_count=vehicle_count_global,
        avg_speed=avg_speed,
        congestion_level=congestion,
        alert_message=alert_message,
        alert_class=alert_class,
        time_labels=time_labels,
        historical_vehicle_counts=vehicle_counts,
        reports_count=len(reports),
        signal_color=signal_color,
        signal_time=signal_time,
        signal_override=signal_override
    )

# Vehicle count API
@app.route('/vehicle_count')
def vehicle_count_api():
    return jsonify(count=vehicle_count_global)

# Search traffic API
@app.route('/search_traffic')
def search_traffic():
    query = request.args.get('q', '').lower()
    time_filter = request.args.get('time', 'all')  # 'today', 'week', 'month', or 'all'
    status_filter = request.args.get('status', 'all')  # 'low', 'mid', 'high', or 'all'

    # Load all recent entries with timestamps and vehicle counts
    time_labels, vehicle_counts = load_recent_entries(100)  # Increase limit if needed

    filtered_labels, filtered_data = [], []

    # Filter entries by time
    now = datetime.now()
    def filter_by_time(ts_str):
        # Convert timestamp string to datetime object with today date
        ts = datetime.strptime(ts_str, '%H:%M:%S')
        ts_full = now.replace(hour=ts.hour, minute=ts.minute, second=ts.second, microsecond=0)

        if time_filter == 'today':
            return True  # Assuming all entries are today (adjust if you have full date)
        elif time_filter == 'week':
            # Assuming all entries today, expand logic if full date exists
            # Example placeholder, return True
            return True
        elif time_filter == 'month':
            # Similar placeholder
            return True
        else:
            return True  # 'all'

    for i, label in enumerate(time_labels):
        count = vehicle_counts[i]

        if not filter_by_time(label):
            continue

        # Filter by status
        if status_filter == 'low' and count >= 5:
            continue
        elif status_filter == 'mid' and (count < 5 or count > 15):
            continue
        elif status_filter == 'high' and count <= 15:
            continue

        # Filter by query (location/time/incident)
        if (query in label.lower() or
            query in str(count) or
            (query == 'high' and count > 15) or
            (query == 'medium' and 5 <= count <= 15) or
            (query == 'low' and count < 5)):
            filtered_labels.append(label)
            filtered_data.append(count)

    return jsonify(labels=filtered_labels, data=filtered_data)

# Report congestion
@app.route('/report_congestion', methods=['POST'])
def report_congestion():
    global reports
    user_report = {
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'message': 'User reported unusual congestion',
        'location': request.json.get('location','Unknown')
    }
    reports.append(user_report)
    return jsonify(status='success', message='Report submitted successfully!')

# Toggle signal override
@app.route('/signal_override', methods=['POST'])
def toggle_signal_override():
    global signal_override
    signal_override = not signal_override
    status = 'activated' if signal_override else 'deactivated'
    return jsonify(status='success', message=f'Signal override {status}', override_active=signal_override)

# Get latest reports
@app.route('/get_reports')
def get_reports():
    return jsonify(reports=reports[-5:])  

@app.route('/active_incidents')
def active_incidents():
    # Example: filter where vehicle count > threshold (e.g., high congestion)
    time_labels, vehicle_counts = load_recent_entries(50)
    filtered_labels = []
    filtered_counts = []
    for i, count in enumerate(vehicle_counts):
        if count > 9:  # Customize logic per your definition
            filtered_labels.append(time_labels[i])
            filtered_counts.append(count)
    return jsonify(labels=filtered_labels, data=filtered_counts)

@app.route('/peak_hours')
def peak_hours():
    # Example: last 5 entries with highest counts
    time_labels, vehicle_counts = load_recent_entries(50)
    peak_indices = sorted(range(len(vehicle_counts)), key=lambda x: vehicle_counts[x], reverse=True)[:5]
    data = [(time_labels[i], vehicle_counts[i]) for i in peak_indices]
    labels = [x[0] for x in data]
    counts = [x[1] for x in data]
    return jsonify(labels=labels, data=counts)

@app.route('/signal_override_periods')
def signal_override_periods():
    # If you log override status changes, filter times when it was active
    # Otherwise, return recent entries when override is True
    # Example: always returns empty unless override is active
    if signal_override:
        time_labels, vehicle_counts = load_recent_entries(10)
        return jsonify(labels=time_labels, data=vehicle_counts)
    else:
        return jsonify(labels=[], data=[])

@app.route('/recent_reports')
def recent_reports():
    # Return recent congestion reports
    return jsonify(reports=reports[-10:])


# Run app
if __name__ == "__main__":
    t = threading.Thread(target=vehicle_detection_thread)
    t.daemon = True
    t.start()
    app.run(debug=True)















