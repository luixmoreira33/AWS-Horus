import React, { useState } from 'react';

interface Props { onSelect: (arn: string) => void }

export default function Filters({ onSelect }: Props) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const search = async () => {
    // const r = await fetch(`/search?q=${encodeURIComponent(query)}`);
    // setResults(await r.json());
    setResults([]);
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
      <div className="space-y-1">
        {results.map((r) => (
          <button key={r.arn} className="w-full text-left text-sm p-2 hover:bg-gray-800 rounded" onClick={() => onSelect(r.arn)}>
            {r.type}
          </button>
        ))}
      </div>
    </div>
  );
}
