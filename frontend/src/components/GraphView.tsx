import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import elk from 'cytoscape-elk';

cytoscape.use(elk);

interface Props {
  elements: any[];
}

export function GraphView({ elements }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    cyRef.current = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        { selector: 'node', style: { 'label': 'data(label)', 'background-color': 'data(color)', 'width': 40, 'height': 40 } },
        { selector: 'edge[evidence_level = "OBSERVADA"]', style: { 'line-style': 'solid', 'width': 'data(weight)', 'target-arrow-shape': 'triangle' } },
        { selector: 'edge[evidence_level = "PERMITIDA"]', style: { 'line-style': 'dashed', 'target-arrow-shape': 'triangle' } },
        { selector: 'edge', style: { 'curve-style': 'bezier' } }
      ],
      layout: { name: 'elk', elk: { algorithm: 'layered' } }
    });
    return () => cyRef.current?.destroy();
  }, [elements]);

  return <div ref={containerRef} style={{ width: '100%', height: '600px' }} />;
}
