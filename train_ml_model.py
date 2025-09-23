import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib 


print("ml model")
data = pd.read_csv('traffic_data.csv')

label_mapping = {'low': 0, 'medium': 1, 'high': 2}
data['congestion_label'] = data['congestion'].map(label_mapping)

X = data[['vehicle_count', 'avg_speed']]
y = data['congestion_label']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = RandomForestClassifier()

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f'Model accuracy on test set: {accuracy:.2f}')

joblib.dump(model, 'congestion_model.pkl')
print('Model saved as congestion_model.pkl')
