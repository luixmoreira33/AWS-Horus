import React, { useState } from 'react';

interface Props {
  onSelect: (arn: string) => void;
  onFilterChange: (filters: { category?: string; evidenceLevel?: string }) => void;
}

export default function Filters({ onSelect, onFilterChange }: Props) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [category, setCategory] = useState('');
  const [evidenceLevel, setEvidenceLevel] = useState('');

  const search = async () => {
    const r = await fetch(`/search?q=${encodeURIComponent(query)}`);
    const data = await r.json();
    setResults(data.results || []);
  };

  const applyFilters = () => {
    onFilterChange({
      category: category || undefined,
      evidenceLevel: evidenceLevel || undefined,
    });
  };

  return (
    <div>
      <input
        className="w-full bg-gray-800 p-2 rounded mb-2"
        placeholder="Buscar por ARN ou tipo"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && search()}
      />
      <div className="space-y-1 mb-4">
        {results.map((r) => (
          <button key={r.arn} className="w-full text-left text-sm p-2 hover:bg-gray-800 rounded" onClick={() => onSelect(r.arn)}>
            {r.type || r.arn.split('/').pop()}
          </button>
        ))}
      </div>

      <h3 className="text-sm font-semibold mb-2">Filtros</h3>
      <select className="w-full bg-gray-800 p-2 rounded mb-2" value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="">Todas categorias</option>
        <option value="REDE">Rede</option>
        <option value="IAM/AUTORIZAÇÃO">IAM</option>
        <option value="CRIPTOGRAFIA">Criptografia</option>
        <option value="EVENTO/INTEGRAÇÃO">Evento</option>
        <option value="DADOS">Dados</option>
      </select>
      <select className="w-full bg-gray-800 p-2 rounded mb-2" value={evidenceLevel} onChange={(e) => setEvidenceLevel(e.target.value)}>
        <option value="">Todos níveis</option>
        <option value="DECLARADA">Declarada</option>
        <option value="PERMITIDA">Permitida</option>
        <option value="OBSERVADA">Observada</option>
      </select>
      <button className="w-full bg-gray-700 py-1 rounded text-sm" onClick={applyFilters}>Aplicar filtros</button>
    </div>
  );
}
