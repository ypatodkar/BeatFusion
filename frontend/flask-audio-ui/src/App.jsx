import React, { useState } from 'react';
import GenerateTablaBpm from './components/GenerateTablaBpm';
import GenerateBpmMap   from './components/GenerateBPM';
import BatchSeparate    from './components/BatchSeparate';
import MixStems         from './components/MixStems';
import UploadSong       from './components/UploadSongs';
import OverlayMixer from './components/OverlayMixer';


const tabs = [
  { id: 'tabla-bpm',    label: 'Generate Tabla BPM' },
  { id: 'bpm-map',      label: 'Generate BPM Map'   },
  { id: 'separate',     label: 'Batch Separate'      },
  { id: 'mix',          label: 'Mix Stems'           },
  { id: 'upload-songs', label: 'Upload Songs'        },  // <-- corrected label
  { id: 'overlay-mixer', label: 'Overlay Mixer'        },  // <-- corrected label
];

export default function App() {
  const [active, setActive] = useState(tabs[0].id);

  return (
    <div className="min-h-screen bg-gray-100 flex">
      <nav className="w-48 bg-white p-4 shadow">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            className={`block w-full text-left px-3 py-2 mb-2 rounded 
              ${active === tab.id 
                ? 'bg-blue-500 text-white' 
                : 'text-gray-700 hover:bg-gray-200'}`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="flex-1 p-6">
        {active === 'tabla-bpm'    && <GenerateTablaBpm />}
        {active === 'bpm-map'      && <GenerateBpmMap  />}
        {active === 'separate'     && <BatchSeparate  />}
        {active === 'mix'          && <MixStems       />}
        {active === 'upload-songs' && <UploadSong     />}  {/* <-- hook in UploadSong */}
        {active === 'overlay-mixer' && <OverlayMixer     />}  {/* <-- hook in UploadSong */}
      </main>
    </div>
  );
}
