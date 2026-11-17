import React, { useEffect, useState } from 'react';

interface Props { arn: string | null }

export default function ResourcePanel({ arn }: Props) {
  const [neighbors, setNeighbors] = useState<any>(null);

  useEffect(() => {
    if (!arn) return;
    fetch(`/resources/${encodeURIComponent(arn)}/neighbors`)
      .then(r => r.json())
      .then(setNeighbors)
      .catch(() => setNeighbors({ inbound: [], outbound: [] }));
  }, [arn]);

  if (!arn) return <div className="p-4 text-gray-500">Selecione um recurso</div>;

  return (
    <div className="p-4 overflow-auto h-full">
      <h2 className="text-lg font-semibold break-all mb-4">{arn.split('/').pop()}</h2>
      <p className="text-xs text-gray-400 mb-4 break-all">{arn}</p>

      <h3 className="font-medium mb-2">Entrada</h3>
      {(neighbors?.inbound || []).map((e: any) => (
        <div key={e.source_arn + e.mechanism} className="text-sm mb-1 p-2 bg-gray-800 rounded">
          <div className="break-all">{e.source_arn}</div>
          <div className="text-xs text-gray-400">{e.category} · {e.evidence_level}</div>
        </div>
      ))}

      <h3 className="font-medium mt-4 mb-2">Saída</h3>
      {(neighbors?.outbound || []).map((e: any) => (
        <div key={e.target_arn + e.mechanism} className="text-sm mb-1 p-2 bg-gray-800 rounded">
          <div className="break-all">{e.target_arn}</div>
          <div className="text-xs text-gray-400">{e.category} · {e.evidence_level}</div>
        </div>
      ))}
    </div>
  );
}
