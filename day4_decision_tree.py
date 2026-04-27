import joblib
import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

CLEANED_PATH = 'data/cleaned_data.csv'
MODEL_PATH = 'models/decision_tree.joblib'
TREE_IMAGE = 'reports/decision_tree.png'

def load_data(path: str):
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return None
    return pd.read_csv(path)

def main():
    # 1. Load Data
    df = load_data(CLEANED_PATH)
    if df is None: return

    # 2. CREATE TARGET (Same as Day 3 for comparison)
    df['HighProfit'] = (df['Profit'] > 500).astype(int)

    # 3. SELECT FEATURES
    # Decision Trees can handle more clues easily!
    features = ['Units_Sold', 'Unit_Price', 'Discount', 'Cost_Price', 'Hour']
    X = df[features]
    y = df['HighProfit']
    
    # 4. SPLIT
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. TRAIN (No Scaling Needed!)
    print("Growing the Decision Tree...")
    # we use max_depth=3 to keep the tree simple and easy to read
    model = DecisionTreeClassifier(random_state=42, max_depth=3)
    model.fit(X_train, y_train)

    # 6. EVALUATE
    y_pred = model.predict(X_test)
    print("\n--- CLASSIFICATION REPORT ---")
    print(classification_report(y_test, y_pred))

    # 7. VISUALIZE (The "Brain Map")
    print(f"\nCreating the 'Brain Map' (Tree Visualization)...")
    os.makedirs('reports', exist_ok=True)
    plt.figure(figsize=(20, 10))
    plot_tree(model, 
              feature_names=features, 
              class_names=['Low Profit', 'High Profit'], 
              filled=True, 
              rounded=True,
              fontsize=12)
    plt.savefig(TREE_IMAGE)
    print(f'Success! Saved tree visualization to {TREE_IMAGE}')

    # Save Model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f'Saved model to {MODEL_PATH}')

if __name__ == '__main__':
    main()
