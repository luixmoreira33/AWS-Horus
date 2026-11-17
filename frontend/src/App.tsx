import React, { useState } from 'react';
import GraphView from './components/GraphView';
import ResourcePanel from './components/ResourcePanel';
import Filters from './components/Filters';

export default function App() {
  const [selectedArn, setSelectedArn] = useState<string | null>(null);
  const [pathResult, setPathResult] = useState<any>(null);
  const [filters, setFilters] = useState<{ category?: string; evidenceLevel?: string }>({});
  const [fromArn, setFromArn] = useState('');
  const [toArn, setToArn] = useState('');

  const findPath = async () => {
    const res = await fetch('/path', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ from_arn: fromArn, to_arn: toArn }),
    });
    if (res.ok) setPathResult(await res.json());
    else setPathResult({ found: false });
  };

  const exportMermaid = () => {
    // Em produção: gerar Mermaid a partir dos nós visíveis
    const mermaid = `graph TD\n  A[Recurso] --> B[Vizinho]`;
    const blob = new Blob([mermaid], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'horus-graph.mmd';
    a.click();
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      <div className="w-80 border-r border-gray-800 p-4 overflow-auto">
        <h1 className="text-xl font-bold mb-4">AWS-Horus</h1>
        <Filters onSelect={setSelectedArn} onFilterChange={setFilters} />
        <div className="mt-6">
          <h2 className="text-sm font-semibold mb-2">Como A chega em B?</h2>
          <input className="w-full bg-gray-800 p-2 rounded mb-2" placeholder="ARN origem" value={fromArn} onChange={(e) => setFromArn(e.target.value)} />
          <input className="w-full bg-gray-800 p-2 rounded mb-2" placeholder="ARN destino" value={toArn} onChange={(e) => setToArn(e.target.value)} />
          <button className="w-full bg-blue-600 py-2 rounded mb-2" onClick={findPath}>Buscar caminho</button>
          <button className="w-full bg-gray-700 py-2 rounded text-sm" onClick={exportMermaid}>Exportar Mermaid</button>
        </div>
      </div>
      <div className="flex-1 relative">
        <GraphView selectedArn={selectedArn} pathResult={pathResult} onNodeClick={setSelectedArn} filters={filters} />
      </div>
      <div className="w-96 border-l border-gray-800">
        <ResourcePanel arn={selectedArn} />
      </div>
    </div>
  );
}
