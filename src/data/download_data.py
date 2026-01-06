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
