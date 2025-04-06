// src/components/GraphSelector.jsx
import React from 'react';

function GraphSelector({ graphs, onSelectGraph, isLoading }) {
  if (isLoading) {
    return <p>Loading graphs...</p>;
  }

  if (!graphs || graphs.length === 0) {
    return <p>No graphs found. Ensure the backend is connected and graphs exist.</p>;
  }

  return (
    <div className="graph-selector">
      <h2>Select a Graph to Edit:</h2>
      <ul>
        {graphs.map(graph => (
          <li key={graph.id}>
            <button onClick={() => onSelectGraph(graph.id)}>
              {graph.name} (ID: {graph.id})
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GraphSelector;