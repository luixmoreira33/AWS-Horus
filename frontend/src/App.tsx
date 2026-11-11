import React, { useState } from 'react';
import { GraphView } from './components/GraphView';
import { ResourcePanel } from './components/ResourcePanel';
import { Filters } from './components/Filters';

const sampleElements = [
  { data: { id: 'lambda1', label: 'my-function', color: '#FF9900' } },
  { data: { id: 'role1', label: 'lambda-role', color: '#DD344C' } },
  { data: { id: 'e1', source: 'lambda1', target: 'role1', evidence_level: 'DECLARADA', weight: 2 } },
];

export default function App() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div>
      <h1>AWS-Horus</h1>
      <Filters onFilterChange={(f) => console.log('filters', f)} />
      <GraphView elements={sampleElements} />
      {selected && (
        <ResourcePanel
          arn={selected}
          inbound={[]}
          outbound={[{ target: 'role1', category: 'IAM/AUTORIZAÇÃO', mechanism: 'iam-role', evidence_level: 'DECLARADA' }]}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}
