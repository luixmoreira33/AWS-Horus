import React, { useState } from 'react';
import GraphView from './components/GraphView';
import ResourcePanel from './components/ResourcePanel';
import Filters from './components/Filters';

export default function App() {
  const [selectedArn, setSelectedArn] = useState<string | null>(null);
  const [pathResult, setPathResult] = useState<any>(null);

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      <div className="w-80 border-r border-gray-800 p-4">
        <h1 className="text-xl font-bold mb-4">AWS-Horus</h1>
        <Filters onSelect={setSelectedArn} />
        <div className="mt-6">
          <h2 className="text-sm font-semibold mb-2">Como A chega em B?</h2>
          <input className="w-full bg-gray-800 p-2 rounded mb-2" placeholder="ARN origem" />
          <input className="w-full bg-gray-800 p-2 rounded mb-2" placeholder="ARN destino" />
          <button className="w-full bg-blue-600 py-2 rounded">Buscar caminho</button>
        </div>
      </div>
      <div className="flex-1 relative">
        <GraphView selectedArn={selectedArn} pathResult={pathResult} onNodeClick={setSelectedArn} />
      </div>
      <div className="w-96 border-l border-gray-800">
        <ResourcePanel arn={selectedArn} />
      </div>
    </div>
  );
}
