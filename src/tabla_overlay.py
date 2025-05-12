import os
import json
import random
import numpy as np
from pydub import AudioSegment
import librosa

# --- Paths ---
songs_dir = "../Songs"
tabla_root = "../tablaDataset"
tabla_bpm_json_path = "../src/tablaDataset_bpm_map.json"
output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

# --- Robust BPM detection ---
def smart_librosa_bpm_and_beats(path, verbose=True):
    y, sr = librosa.load(path)
    _, y_perc = librosa.effects.hpss(y)
    hop = 256

    tempo_raw, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sr, hop_length=hop)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop)

    if len(beat_times) > 1:
        intervals = np.diff(beat_times)
        inferred_bpm = 60. / np.mean(intervals)
    else:
        inferred_bpm = tempo_raw.item() if hasattr(tempo_raw, "item") else float(tempo_raw)

    # Adjust if clearly misread
    if inferred_bpm > 130:
        adjusted_bpm = inferred_bpm / 2
    elif inferred_bpm < 70:
        adjusted_bpm = inferred_bpm * 2
    else:
        adjusted_bpm = inferred_bpm

    if verbose:
        raw = tempo_raw.item() if hasattr(tempo_raw, "item") else float(tempo_raw)
        print(f"🎧 Raw tempo: {raw:.2f}")
        print(f"🧠 Inferred BPM: {inferred_bpm:.2f}")
        print(f"🎯 Adjusted BPM: {adjusted_bpm:.2f}")
        print(f"📍 Beat count: {len(beat_times)}")

    return adjusted_bpm, beat_times

# --- Suggest Taal by BPM ---
def suggest_taal_and_cycle(bpm):
    if bpm < 90:
        return "Dadra", 6
    elif bpm < 110:
        return "Roopak", 7
    elif bpm < 130:
        return "Keharwa", 8
    else:
        return "TeenTaal", 16

# --- Load tabla loop matches ---
def get_matching_tabla_loops(song_bpm, tolerance=4.0):
    with open(tabla_bpm_json_path, "r") as f:
        bpm_map = json.load(f)

    matches = {}
    for path, bpm in bpm_map.items():
        if abs(bpm - song_bpm) <= tolerance:
            taal = path.split("/")[0]
            matches.setdefault(taal, []).append(path)
    return matches

# --- Overlay tabla loops on beat cycles ---
def overlay_tabla(song_path):
    print(f"\n🎵 Loading: {song_path}")
    base_audio = AudioSegment.from_file(song_path)
    song_name = os.path.splitext(os.path.basename(song_path))[0]

    bpm, beat_times = smart_librosa_bpm_and_beats(song_path)
    beat_ms = (np.array(beat_times) * 1000).astype(int)
    
    taal, cycle_beats = suggest_taal_and_cycle(bpm)
    tabla_matches = get_matching_tabla_loops(bpm)

    if taal.lower() in tabla_matches:
        selected_taal = taal.lower()
    elif tabla_matches:
        selected_taal = max(tabla_matches.items(), key=lambda kv: len(kv[1]))[0]
        print(f"⚠️ Falling back to closest taal: {selected_taal}")
    else:
        raise SystemExit("❌ No tabla loops found near this BPM.")

    tabla_paths = tabla_matches[selected_taal]
    print(f"🪘 Using loops from '{selected_taal}' ({len(tabla_paths)} options)")

    tabla_track = AudioSegment.silent(duration=len(base_audio))

    if len(beat_ms) < cycle_beats + 1:
        raise SystemExit("❌ Not enough beats to form a single cycle.")

    for i in range(0, len(beat_ms) - cycle_beats, cycle_beats):
        start = beat_ms[i]
        end = beat_ms[i + cycle_beats]
        duration = end - start

        loop_path = random.choice(tabla_paths)
        full_path = os.path.join(tabla_root, loop_path)
        tabla = AudioSegment.from_file(full_path)

        if len(tabla) < duration:
            continue

        tabla_cycle = tabla[:duration]
        tabla_track = tabla_track.overlay(tabla_cycle, position=start)

    # Mix and export
    final = base_audio.overlay(tabla_track)
    out_path = os.path.join(output_dir, f"with_new_tabla_{song_name}.wav")
    final.export(out_path, format="wav")
    print(f"✅ Saved → {out_path}")

# --- Run ---
if __name__ == "__main__":
    all_songs = [f for f in os.listdir(songs_dir) if f.endswith((".mp3", ".wav"))]
    if not all_songs:
        print("❌ No songs found in Songs folder.")
        exit()

    print("\n🎧 Select a song:")
    for i, s in enumerate(all_songs):
        print(f"{i+1}. {s}")
    choice = int(input("Enter number: ")) - 1
    selected_path = os.path.join(songs_dir, all_songs[choice])

    overlay_tabla(selected_path)
