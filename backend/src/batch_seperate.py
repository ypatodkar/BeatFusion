import os
import subprocess
import shutil

SONGS_DIR = "../songs"  # Fixed folder path relative to Flask project root

def list_songs() -> list[str]:
    """
    Return a list of .mp3 and .wav files in the songs directory.
    """
    if not os.path.isdir(SONGS_DIR):
        return []
    return [f for f in os.listdir(SONGS_DIR)
            if f.lower().endswith((".mp3", ".wav"))]

def batch_separate(selected_song: str, demucs_model: str) -> str:
    """
    Run Demucs to separate stems for a given song and model.
    Returns the path to the separated output folder.
    """
    print(f"\n🚀1. Selected song: '{selected_song}', model: '{demucs_model}'\n")

    # Build full path to the song
    selected_song_path = os.path.join(SONGS_DIR, selected_song)

    if not os.path.isfile(selected_song_path):
        raise FileNotFoundError(f"❌ Song file not found: {selected_song_path}")

    # Define output folder
    output_folder = os.path.join("separated", demucs_model, os.path.splitext(selected_song)[0])
    os.makedirs(output_folder, exist_ok=True)

    print(f"\n🚀2. Running Demucs on: '{selected_song_path}'\n")

    # Run Demucs
    subprocess.run([
        "python", "-m", "demucs",
        "--name", demucs_model,
        "--out", "separated",   # use relative output path to keep things simple
        "-d", "mps",
        selected_song_path
    ], check=True)

    # Copy original song to output folder
    dest_path = os.path.join(output_folder, os.path.basename(selected_song_path))
    print(f"📂 Copying from: {selected_song_path} → {dest_path}")
    shutil.copy2(selected_song_path, dest_path)
    print(f"✅ Original song copied to: {dest_path}")

    print("\n📁 Final contents of output folder:")
    print(os.listdir(output_folder))

    return output_folder
