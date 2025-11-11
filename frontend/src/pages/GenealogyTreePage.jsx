import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGetGenealogy } from '../hooks/usePropagations';
import * as d3 from 'd3';

const GenealogyTreePage = () => {
  const navigate = useNavigate();
  const [plantId, setPlantId] = useState(null);
  const [treeData, setTreeData] = useState(null);
  const svgRef = useRef();
  const { data: genealogy } = useGetGenealogy(plantId);

  const statusColors = {
    'pending': '#fcd34d',
    'rooting': '#93c5fd',
    'rooted': '#86efac',
    'growing': '#86efac',
    'ready-to-pot': '#bfef45',
    'potted': '#a3f0b5',
    'transplanted': '#7dd3fc',
    'established': '#4ade80',
    'failed': '#fca5a5',
    'abandoned': '#d1d5db',
  };

  // Transformer les données généalogie en structure d'arbre D3
  useEffect(() => {
    if (genealogy) {
      const buildTree = (node, depth = 0) => {
        return {
          id: node.id,
          name: node.name,
          status: node.status || 'unknown',
          propagation_id: node.propagation_id,
          children: node.children ? node.children.map(child => buildTree(child, depth + 1)) : [],
        };
      };

      setTreeData(buildTree(genealogy));
    }
  }, [genealogy]);

  // Rendu du graphique D3
  useEffect(() => {
    if (!treeData || !svgRef.current) return;

    const width = svgRef.current.clientWidth;
    const height = Math.max(600, treeData.children.length * 150 + 300);

    // Nettoyer les anciens éléments
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .style('border', '1px solid #e5e7eb');

    const g = svg.append('g')
      .attr('transform', `translate(${width / 2},40)`);

    // Configuration de la disposition en arbre
    const tree = d3.tree().size([width - 100, height - 100]);
    const hierarchy = d3.hierarchy(treeData);
    const root = tree(hierarchy);

    // Liens (lignes entre parents et enfants)
    g.selectAll('.link')
      .data(root.links())
      .enter().append('path')
      .attr('class', 'link')
      .attr('d', d3.linkVertical()
        .x(d => d.x)
        .y(d => d.y))
      .style('stroke', '#d1d5db')
      .style('stroke-width', 2)
      .style('fill', 'none');

    // Groupes nœuds
    const node = g.selectAll('.node')
      .data(root.descendants())
      .enter().append('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.x},${d.y})`);

    // Cercles nœuds
    node.append('circle')
      .attr('r', 25)
      .style('fill', d => statusColors[d.data.status] || '#e5e7eb')
      .style('stroke', '#374151')
      .style('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', d => {
        if (d.data.propagation_id) {
          navigate(`/propagations/${d.data.propagation_id}`);
        }
      })
      .on('mouseover', function() {
        d3.select(this)
          .style('stroke-width', 3)
          .style('stroke', '#1f2937');
      })
      .on('mouseout', function() {
        d3.select(this)
          .style('stroke-width', 2)
          .style('stroke', '#374151');
      });

    // Texte des nœuds
    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.3em')
      .style('font-size', '11px')
      .style('font-weight', 'bold')
      .style('pointer-events', 'none')
      .text(d => d.data.name.substring(0, 15));

    // Labels de status sous les nœuds
    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '3em')
      .style('font-size', '10px')
      .style('fill', '#6b7280')
      .style('pointer-events', 'none')
      .text(d => d.data.status.substring(0, 12));

  }, [treeData, navigate]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Arbre Généalogique</h1>
          <p className="text-gray-600 mt-2">Visualisez les relations parent-enfant entre propagations</p>
        </div>

        {/* Plant Selection */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Sélectionner une plante de départ:
          </label>
          <p className="text-sm text-gray-600 mb-4">
            Actuellement: {treeData ? treeData.name : 'Aucune sélection'}
          </p>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/plants')}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Choisir une plante
            </button>
            {plantId && (
              <button
                onClick={() => {
                  setPlantId(null);
                  setTreeData(null);
                }}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
              >
                Réinitialiser
              </button>
            )}
          </div>
        </div>

        {/* Legend */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Légende des couleurs</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {Object.entries(statusColors).map(([status, color]) => (
              <div key={status} className="flex items-center gap-3">
                <div
                  className="w-6 h-6 rounded-full border-2 border-gray-400"
                  style={{ backgroundColor: color }}
                ></div>
                <span className="text-sm text-gray-700 capitalize">{status}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Tree Container */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          {treeData ? (
            <div className="overflow-x-auto">
              <svg ref={svgRef} className="w-full" style={{ minHeight: '600px' }}></svg>
            </div>
          ) : (
            <div className="p-12 text-center">
              <p className="text-gray-500 text-lg">
                Sélectionnez une plante pour voir son arbre généalogique
              </p>
              <p className="text-gray-400 text-sm mt-2">
                Cliquez sur un nœud pour voir les détails de la propagation
              </p>
            </div>
          )}
        </div>

        {/* Info Panel */}
        {treeData && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
            <h3 className="font-bold text-blue-900 mb-2">À propos de cet arbre</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Cliquez sur un nœud pour voir les détails de la propagation</li>
              <li>• La couleur du nœud indique le statut de la propagation</li>
              <li>• Les lignes relient les propagations parent-enfant</li>
              <li>• Vous pouvez utiliser le zoom de votre navigateur (Ctrl/Cmd + +/-)</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default GenealogyTreePage;
