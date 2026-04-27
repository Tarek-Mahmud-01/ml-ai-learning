import joblib
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

CLEANED_PATH = 'data/cleaned_data.csv'
MODEL_PATH = 'models/rf_tuned.joblib'

def load_data(path: str):
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return None
    return pd.read_csv(path)

def main():
    # 1. Load Data
    df = load_data(CLEANED_PATH)
    if df is None: return

    # 2. CREATE TARGET
    df['HighProfit'] = (df['Profit'] > 500).astype(int)

    # 3. SELECT FEATURES
    features = ['Units_Sold', 'Unit_Price', 'Discount', 'Cost_Price', 'Hour']
    X = df[features]
    y = df['HighProfit']
    
    # 4. SPLIT
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. DEFINE THE SEARCH GRID (The different recipes to try)
    param_grid = {
        'n_estimators': [50, 100, 150],       # Number of trees
        'max_depth': [None, 5, 10],           # How deep the trees can go
        'min_samples_split': [2, 5],          # Minimum items to make a branch
    }
    
    # 6. START GRID SEARCH (Trying all combinations)
    print("Starting Grid Search... (This might take a moment as we try many combinations)")
    rf = RandomForestClassifier(random_state=42)
    
    # cv=3 means we will do a "Triple Check" (3-fold cross validation)
    grid = GridSearchCV(rf, param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=1)
    grid.fit(X_train, y_train)

    # 7. RESULTS
    print("\n" + "="*30)
    print("THE WINNING SETTINGS:")
    print(grid.best_params_)
    print(f"BEST SCORE: {grid.best_score_:.4f}")
    print("="*30)

    # Save the absolute best model
    os.makedirs('models', exist_ok=True)
    best_model = grid.best_estimator_
    joblib.dump(best_model, MODEL_PATH)
    print(f'Success! Saved tuned model to {MODEL_PATH}')

if __name__ == '__main__':
    main()
