# BPMBuddies

## Overview
BPMBuddies is a Python-based web application that helps users generate custom workout playlists by matching songs to user-defined workout intervals. The application uses two different algorithmic approaches to find the perfect songs for each interval based on BPM (beats per minute), duration, and optional energy level.

## Features
- Upload or use a pre-cleaned 160k+ Spotify dataset
- Add workout intervals with:
  - Target BPM
  - Duration in minutes
  - Optional energy level (0.0-1.0)
- Choose between two algorithms:
  - **Greedy**: Fastest match per interval using a heap-based approach
  - **Graph-based**: Globally smooth transitions using shortest path algorithm
- Flask web interface for easy playlist creation
- CSV export support for generated playlists
- Modular Python design for maintainability

## Technologies
- **Python 3.x**: Core programming language
- **Flask**: Web framework for the user interface
- **Pandas**: Data manipulation and analysis
- **heapq**: Priority queue implementation for the greedy algorithm
- **NetworkX**: Graph algorithms for the pathfinding approach

## Project Structure
```
BPMBuddies/
├── app.py                  # Flask app
├── requirements.txt        # Project dependencies
├── README.md               # This file
├── data/
│   ├── raw_tracks.csv      # Original Spotify dataset
│   └── clean_tracks.csv    # Cleaned dataset used in algorithms
├── src/
│   ├── clean_tracks.py     # Cleans and trims raw data
│   ├── greedy_selector.py  # Greedy selection algorithm
│   ├── graph_selector.py   # Graph-based pathfinding
│   └── utils.py            # Shared helpers (if used)
├── templates/
│   ├── index.html          # Form UI
│   └── playlist.html       # Playlist results
├── docs/
│   └── comparison.md       # Algorithm performance comparison
└── static/                 # (Optional CSS or JS)
```

## Setup & Usage

### 1. Clone this repo
```bash
git clone https://github.com/eeshs/BPMBuddies.git
cd BPMBuddies
```

### 2. Create virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Clean dataset (if needed)
```bash
python src/clean_tracks.py
```

### 4. Run the Flask app
```bash
python app.py
```

The application will be available at http://127.0.0.1:5001/

## Dataset
The application uses the Spotify Dataset 1921–2020 with over 160,000 tracks. This dataset is cleaned using `src/clean_tracks.py` to:
- Remove rows with missing values
- Rename columns for clarity
- Convert duration from milliseconds to seconds
- Trim to 120,000 entries for optimal performance

## Algorithms Compared

### Greedy Algorithm
- Uses a min-heap to find the song closest to the target BPM for each interval
- Optimizes each interval independently
- Faster runtime (typically 5-6 seconds)
- Best for quick playlist generation

### Graph-based Algorithm
- Builds a layered graph with candidate songs for each interval
- Uses shortest path algorithm to find globally optimal transitions
- Slower runtime (typically 6-7 seconds)
- Produces smoother transitions between intervals


## Contributors
- [Akhil](https://github.com/akhilw0811)
- [Eesh] (https://github.com/eeshs)
- [Vishvath] (https://github.com/vishg13)
## Acknowledgments
- Spotify Dataset 1921–2020 from Kaggle
- Flask web framework
- NetworkX graph library 