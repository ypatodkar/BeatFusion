import librosa
import pretty_midi
import os

DEFAULT_MIDI_NOTE = 42  # Use same stroke for now (all tabla hits)
INPUT_ROOT = "../tablaDataset"
OUTPUT_ROOT = "tablaMidis"
os.makedirs(OUTPUT_ROOT, exist_ok=True)

def audio_to_midi(input_path, output_path):
    y, sr = librosa.load(input_path, sr=None)
    onset_times = librosa.onset.onset_detect(y=y, sr=sr, units='time')

    midi = pretty_midi.PrettyMIDI()
    drum_instr = pretty_midi.Instrument(program=0, is_drum=True)

    for t in onset_times:
        note = pretty_midi.Note(
            velocity=100,
            pitch=DEFAULT_MIDI_NOTE,
            start=t,
            end=t + 0.1
        )
        drum_instr.notes.append(note)

    midi.instruments.append(drum_instr)
    midi.write(output_path)

# Walk through each taal folder
for taal in os.listdir(INPUT_ROOT):
    taal_path = os.path.join(INPUT_ROOT, taal)
    if os.path.isdir(taal_path):
        output_taal_path = os.path.join(OUTPUT_ROOT, taal)
        os.makedirs(output_taal_path, exist_ok=True)

        for fname in os.listdir(taal_path):
            if fname.endswith(".wav"):
                in_file = os.path.join(taal_path, fname)
                out_file = os.path.join(output_taal_path, fname.replace(".wav", ".mid"))
                try:
                    audio_to_midi(in_file, out_file)
                    print(f"✅ Converted {fname} → {out_file}")
                except Exception as e:
                    print(f"❌ Error on {fname}: {e}")
