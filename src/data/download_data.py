"""
Download Heart Disease dataset from UCI ML Repository
"""
import os
import ssl
import urllib.request
import certifi
import pandas as pd

def download_dataset():
    """Download UCI Heart Disease dataset"""
    # Create data directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # UCI Heart Disease dataset URL
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    
    # Column names for the dataset
    column_names = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    
    print("Downloading Heart Disease dataset from UCI ML Repository...")
    
    try:
        # Create SSL context using certifi CA bundle to avoid macOS certificate issues
        context = ssl.create_default_context(cafile=certifi.where())

        # Download the dataset with SSL context
        with urllib.request.urlopen(url, context=context) as response:
            with open('data/raw/heart.data', 'wb') as out_file:
                out_file.write(response.read())

        # Read and save as CSV
        df = pd.read_csv('data/raw/heart.data', names=column_names, na_values='?')
        
        # Convert target to binary (0: no disease, 1: disease present)
        df['target'] = (df['target'] > 0).astype(int)
        
        # Save as CSV
        df.to_csv('data/raw/heart.csv', index=False)
        
        print(f"✓ Dataset downloaded successfully!")
        print(f"✓ Shape: {df.shape}")
        print(f"✓ Saved to: data/raw/heart.csv")
        
        # Display basic info
        print("Dataset Info:")
        print(df.info())
        print("Target distribution:")
        print(df['target'].value_counts())
        
        return df
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        raise

if __name__ == "__main__":
    download_dataset()
