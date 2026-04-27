import joblib
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

CLEANED_PATH = 'data/cleaned_data.csv'
MODEL_PATH = 'models/linear_regression.joblib'

def load_data(path: str):
    """Teacher Tip: Always ensure the file exists before loading!"""
    if not os.path.exists(path):
        print(f"Error: {path} not found. Did you run Day 1 script?")
        return None
    return pd.read_csv(path)

def prepare_features(df):
    """
    Teacher Tip: We select specific 'Features' (X) to predict our 'Target' (y).
    Target = What we want to guess (Revenue)
    Features = The clues we use (Units_Sold, Unit_Price, Discount)
    """
    # 1. Define what we want to predict
    target_col = 'Revenue'
    
    # 2. Select the 'Clues'
    # We use numeric columns that actually influence Revenue
    features = ['Units_Sold', 'Unit_Price', 'Discount', 'Cost_Price']
    
    print(f"Using features: {features}")
    print(f"Targeting: {target_col}")

    X = df[features]
    y = df[target_col]

    # 3. Split: 80% for learning, 20% for testing
    return train_test_split(X, y, test_size=0.2, random_state=42)

def main():
    # Load our cleaned data from Day 1
    df = load_data(CLEANED_PATH)
    if df is None: return

    # Prepare data
    X_train, X_test, y_train, y_test = prepare_features(df)

    # --- THE LEARNING PHASE ---
    print("\nTraining the model (Finding the pattern)...")
    model = LinearRegression()
    model.fit(X_train, y_train) # This is where the 'math' happens!

    # --- THE EXAM PHASE ---
    print("Testing the model (Evaluating accuracy)...")
    predictions = model.predict(X_test)
    
    # How far off were we? (Smaller is better)
    mse = mean_squared_error(y_test, predictions)
    # How much of the pattern did we catch? (1.0 is a perfect score)
    r2 = r2_score(y_test, predictions)
    
    print("-" * 30)
    print(f'Mean Squared Error (Avg Error): {mse:.2f}')
    print(f'R2 Score (Pattern Match): {r2:.4f}')
    print("-" * 30)

    # Save our 'Brain' for future use
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f'Success! Saved model to {MODEL_PATH}')

if __name__ == '__main__':
    main()
