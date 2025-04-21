#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, session, send_file
import csv
import io
import time
from src.greedy_selector import generate_playlist as greedy_generate_playlist
from src.graph_selector import generate_playlist as graph_generate_playlist

app = Flask(__name__)
app.secret_key = 'workout_music_creator_secret_key'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate/<method>', methods=['POST'])
def generate(method):
    if method not in ['greedy', 'graph']:
        return redirect(url_for('index'))
    
    intervals = []
    i = 0
    
    while True:
        bpm_key = f'bpm_{i}'
        duration_key = f'duration_{i}'
        energy_key = f'energy_{i}'
        
        if bpm_key not in request.form or duration_key not in request.form:
            break
        
        bpm = request.form.get(bpm_key)
        duration = request.form.get(duration_key)
        energy = request.form.get(energy_key)
        
        if not bpm or not duration:
            return redirect(url_for('index'))
        
        try:
            bpm = int(bpm)
            duration = int(duration)
            
            if bpm <= 0 or duration <= 0:
                return redirect(url_for('index'))
            
            interval = {
                'bpm': bpm,
                'duration': duration
            }
            
            if energy:
                try:
                    energy = float(energy)
                    if 0 <= energy <= 1:
                        interval['energy'] = energy
                except ValueError:
                    return redirect(url_for('index'))
            
            intervals.append(interval)
            i += 1
            
        except ValueError:
            return redirect(url_for('index'))
    
    if not intervals:
        return redirect(url_for('index'))
    
    start_time = time.perf_counter()
    
    if method == 'greedy':
        playlist = greedy_generate_playlist(intervals)
    else:
        playlist = graph_generate_playlist(intervals)
    
    end_time = time.perf_counter()
    runtime = end_time - start_time
    
    session['playlist'] = playlist
    
    return render_template('playlist.html', 
                          playlist=playlist, 
                          method=method, 
                          runtime=runtime)

@app.route('/download', methods=['GET'])
def download():
    if 'playlist' not in session:
        return redirect(url_for('index'))
    
    playlist = session['playlist']
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Interval', 'Title', 'Artist', 'BPM', 'Energy', 'Duration (sec)', 'BPM Diff'])
    
    for track in playlist:
        writer.writerow([
            track['interval_number'],
            track['title'],
            track['artist'],
            track['bpm'],
            track['energy'],
            track['duration_sec'],
            track['bpm_diff']
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='workout_playlist.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=True) 