import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function BatchSeparate() {
  const [songs, setSongs] = useState([]);
  const [selectedSong, setSelectedSong] = useState('');
  const [model, setModel] = useState('htdemucs_6s');
  const [result, setResult] = useState(null);
  const [loadingSongs, setLoadingSongs] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch available songs
  useEffect(() => {
    async function fetchSongs() {
      try {
        const res = await axios.get('/api/songs');
        console.log('got /api/songs →', res.data);

        // Normalize response to an array
        const list = Array.isArray(res.data)
          ? res.data
          : Array.isArray(res.data.songs)
            ? res.data.songs
            : [];
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedSong) {
      setError('Please select a song.');
      return;
    }
    setLoading(true);
    setError('');
    setResult(null);

    try {
      console.log("Selected song: ",selectedSong, " Model : ",model)
      const res = await axios.post('/api/batch-separate', { song: selectedSong, model });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError('Separation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md space-y-4">
      <h2 className="text-xl font-semibold">Batch Separate Stems</h2>

      {loadingSongs ? (
        <p>Loading songs...</p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-gray-700">Select Song</label>
            <select
              value={selectedSong}
              onChange={(e) => setSelectedSong(e.target.value)}
              className="block w-full p-2 border rounded"
            >
              <option value="" disabled>
                -- choose a song --
              </option>
              {songs.map((song) => (
                <option key={song} value={song}>
                  {song}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-1 text-gray-700">Select Model</label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="block w-full p-2 border rounded"
            >
              <option value="htdemucs_6s">htdemucs_6s</option>
              <option value="htdemucs">htdemucs</option>
              <option value="mdx_extra_q">mdx_extra_q</option>
              <option value="mdx">mdx</option>
              <option value="mdx_q">mdx_q</option>
              <option value="spleeter">spleeter</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {loading ? 'Separating...' : 'Separate'}
          </button>
        </form>
      )}

      {error && <p className="text-red-500">{error}</p>}
      {result && (
        <pre className="bg-gray-100 p-4 rounded">
          Separated Folder: {result.output_folder}
        </pre>
      )}
    </div>
  );
}
