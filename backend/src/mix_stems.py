import os
from pydub import AudioSegment


def mix_stems(song_name: str,
              remove_stem: str = "other",
              input_dir: str = None,
              output_path: str = None) -> str:
    """
    Mix all separated stems except the one to remove.
    Returns the path to the mixed output file.
    """
    if input_dir is None:
        input_dir = f"separated/htdemucs/{song_name}/"
    if output_path is None:
        output_path = f"output/{song_name}_no_{remove_stem}.wav"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    available_stems = ["vocals", "drums", "bass", "other"]
    stems_to_mix = [s for s in available_stems if s != remove_stem]

    # Load the first stem as the base
    base = stems_to_mix[0]
    combined = AudioSegment.from_file(os.path.join(input_dir, f"{base}.wav"))

    # Overlay remaining stems
    for stem in stems_to_mix[1:]:
        stem_file = os.path.join(input_dir, f"{stem}.wav")
        print(f"Overlaying: {stem_file}")
        audio = AudioSegment.from_file(stem_file)
        combined = combined.overlay(audio)

    combined.export(output_path, format="wav")
    print(f"✅ Exported: {output_path}")
    return output_path


if __name__ == "__main__":
    # Example usage
    mix_stems("NatinMarliMithi")