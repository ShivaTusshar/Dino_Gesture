import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

print("Loading your gesture data...")
try:
    df = pd.read_csv('gesture_data.csv')
except FileNotFoundError:
    print("Error: gesture_data.csv not found. Run collect_data.py first!")
    exit()

# Separate the answers (labels) from the math (coordinates)
X = df.drop('label', axis=1) 
y = df['label']              

# Split data: 80% for studying, 20% for taking a test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the AI brain (Random Forest)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Give the AI a test to see how accurate it is
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the brain into a file we can use for the game
with open('gesture_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
print("Success! Your AI brain has been saved as 'gesture_model.pkl'") 