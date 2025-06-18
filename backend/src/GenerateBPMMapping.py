import os
import librosa
import json


def generate_bpm_map(tabla_dataset_root: str = os.path.join("..", "tablaDataset"),
                     output_path: str = os.path.join("..", "src", "tablaDataset_bpm_map.json")) -> dict:
    """
    Scan the tabla dataset for loops and generate a BPM mapping JSON.
    Returns the BPM map dict.
    """
    bpm_map = {}
    print("🔍 Scanning tablaDataset folder for loops...")

    for root, dirs, files in os.walk(tabla_dataset_root):
        for file in files:
            if file.endswith((".wav", ".mp3")):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start=tabla_dataset_root)
                try:
                    y, sr = librosa.load(file_path, sr=None)
                    if len(y) < sr * 1:
                        print(f"⏭️ Skipped short file: {rel_path}")
                        continue
                    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
                    bpm_map[rel_path] = round(float(bpm), 2)
                    print(f"✅ {rel_path} → {bpm:.2f} BPM")
                except Exception as e:
                    print(f"⚠️ Failed for {rel_path}: {e}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(bpm_map, f, indent=2)

    print(f"\n💾 BPM map saved to: {output_path}")
    return bpm_map


if __name__ == "__main__":
    generate_bpm_map()