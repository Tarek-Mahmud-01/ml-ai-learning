import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

DATA_PATH = 'data/erp_data.csv'
CLEANED_PATH = 'data/cleaned_data.csv'
REPORTS_DIR = 'reports'

def load_data(path: str):
    """Loads CSV data and returns a DataFrame."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Data file not found at {path}")
        df = pd.read_csv(path)
        print(f"Successfully loaded {len(df)} rows from {path}")
        return df
    except FileNotFoundError as e:
        print(e)
        return None

def clean_data(df):
    """Performs data cleaning operations."""
    print("\nCleaning data...")
    df = df.copy()
    
    # Handle Date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print("- Converted 'Date' to datetime objects.")

    # Handle missing values (we added some to Units_Sold)
    initial_len = len(df)
    df = df.dropna(subset=['Units_Sold'])
    dropped = initial_len - len(df)
    if dropped > 0:
        print(f"- Dropped {dropped} rows with missing 'Units_Sold'.")

    # Feature Engineering: Extract Hour and Day from Date
    if 'Date' in df.columns:
        df['Hour'] = df['Date'].dt.hour
        df['DayOfWeek'] = df['Date'].dt.day_name()
        print("- Added 'Hour' and 'DayOfWeek' features.")

    return df

def plot_data(df):
    """Generates and saves visual reports."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    print(f"\nGenerating plots in {REPORTS_DIR}...")
    
    # 1. Histograms for numeric columns
    plt.figure(figsize=(12, 8))
    df.select_dtypes('number').hist(bins=20, figsize=(15, 10))
    plt.tight_layout()
    plt.savefig(f'{REPORTS_DIR}/histograms.png')
    print("- Saved histograms.png")

    # 2. Revenue by Category
    if 'Category' in df.columns and 'Revenue' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Revenue', data=df, estimator='sum', hue='Category', palette='viridis', legend=False)
        plt.title('Total Revenue by Category')
        plt.savefig(f'{REPORTS_DIR}/revenue_by_category.png')
        print("- Saved revenue_by_category.png")

    # 3. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes('number')
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.savefig(f'{REPORTS_DIR}/correlation_heatmap.png')
    print("- Saved correlation_heatmap.png")

def main():
    # Load
    df = load_data(DATA_PATH)
    if df is None:
        print("Please ensure the data file exists or run the generation script.")
        return
    
    # Inspect
    print("\nData Overview:")
    print(df.head())
    print(f"\nMissing values per column:\n{df.isnull().sum()}")

    # Clean
    cleaned = clean_data(df)
    
    # Save Cleaned Data
    os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
    cleaned.to_csv(CLEANED_PATH, index=False)
    print(f"\nSaved cleaned data to {CLEANED_PATH}")

    # Analyze/Plot
    plot_data(cleaned)
    
    print("\nData Wrangling Workflow Complete!")

if __name__ == '__main__':
    main()
