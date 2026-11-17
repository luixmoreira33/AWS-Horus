import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

interface Props {
  selectedArn: string | null;
  pathResult: any;
  onNodeClick: (arn: string) => void;
}

export default function GraphView({ selectedArn, pathResult, onNodeClick }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    cyRef.current = cytoscape({
      container: containerRef.current,
      style: [
        { selector: 'node', style: { 'background-color': '#3b82f6', label: 'data(label)', 'font-size': 10 } },
        { selector: 'edge', style: { 'line-color': '#64748b', 'target-arrow-color': '#64748b', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' } },
        { selector: '.highlighted', style: { 'background-color': '#f59e0b', 'line-color': '#f59e0b' } },
      ],
      layout: { name: 'breadthfirst' },
    });

    cyRef.current.on('tap', 'node', (evt) => {
      onNodeClick(evt.target.id());
    });

    return () => cyRef.current?.destroy();
  }, []);

  useEffect(() => {
    if (!cyRef.current || !selectedArn) return;
    // Em produção: fetch neighbors e adicionar nós/arestas
  }, [selectedArn]);

  return <div ref={containerRef} className="w-full h-full" />;
}
