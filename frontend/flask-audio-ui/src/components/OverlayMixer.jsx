import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function OverlayMixer() {
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState('');
  const [mixType, setMixType] = useState('vocals+tabla');
  const [loadingSongs, setLoadingSongs] = useState(true);
  const [mixing, setMixing] = useState(false);
  const [error, setError] = useState('');
  const [resultPath, setResultPath] = useState(null);

  // Fetch available songs
  useEffect(() => {
    async function fetchSongs() {
      try {
        const res = await axios.get('/api/songs');
        // Expect res.data.songs = array of filenames
        const list = Array.isArray(res.data.songs) ? res.data.songs : res.data;
        setSongs(list);
      } catch (err) {
        console.error(err);
        setError('Failed to load songs');
      } finally {
        setLoadingSongs(false);
      }
    }
    fetchSongs();
  }, []);

  const handleMix = async () => {
    if (!selectedSong) {
      setError('Please select a song.');
      return;
    }
    setMixing(true);
    setError('');
    setResultPath(null);

    try {
      const payload = { song: selectedSong, mix: mixType };
      const res = await axios.post('/api/overlay', payload);
      setResultPath(res.data.output_path);
    } catch (err) {
      console.error(err);
      setError('Mixing failed');
    } finally {
      setMixing(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md space-y-4">
      <h2 className="text-xl font-semibold">Tabla Overlay Mixer</h2>

      {loadingSongs ? (
        <p>Loading songs...</p>
      ) : (
        <>
          <div>
            <label className="block mb-1 text-gray-700">Select Song</label>
            <select
              value={selectedSong}
              onChange={(e) => setSelectedSong(e.target.value)}
              className="block w-full p-2 border rounded"
            >
              <option value="" disabled>-- choose a song --</option>
              {songs.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-1 text-gray-700">Mix Type</label>
            <select
              value={mixType}
              onChange={(e) => setMixType(e.target.value)}
              className="block w-full p-2 border rounded"
            >
              <option value="vocals+tabla">Vocals + Tabla</option>
              <option value="vocals+piano+bass">Vocals + Piano + Bass</option>
            </select>
          </div>

          <button
            onClick={handleMix}
            disabled={mixing}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {mixing ? 'Mixing...' : 'Mix'}
          </button>
        </>
      )}

      {error && <p className="text-red-500">{error}</p>}
      {resultPath && (
        <p className="text-green-600">✅ Mixed file saved at: {resultPath}</p>
      )}
    </div>
  );
}
