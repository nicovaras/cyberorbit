// src/components/GraphSelector.jsx
import React from 'react';

function GraphSelector({ graphs, onSelectGraph, isLoading }) {
  if (isLoading) {
    return <p>Loading graphs...</p>;
  }

  if (!graphs || graphs.length === 0) {
    return <div className="placeholder-message"><FiDatabase/> No graphs found. Ensure the backend is connected and graphs exist.</div>;
  }

  return (
    <div className="graph-selector">
      <h2>Select a Graph to Edit:</h2>
      <ul>
        {graphs.map(graph => (
          <li key={graph.id}>
           {/* Apply new button class and structure */}
           <button className="button button-secondary" onClick={() => onSelectGraph(graph.id)}>
             <span>{graph.name}</span>
             <span className="graph-id">ID: {graph.id}</span>
             {/* Optional: <FiChevronRight/> */}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GraphSelector;