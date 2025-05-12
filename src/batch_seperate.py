from InquirerPy import prompt
import os
import subprocess

# ----------- Step 1: Discover all audio files ----------
songs_dir = os.path.join("..", "Songs")
audio_files = [f for f in os.listdir(songs_dir) if f.endswith((".mp3", ".wav"))]

if not audio_files:
    print("❌ No audio files found in the Songs folder.")
    exit()

# ----------- Step 2: Let user pick a song ---------------
song_answer = prompt([
    {
        "type": "list",
        "name": "song",
        "message": "🎵 Which song do you want to separate?",
        "choices": audio_files,
    }
])
selected_song = song_answer["song"]
selected_song_path = os.path.join(songs_dir, selected_song)

# ----------- Step 3: Let user pick a model -------------
models = [
    "htdemucs",
    "htdemucs_6s",
    "mdx_extra",
    "mdx_extra_q",
    "demucs_quantized"
]

model_answer = prompt([
    {
        "type": "list",
        "name": "model",
        "message": "🧠 Choose a Demucs model:",
        "choices": models,
    }
])
selected_model = model_answer["model"]

# ----------- Step 4: Run Demucs -------------------------
print(f"\n🚀 Separating '{selected_song}' using model '{selected_model}'...\n")

subprocess.run([
    "python3", "-m", "demucs.separate",
    "--name", selected_model,
    selected_song_path
])

print(f"\n✅ Done! Find outputs in: ../separated/{selected_model}/{os.path.splitext(selected_song)[0]}/")
