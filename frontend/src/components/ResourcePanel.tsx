import React from 'react';

interface EdgeInfo {
  target?: string;
  source?: string;
  category: string;
  mechanism: string;
  evidence_level: string;
  ports?: number[];
  protocol?: string;
}

interface Props {
  arn: string;
  inbound: EdgeInfo[];
  outbound: EdgeInfo[];
  onClose: () => void;
}

export function ResourcePanel({ arn, inbound, outbound, onClose }: Props) {
  return (
    <div style={{ position: 'fixed', right: 0, top: 0, width: 400, height: '100%', background: '#1e1e1e', color: '#fff', padding: 16, overflowY: 'auto' }}>
      <button onClick={onClose}>Fechar</button>
      <h3>{arn}</h3>
      <h4>Saída ({outbound.length})</h4>
      {outbound.map((e, i) => (
        <div key={i}>
          → {e.target} | {e.category} | {e.mechanism} | {e.evidence_level}
          {e.ports && ` | portas: ${e.ports.join(',')}`}
        </div>
      ))}
      <h4>Entrada ({inbound.length})</h4>
      {inbound.map((e, i) => (
        <div key={i}>
          ← {e.source} | {e.category} | {e.mechanism} | {e.evidence_level}
        </div>
      ))}
    </div>
  );
}
