#!/usr/bin/env python3

import pandas as pd
import heapq
import time
from typing import List, Dict

def generate_playlist(intervals: List[Dict]) -> List[Dict]:
    """
    Given a list of intervals with target BPM and optional energy, 
    return a list of tracks that best match each interval.
    
    Each interval dict contains:
        - bpm (int)
        - duration (int, in minutes)
        - energy (optional float between 0.0 and 1.0)

    Output: A list of dictionaries with:
        - interval_number (int)
        - title (str)
        - artist (str)
        - bpm (float)
        - energy (float)
        - duration_sec (int)
        - bpm_diff (float)
    """
    df = pd.read_csv('data/clean_tracks.csv')
    
    df['artist'] = df['artist'].str.strip('[]').str.replace("'", "")
    
    playlist = []
    used_tracks = set()
    
    for i, interval in enumerate(intervals, 1):
        target_bpm = interval['bpm']
        target_energy = interval.get('energy')
        
        heap = []
        
        for idx, track in df.iterrows():
            if idx in used_tracks:
                continue
                
            bpm_diff = abs(track['bpm'] - target_bpm)
            
            if target_energy is not None:
                energy_diff = abs(track['energy'] - target_energy)
                score = bpm_diff + 10 * energy_diff
            else:
                score = bpm_diff
            
            heapq.heappush(heap, (score, idx, track))
        
        if heap:
            score, idx, track = heapq.heappop(heap)
            used_tracks.add(idx)
            
            playlist.append({
                'interval_number': i,
                'title': track['title'],
                'artist': track['artist'],
                'bpm': track['bpm'],
                'energy': track['energy'],
                'duration_sec': track['duration_sec'],
                'bpm_diff': abs(track['bpm'] - target_bpm)
            })
    
    return playlist

def main():
    """Test the playlist generator with sample intervals."""
    test_intervals = [
        {'bpm': 120, 'duration': 5, 'energy': 0.4},  # Warm-up
        {'bpm': 155, 'duration': 3, 'energy': 0.8},  # High-intensity
        {'bpm': 100, 'duration': 4}                  # Cool-down (no energy specified)
    ]
    
    # Time the execution
    start_time = time.perf_counter()
    playlist = generate_playlist(test_intervals)
    end_time = time.perf_counter()
    
    # Print results
    print("\nGenerated Playlist:")
    print("-" * 80)
    print(f"{'Interval':<8} {'Title':<30} {'Artist':<20} {'BPM':<6} {'Energy':<7} {'BPM Diff':<9}")
    print("-" * 80)
    
    for track in playlist:
        print(f"{track['interval_number']:<8} "
              f"{track['title'][:27]:<30} "
              f"{track['artist'][:17]:<20} "
              f"{track['bpm']:<6.1f} "
              f"{track['energy']:<7.2f} "
              f"{track['bpm_diff']:<9.1f}")
    
    print(f"\nRuntime: {end_time - start_time:.3f} seconds")

if __name__ == '__main__':
    main() 