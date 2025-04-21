#!/usr/bin/env python3

import pandas as pd
import networkx as nx
import time
from typing import List, Dict
import heapq

def generate_playlist(intervals: List[Dict], top_n: int = 20) -> List[Dict]:
    """
    Generate a playlist that globally minimizes transitions across intervals.

    Parameters:
        intervals: list of dictionaries, each with:
            - bpm (int)
            - duration (int, in minutes)
            - energy (optional float between 0.0 and 1.0)
        top_n: number of top candidate songs to keep per interval layer

    Returns:
        A list of dictionaries, each with:
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
    
    G = nx.DiGraph()
    
    source = 'source'
    sink = 'sink'
    
    layer_songs = []
    for i, interval in enumerate(intervals):
        target_bpm = interval['bpm']
        target_energy = interval.get('energy')
        
        scores = []
        for idx, track in df.iterrows():
            bpm_diff = abs(track['bpm'] - target_bpm)
            
            if target_energy is not None:
                energy_diff = abs(track['energy'] - target_energy)
                score = bpm_diff + 10 * energy_diff
            else:
                score = bpm_diff
            
            scores.append((score, idx, track))
        
        top_songs = heapq.nsmallest(top_n, scores)
        layer_songs.append(top_songs)
        
        for score, idx, track in top_songs:
            node_id = f"layer_{i}_song_{idx}"
            G.add_node(node_id, 
                      track=track,
                      layer=i,
                      bpm=track['bpm'],
                      energy=track['energy'])
    
    for i in range(len(intervals) - 1):
        current_layer = layer_songs[i]
        next_layer = layer_songs[i + 1]
        
        for score1, idx1, track1 in current_layer:
            node1 = f"layer_{i}_song_{idx1}"
            
            for score2, idx2, track2 in next_layer:
                node2 = f"layer_{i+1}_song_{idx2}"
                
                bpm_diff = abs(track1['bpm'] - track2['bpm'])
                energy_diff = abs(track1['energy'] - track2['energy'])
                weight = bpm_diff + 10 * energy_diff
                
                G.add_edge(node1, node2, weight=weight)
    
    for score, idx, track in layer_songs[0]:
        node = f"layer_0_song_{idx}"
        G.add_edge(source, node, weight=0)
    
    for score, idx, track in layer_songs[-1]:
        node = f"layer_{len(intervals)-1}_song_{idx}"
        G.add_edge(node, sink, weight=0)
    
    path = nx.shortest_path(G, source=source, target=sink, weight='weight')
    
    playlist = []
    for i, node in enumerate(path[1:-1], 1):
        track = G.nodes[node]['track']
        target_bpm = intervals[i-1]['bpm']
        
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
    """Test the graph-based playlist generator with sample intervals."""
    test_intervals = [
        {'bpm': 120, 'duration': 5, 'energy': 0.4},  # Warm-up
        {'bpm': 155, 'duration': 3, 'energy': 0.8},  # High-intensity
        {'bpm': 130, 'duration': 4, 'energy': 0.6},  # Medium-intensity
        {'bpm': 100, 'duration': 4}                  # Cool-down (no energy specified)
    ]
    
    # Time the execution
    start_time = time.perf_counter()
    playlist = generate_playlist(test_intervals, top_n=20)
    end_time = time.perf_counter()
    
    # Print results
    print("\nGenerated Playlist (Graph-based):")
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