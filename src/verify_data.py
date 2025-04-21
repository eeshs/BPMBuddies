#!/usr/bin/env python3

import pandas as pd
import os

def verify_cleaned_data():
    file_path = 'data/clean_tracks.csv'
    print(f"Loading cleaned data from {file_path}...")
    
    df = pd.read_csv(file_path)
    
    # Basic info
    print("\nDataset Overview:")
    print(f"Number of rows: {len(df):,}")
    print(f"Number of columns: {len(df.columns):,}")
    
    # Column names and types
    print("\nColumns and their types:")
    print(df.dtypes)
    
    # Value ranges
    print("\nValue ranges for numeric columns:")
    numeric_cols = ['bpm', 'energy', 'duration_sec']
    for col in numeric_cols:
        print(f"\n{col}:")
        print(f"  Min: {df[col].min():.2f}")
        print(f"  Max: {df[col].max():.2f}")
        print(f"  Mean: {df[col].mean():.2f}")
    
    # Check for missing values
    print("\nMissing values check:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("✓ No missing values found")
    else:
        print("Missing values per column:")
        print(missing[missing > 0])
    
    # Sample data
    print("\nFirst few rows of the dataset:")
    print(df.head(3).to_string())

if __name__ == '__main__':
    verify_cleaned_data() 