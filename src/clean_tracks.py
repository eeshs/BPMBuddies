#!/usr/bin/env python3

import pandas as pd
import os

def clean_tracks():
    input_file = 'data/raw_tracks.csv'
    output_file = 'data/clean_tracks.csv'
    
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Initial row count: {len(df):,}")
    
    columns_to_keep = {
        'id': 'track_id',
        'name': 'title',
        'artists': 'artist',
        'tempo': 'bpm',
        'energy': 'energy',
        'duration_ms': 'duration_ms'
    }
    
    df = df[columns_to_keep.keys()].rename(columns=columns_to_keep)
    
    df = df.dropna(subset=['bpm', 'energy', 'duration_ms'])
    print(f"Row count after dropping missing values: {len(df):,}")
    
    df['duration_sec'] = (df['duration_ms'] / 1000).astype(int)
    df = df.drop('duration_ms', axis=1)
    
    df = df.head(120000)
    print(f"Final row count: {len(df):,}")
    
    print(f"Saving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False, encoding='utf-8')
    print("Data cleaning completed successfully!")

if __name__ == '__main__':
    clean_tracks() 