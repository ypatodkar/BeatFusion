
# BeatFusion

_Beat‑aware AI that lets you **separate**, **edit**, and **blend** tabla rhythms with any song right in your browser._

---

<table>
<tr><td><strong>⭐ Why BeatFusion?</strong></td></tr>
<tr><td>

* **Instant stem separation** – powered by <a href="https://github.com/facebookresearch/demucs">Demucs</a> to isolate drums, bass, vocals & more.  
* **One‑click tabla overlay** – choose from 500+ professionally recorded loops (Dadra, Keharwa, Teen‑Taal, etc.) or upload your own.  
* **Beat‑synchronised mixing** – alignment algorithm locks tabla bols to the song’s tempo and groove.  
* **Web‑first workflow** – React + WaveSurfer.js give a DAW‑like waveform editor in the browser.  
* **Open source & extendable** – clean Flask API, pluggable ML models, MIT‑licensed.

</td></tr>
</table>



---

## Architecture

```
frontend/          # React + Vite + Tailwind
├─ src/
│  ├─ components/  # Waveform, StemTrack, LoopBrowser...
│  └─ pages/       # UploadPage, EditorPage
└─ ...

backend/
├─ app.py          # Flask entry‑point
├─ separater.py    # Demucs wrapper
├─ overlay.py      # Time‑stretch & mix‑down utilities
└─ loops/          # Curated tabla stems (.wav)
```

### Audio pipeline

1. **Upload** → file saved to `/tmp`  
2. **/separate** → `separater.py` calls Demucs, returns stem URLs  
3. **/overlay** → `overlay.py` time‑stretches & mixes the chosen tabla loop  
4. Result delivered as a streaming `.wav` / `.mp3`

### Front‑end stack

| Feature                    | Library |
| -------------------------- | ------- |
| Waveform display           | `wavesurfer.js` |
| Playback & scheduling      | `tone.js` |
| State / data‑fetching      | `react‑query` |
| Styling & layout           | Tailwind CSS |

---

## Quick start

### 1. Clone & install

```bash
git clone https://github.com/ypatodkar/BeatFusion.git
cd BeatFusion
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt           # Flask, Demucs, librosa, ...
cd frontend
npm install                                # React deps
```

### 2. Run the dev stack

```bash
# Terminal 1
cd backend
python app.py                             # http://127.0.0.1:5000

# Terminal 2
cd frontend
npm run dev                               # http://localhost:5173
```

Open the web app, drag‑and‑drop a song, click **Separate**, then audition tabla loops until you’re happy with the blend!

---

## REST API (excerpt)

| Method | Endpoint            | Description                                |
| ------ | ------------------- | ------------------------------------------ |
| POST   | `/upload`           | Multipart audio → returns `song_id`.       |
| POST   | `/separate/<id>`    | Runs Demucs → returns list of stems.       |
| GET    | `/stems/<id>`       | Streams a specific stem.                   |
| POST   | `/overlay`          | `{ song_id, stem, loop_name } → mixed WAV` |
| GET    | `/loops`            | Lists available tabla loops.               |

OpenAPI / Swagger docs: `http://localhost:5000/docs`.

---

## Roadmap

- [ ] **Smart loop suggestion** – LSTM / MusicGen model to generate bols that match melody.  
- [ ] **Beat‑grid editing** – drag stems on a timeline, quantise to grid.  
- [ ] **Export stems separately** – download individual tabla / vocals / drums tracks.  
- [ ] **Docker image** – one‑shot deployment.

---

## Contributing

Pull requests are welcome!  
Please file an issue before working on large changes.

1. Fork → `git checkout -b feat/my-awesome-change`  
2. Run `pre-commit install` (black + isort)  
3. Add unit tests (`pytest`) where possible.

---

## License

MIT © 2025 [Yash Patodkar](https://github.com/ypatodkar)

---

> _“Rhythm is a language; BeatFusion lets your code speak it.”_
