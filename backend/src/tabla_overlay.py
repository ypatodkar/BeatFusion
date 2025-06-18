import os
import json
import random
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range
import librosa

# --- Configuration ---
app = Flask(__name__)
CORS(app)

SEPARATED_ROOT = "separated"
TABLA_ROOT = "../tablaDataset"
TABLA_BPM_JSON = "tablaDataset_bpm_map.json"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def smart_librosa_bpm_and_beats(path):
    y, sr = librosa.load(path, mono=True)
    _, y_perc = librosa.effects.hpss(y)
    hop = 256
    tempo_raw, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sr, hop_length=hop)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop)
    if len(beat_times) > 1:
        intervals = np.diff(beat_times)
        inferred_bpm = 60.0 / np.mean(intervals)
    else:
        inferred_bpm = float(tempo_raw)
    if inferred_bpm > 130:
        adjusted_bpm = inferred_bpm / 2
    elif inferred_bpm < 70:
        adjusted_bpm = inferred_bpm * 2
    else:
        adjusted_bpm = inferred_bpm
    return adjusted_bpm, beat_times


def suggest_taal_and_cycle(bpm):
    if bpm < 85:
        return "dadra", 6
    elif bpm < 95:
        return "bhajani", 8
    elif bpm < 105:
        return "rupak", 7
    elif bpm < 115:
        return "keharwa", 8
    elif bpm < 125:
        return "deepchandi", 14
    elif bpm < 130:
        return "ektal", 12
    elif bpm < 135:
        return "jhaptal", 10
    elif bpm < 140:
        return "trital", 16
    else:
        return "addhatrital", 16
    
def get_matching_tabla_loops(song_bpm: float,
                             tolerance: float = 4.0):
    with open(TABLA_BPM_JSON, "r") as f:
        bpm_map = json.load(f)

    def _filter(strict=True):
        matches = {}
        for path, bpm in bpm_map.items():
            if bpm >= 100:
                taal = path.split('/')[0].lower()
                matches.setdefault(taal, []).append(path)
        return matches

    matches = _filter(strict=True)
    if not matches:
        print(f"⚠️ No strict matches for BPM {song_bpm}, falling back to any tabla loop ≥ 100 BPM")
        matches = _filter(strict=False)

    if not matches:
        raise Exception(f"No tabla loops found with BPM ≥ 100 at all.")

    return matches


def overlay_tabla(song_name, mix_type, model='htdemucs_6s'):
    song_base = os.path.splitext(song_name)[0]
    stem_dir = os.path.join(SEPARATED_ROOT, model, song_base)
    if not os.path.isdir(stem_dir):
        raise FileNotFoundError(f"Stems not found for '{song_name}' at {stem_dir}")

    base_file = os.path.join(stem_dir, 'vocals.wav')
    if not os.path.isfile(base_file):
        raise FileNotFoundError(f"Vocals stem missing at {base_file}")
    base_audio = AudioSegment.from_file(base_file)

    if mix_type == 'vocals+piano+bass':
        for stem in ['piano', 'bass', 'vocals']:
            path = os.path.join(stem_dir, f"{stem}.wav")
            if os.path.isfile(path):
                base_audio = base_audio.overlay(AudioSegment.from_file(path))

    bpm, beat_times = smart_librosa_bpm_and_beats(base_file)
    beat_ms = (np.array(beat_times) * 1000).astype(int)

    tabla_matches = get_matching_tabla_loops(bpm)
    taal, cycle = suggest_taal_and_cycle(bpm)

    if taal in tabla_matches:
        chosen = taal
    elif tabla_matches:
        chosen = max(tabla_matches, key=lambda t: len(tabla_matches[t]))
    else:
        raise Exception("No tabla loops found near this BPM")

    loops = tabla_matches[chosen]
    tabla_track = AudioSegment.silent(duration=len(base_audio))
    used_loops = []

    group_size = 4  # number of cycles to repeat same loop

    i = 0
    while i + cycle * group_size <= len(beat_ms):
        loop_rel = random.choice(loops)  # use same loop for the group
        loop_path = os.path.join(TABLA_ROOT, loop_rel)
        tabla = AudioSegment.from_file(loop_path)
        tabla = compress_dynamic_range(tabla, threshold=-20.0, ratio=2.0)

        for j in range(group_size):
            start_idx = i + j * cycle
            start_ms = beat_ms[start_idx]
            end_ms = beat_ms[start_idx + cycle]
            duration_ms = end_ms - start_ms

            if len(tabla) < duration_ms:
                continue

            tabla_segment = tabla[:duration_ms]
            tabla_track = tabla_track.overlay(tabla_segment, position=start_ms)
            used_loops.append((loop_rel, start_ms, duration_ms))

        i += cycle * group_size


    mix_audio = base_audio.overlay(tabla_track)
    out_name = f"with_tabla_{song_name}.wav"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    mix_audio.export(out_path, format='wav')

    log_file = os.path.join(OUTPUT_DIR, 'used_loops.txt')
    timestamp = datetime.now().isoformat()
    with open(log_file, 'a') as lf:
        lf.write(f"[{timestamp}] {song_name}: {taal}\n")
        for loop_file, start, dur in used_loops:
            lf.write(f"- {loop_file} @ {start}ms for {dur}ms\n")
        lf.write("\n")

    return out_path



if __name__ == '__main__':
    app.run(debug=True)
