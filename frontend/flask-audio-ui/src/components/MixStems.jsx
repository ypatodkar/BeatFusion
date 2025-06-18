import React, { useState } from 'react';
import axios from 'axios';

export default function MixStems() {
  const [song, setSong] = useState('');
  const [remove, setRemove] = useState('other');
  const [inputDir, setInputDir] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async e => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const res = await axios.post('/mix-stems', { song_name: song, remove_stem: remove, input_dir: inputDir }, { responseType: 'blob' });
      // download file
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${song}_no_${remove}.wav`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch(err) {
      setError(err.message);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Mix Stems</h2>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input value={song} onChange={e=>setSong(e.target.value)} type="text" placeholder="Song name" className="w-full p-2 border rounded" />
        <input value={inputDir} onChange={e=>setInputDir(e.target.value)} type="text" placeholder="Separated folder path" className="w-full p-2 border rounded" />
        <select value={remove} onChange={e=>setRemove(e.target.value)} className="block p-2 border rounded">
          <option value="vocals">vocals</option>
          <option value="drums">drums</option>
          <option value="bass">bass</option>
          <option value="other">other</option>
        </select>
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded">
          {loading? 'Mixing...' : 'Mix'}
        </button>
      </form>
      {error && <p className="text-red-500">{error}</p>}
    </div>
  )
}
