import joblib
import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

CLEANED_PATH = 'data/cleaned_data.csv'
MODEL_PATH = 'models/logistic_regression.joblib'

def load_data(path: str):
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return None
    return pd.read_csv(path)

def main():
    # 1. Load Data
    df = load_data(CLEANED_PATH)
    if df is None: return

    # 2. CREATE A TARGET (High Profit vs Low Profit)
    # We define 'High Profit' as anything over $500
    threshold = 500
    df['HighProfit'] = (df['Profit'] > threshold).astype(int)
    print(f"Created target 'HighProfit' based on > ${threshold} threshold.")
    print(f"Counts:\n{df['HighProfit'].value_counts()}")

    # 3. SELECT FEATURES (Clues)
    features = ['Units_Sold', 'Unit_Price', 'Discount', 'Cost_Price', 'Hour']
    X = df[features]
    y = df['HighProfit']
    
    # 4. SPLIT (Train/Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. SCALING (Standardize the clues)
    print("\nScaling features (Making all clues the same 'size')...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 6. TRAIN (Logistic Regression)
    print("Training the Logistic Classifier...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # 7. EVALUATE (The Report Card)
    y_pred = model.predict(X_test_scaled)
    
    print("\n--- CLASSIFICATION REPORT ---")
    print(classification_report(y_test, y_pred))
    
    # Save Model and Scaler (We need the scaler to use the model later!)
    os.makedirs('models', exist_ok=True)
    joblib.dump({'model': model, 'scaler': scaler}, MODEL_PATH)
    print(f'Success! Saved model and scaler to {MODEL_PATH}')

if __name__ == '__main__':
    main()
