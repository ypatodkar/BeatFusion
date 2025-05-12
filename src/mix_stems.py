from pydub import AudioSegment
import os

# CONFIGURATION
song_name = "NatinMarliMithi"
remove_stem = "other"

input_path = f"separated/htdemucs/{song_name}/"
output_path = f"output/{song_name}_no_{remove_stem}.wav"

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Define stems to load
available_stems = ["vocals", "drums", "bass", "other"]
stems_to_mix = [s for s in available_stems if s != remove_stem]

# Load the first stem as the base
base_stem = stems_to_mix[0]
combined = AudioSegment.from_file(os.path.join(input_path, f"{base_stem}.wav"))

# Overlay remaining stems
for stem in stems_to_mix[1:]:
    stem_path = os.path.join(input_path, f"{stem}.wav")
    print(f"Overlaying: {stem_path}")
    audio = AudioSegment.from_file(stem_path)
    combined = combined.overlay(audio)

# Export the final mix
combined.export(output_path, format="wav")
print(f"✅ Exported: {output_path}")
