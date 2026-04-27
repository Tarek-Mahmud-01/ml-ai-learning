import pandas as pd
import numpy as np
import os

def generate_sample_erp_data(path='data/erp_data.csv', n_rows=1000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=n_rows, freq='h')
    products = ['P001', 'P002', 'P003', 'P004', 'P005']
    regions = ['North', 'South', 'East', 'West']
    categories = ['Electronics', 'Furniture', 'Apparel', 'Food']
    
    data = {
        'Date': dates,
        'Product_ID': np.random.choice(products, n_rows),
        'Category': np.random.choice(categories, n_rows),
        'Region': np.random.choice(regions, n_rows),
        'Units_Sold': np.random.randint(1, 50, n_rows),
        'Unit_Price': np.random.uniform(10.0, 500.0, n_rows).round(2),
        'Discount': np.random.uniform(0, 0.2, n_rows).round(2),
        'Cost_Price': np.random.uniform(5.0, 300.0, n_rows).round(2)
    }
    
    df = pd.DataFrame(data)
    df['Revenue'] = (df['Units_Sold'] * df['Unit_Price'] * (1 - df['Discount'])).round(2)
    df['Profit'] = (df['Revenue'] - (df['Units_Sold'] * df['Cost_Price'])).round(2)
    
    # Add some noise/missing values for wrangling practice
    mask = np.random.random(n_rows) < 0.05
    df.loc[mask, 'Units_Sold'] = np.nan
    
    df.to_csv(path, index=False)
    print(f"Generated sample ERP data at {path}")

if __name__ == "__main__":
    generate_sample_erp_data()
