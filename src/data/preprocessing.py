"""
Data preprocessing and feature engineering for Heart Disease prediction
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

def load_data(filepath='data/raw/heart.csv'):
    """Load raw data from CSV file"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"Loaded data shape: {df.shape}")
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print("\nMissing values:")
        print(missing[missing > 0])
        
        # For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
                print(f"Filled missing values in {col} with median")
    else:
        print("✓ No missing values found")
    
    return df

def preprocess_data(df, test_size=0.2, random_state=42):
    """
    Preprocess the data:
    - Split features and target
    - Train/test split
    - Scale features
    """
    # Separate features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"\nTrain set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrame to preserve column names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns, index=X_test.index)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def save_processed_data(X_train, X_test, y_train, y_test, scaler, output_dir='data/processed'):
    """Save processed data and scaler"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save datasets
    X_train.to_pickle(f"{output_dir}/X_train.pkl")
    X_test.to_pickle(f"{output_dir}/X_test.pkl")
    y_train.to_pickle(f"{output_dir}/y_train.pkl")
    y_test.to_pickle(f"{output_dir}/y_test.pkl")
    
    # Save scaler
    with open(f"{output_dir}/scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"\n✓ Processed data saved to {output_dir}/")

def main():
    """Main preprocessing pipeline"""
    print("=" * 50)
    print("Data Preprocessing Pipeline")
    print("=" * 50)
    
    # Load data
    print("\n1. Loading data...")
    df = load_data()
    
    # Handle missing values
    print("\n2. Handling missing values...")
    df = handle_missing_values(df)
    
    # Preprocess data
    print("\n3. Preprocessing data...")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    
    # Save processed data
    print("\n4. Saving processed data...")
    save_processed_data(X_train, X_test, y_train, y_test, scaler)
    
    print("\n" + "=" * 50)
    print("Preprocessing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
