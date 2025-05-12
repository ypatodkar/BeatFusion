import os
import librosa
import json

tabla_dataset_root = os.path.join("..", "tablaDataset")  # adjust if script is in src/
bpm_map = {}

print("🔍 Scanning tablaDataset folder for loops...")

for root, dirs, files in os.walk(tabla_dataset_root):
    for file in files:
        if file.endswith((".wav", ".mp3")):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, start=tabla_dataset_root)
            try:
                y, sr = librosa.load(file_path, sr=None)
                duration = librosa.get_duration(y=y, sr=sr)
                if duration < 1.0:
                    print(f"⏭️ Skipped short file: {rel_path}")
                    continue
                bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
                bpm_map[rel_path] = round(float(bpm), 2)
                print(f"✅ {rel_path} → {bpm:.2f} BPM")
            except Exception as e:
                print(f"⚠️ Failed for {rel_path}: {e}")

# Save JSON to src or current dir
output_path = os.path.join("..", "src", "tablaDataset_bpm_map.json")
with open(output_path, "w") as f:
    json.dump(bpm_map, f, indent=2)

print(f"\n💾 BPM map saved to: {output_path}")
