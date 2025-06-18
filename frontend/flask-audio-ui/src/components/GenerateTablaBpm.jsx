import React, { useState } from 'react';
import axios from 'axios';

export default function GenerateTablaBpm() {
  const [root, setRoot] = useState('');
  const [output, setOutput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async e => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const res = await axios.post('/generate-tabla-bpm', { tabla_root: root, output_path: output });
      setResult(res.data);
    } catch(err) {
      setError(err.message);
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Generate Tabla BPM Map</h2>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input value={root} onChange={e=>setRoot(e.target.value)} type="text" placeholder="Tabla root (optional)" className="w-full p-2 border rounded" />
        <input value={output} onChange={e=>setOutput(e.target.value)} type="text" placeholder="Output JSON path (optional)" className="w-full p-2 border rounded" />
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded">
          {loading? 'Generating...' : 'Generate'}
        </button>
      </form>
      {error && <p className="text-red-500">{error}</p>}
      {result && <pre className="bg-gray-50 p-4 rounded overflow-auto">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
