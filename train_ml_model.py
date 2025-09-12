import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib  # for saving the model

# Load the dataset
print("ml model")
data = pd.read_csv('traffic_data.csv')

# Encode the congestion labels into numeric form
label_mapping = {'low': 0, 'medium': 1, 'high': 2}
data['congestion_label'] = data['congestion'].map(label_mapping)

# Select features and target
X = data[['vehicle_count', 'avg_speed']]
y = data['congestion_label']

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Instantiate the model
model = RandomForestClassifier()

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f'Model accuracy on test set: {accuracy:.2f}')

# Save the trained model to a file
joblib.dump(model, 'congestion_model.pkl')
print('Model saved as congestion_model.pkl')
