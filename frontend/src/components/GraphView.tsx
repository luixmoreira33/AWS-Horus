import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

interface Props {
  selectedArn: string | null;
  pathResult: any;
  onNodeClick: (arn: string) => void;
  filters: { category?: string; evidenceLevel?: string };
}

export default function GraphView({ selectedArn, pathResult, onNodeClick, filters }: Props) {
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
        { selector: '.compound', style: { 'background-opacity': 0.1, 'border-width': 2, 'border-color': '#475569' } },
      ],
      layout: { name: 'breadthfirst' },
    });

    cyRef.current.on('tap', 'node', (evt) => {
      const id = evt.target.id();
      if (!id.startsWith('compound-')) onNodeClick(id);
    });

    return () => cyRef.current?.destroy();
  }, []);

  useEffect(() => {
    if (!cyRef.current || !selectedArn) return;

    const load = async () => {
      const res = await fetch(`/resources/${encodeURIComponent(selectedArn)}/neighbors`);
      const data = await res.json();
      const cy = cyRef.current!;
      cy.elements().remove();

      // Agrupamento por camadas (Conta → Região → VPC)
      const compounds = new Map<string, string>();
      const addNode = (arn: string, label?: string) => {
        const parts = arn.split(':');
        const account = parts[4] || 'unknown';
        const region = parts[3] || 'global';
        const parent = `compound-${account}-${region}`;
        if (!compounds.has(parent)) {
          cy.add({ group: 'nodes', data: { id: parent, label: `${account} / ${region}` }, classes: 'compound' });
          compounds.set(parent, parent);
        }
        cy.add({ group: 'nodes', data: { id: arn, label: label || arn.split('/').pop(), parent } });
      };

      addNode(selectedArn, selectedArn.split('/').pop());
      [...(data.inbound || []), ...(data.outbound || [])].forEach((e: any) => {
        const other = e.source_arn === selectedArn ? e.target_arn : e.source_arn;
        if (filters.category && e.category !== filters.category) return;
        if (filters.evidenceLevel && e.evidence_level !== filters.evidenceLevel) return;
        addNode(other);
        cy.add({ group: 'edges', data: { source: e.source_arn, target: e.target_arn, category: e.category } });
      });

      cy.layout({ name: 'breadthfirst' }).run();
    };

    load();
  }, [selectedArn, filters]);

  useEffect(() => {
    if (!cyRef.current || !pathResult?.path) return;
    const cy = cyRef.current;
    cy.elements().removeClass('highlighted');
    pathResult.path.forEach((arn: string) => cy.getElementById(arn).addClass('highlighted'));
  }, [pathResult]);

  return <div ref={containerRef} className="w-full h-full" />;
}
