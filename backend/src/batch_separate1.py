import os
import subprocess
import shutil
from InquirerPy import prompt


def list_songs(songs_dir: str = "../Songs") -> list[str]:
    """
    Return a list of .mp3 and .wav files in the songs directory.
    """
    if not os.path.isdir(songs_dir):
        return []
    return [f for f in os.listdir(songs_dir)
            if f.lower().endswith((".mp3", ".wav"))]

def batch_separate(songs_dir: str = "../Songs",
                   demucs_model: str = None) -> str:
    """
    Interactively pick a song from the songs directory and run Demucs to separate stems.
    Returns the path to the separated output folder.
    """
    print(f"\n🚀 Song path'{songs_dir}' '{demucs_model}' .\n")

    # Discover all audio files
    audio_files = [f for f in os.listdir(songs_dir) if f.endswith((".mp3", ".wav"))]
    if not audio_files:
        raise FileNotFoundError("❌ No audio files found in the Songs folder.")

    # Let user pick a song
    song_answer = prompt([
        {"type": "list", "name": "song", "message": "🎵 Select a song to separate:", "choices": audio_files}
    ])
    selected_song = song_answer["song"]
    selected_song_path = os.path.join(songs_dir, selected_song)
    print(f"\n🚀 Song found'{selected_song_path}' '{demucs_model}' .\n")
    # Let user pick a Demucs model if not provided
    if demucs_model is None:
        model_answer = prompt([
            {"type": "list", "name": "model", "message": "🤖 Select Demucs model:",
             "choices": ["htdemucs_6s", "htdemucs", "mdx_extra_q", "mdx", "mdx_q"]}
        ])
        demucs_model = model_answer["model"]

    output_folder = os.path.join("..", "separated", demucs_model, os.path.splitext(selected_song)[0])
    os.makedirs(output_folder, exist_ok=True)

    # Run Demucs separation
    # print(f"\n🚀 Separating '{selected_song}' using model '{demucs_model}' with MPS acceleration...\n")
    subprocess.run([
        "python", "-m", "demucs",
        "--name", demucs_model,
        "--out", "../separated",
        "-d", "mps",
        selected_song_path
    ], check=True)

    # Copy original song to the output folder
    # Copy original song to the output folder
    dest_path = os.path.join(output_folder, os.path.basename(selected_song_path))
    print(f"📂 Copying from: {selected_song_path} → {dest_path}")
    shutil.copy2(selected_song_path, dest_path)
    print(f"✅ Original song copied to: {dest_path}")

    print("\n📁 Final contents of output folder:")
    print(os.listdir(output_folder))


    return output_folder


if __name__ == "__main__":
    batch_separate()





