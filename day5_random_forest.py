import joblib
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

CLEANED_PATH = 'data/cleaned_data.csv'
MODEL_PATH = 'models/random_forest.joblib'
IMPORTANCE_IMAGE = 'reports/rf_feature_importance.png'

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

    # 5. TRAIN (The Forest of 100 Trees)
    print("Planting the Random Forest (100 trees voting)...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. EVALUATE
    y_pred = model.predict(X_test)
    print("\n--- CLASSIFICATION REPORT ---")
    print(classification_report(y_test, y_pred))

    # 7. FEATURE IMPORTANCE (Which clue was the MVP?)
    print("\nCalculating Feature Importance...")
    importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances.values, y=importances.index, palette='magma', hue=importances.index, legend=False)
    plt.title('Which clues were most important to the AI?')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    
    os.makedirs('reports', exist_ok=True)
    plt.savefig(IMPORTANCE_IMAGE)
    print(f'Success! Saved feature importance chart to {IMPORTANCE_IMAGE}')

    # Save Model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f'Saved model to {MODEL_PATH}')

if __name__ == '__main__':
    main()
