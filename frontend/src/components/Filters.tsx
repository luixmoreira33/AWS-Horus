import React from 'react';

interface Props {
  onFilterChange: (filters: any) => void;
}

export function Filters({ onFilterChange }: Props) {
  return (
    <div style={{ padding: 8, background: '#f5f5f5' }}>
      <select onChange={e => onFilterChange({ account: e.target.value })}>
        <option value="">Todas as contas</option>
      </select>
      <select onChange={e => onFilterChange({ region: e.target.value })}>
        <option value="">Todas as regiões</option>
      </select>
      <select onChange={e => onFilterChange({ category: e.target.value })}>
        <option value="">Todas as categorias</option>
        <option value="REDE">REDE</option>
        <option value="IAM/AUTORIZAÇÃO">IAM</option>
        <option value="EVENTO/INTEGRAÇÃO">EVENTO</option>
      </select>
      <select onChange={e => onFilterChange({ evidence: e.target.value })}>
        <option value="">Todos os níveis</option>
        <option value="DECLARADA">Declarada</option>
        <option value="PERMITIDA">Permitida</option>
        <option value="OBSERVADA">Observada</option>
      </select>
    </div>
  );
}
