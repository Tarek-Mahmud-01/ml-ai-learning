import joblib
import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

CLEANED_PATH = 'data/cleaned_data.csv'
BEST_MODEL_PATH = 'models/best_sales_forecast.joblib'

def load_data(path: str):
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return None
    return pd.read_csv(path)

def main():
    # 1. Load Data
    df = load_data(CLEANED_PATH)
    if df is None: return

    # 2. SELECT FEATURES & TARGET (Predicting Revenue)
    # These are our "Clues" and our "Goal"
    features = ['Units_Sold', 'Unit_Price', 'Discount', 'Cost_Price']
    X = df[features]
    y = df['Revenue']
    
    # 3. SPLIT
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. START THE COMPETITION
    print("--- MODEL COMPETITION STARTING ---")
    
    # Candidate 1: Linear Regression (The Straight Line)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    
    # Candidate 2: Random Forest (The Forest of Trees)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

    # 5. ANNOUNCE THE WINNER
    print(f"\nLinear Regression Error (RMSE): ${lr_rmse:.2f}")
    print(f"Random Forest Error (RMSE): ${rf_rmse:.2f}")

    if lr_rmse < rf_rmse:
        best_model = lr
        model_name = 'Linear Regression'
    else:
        best_model = rf
        model_name = 'Random Forest'

    print(f"\nTHE WINNER IS: {model_name}")
    print(f"Accuracy (R2 Score): {r2_score(y_test, best_model.predict(X_test)):.4f}")

    # 6. BUSINESS INSIGHT (FORECASTING)
    print("\n--- FINAL BUSINESS REPORT ---")
    # Let's predict a sale of 50 units of a $200 item with 10% discount
    sample_sale = pd.DataFrame([[50, 200.0, 0.10, 100.0]], columns=features)
    forecast = best_model.predict(sample_sale)[0]
    print(f"Predicted Revenue for a 50-unit sale: ${forecast:.2f}")

    # Save the winner
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, BEST_MODEL_PATH)
    print(f"\nFinal model saved to {BEST_MODEL_PATH}")
    print("Congratulations on completing the 7-day program!")

if __name__ == '__main__':
    main()
