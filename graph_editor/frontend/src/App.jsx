// src/App.jsx
import React, { useState, useEffect, useCallback } from 'react';
import GraphSelector from './components/GraphSelector';
import EditorView from './components/EditorView';
import * as api from './api'; // Import API functions
import './App.css'; // Basic styling

function App() {
  const [graphs, setGraphs] = useState([]);
  const [selectedGraphId, setSelectedGraphId] = useState(null);
  const [loadingGraphs, setLoadingGraphs] = useState(true);
  const [error, setError] = useState(null);

  // Fetch graphs on component mount
  useEffect(() => {
    setLoadingGraphs(true);
    setError(null);
    api.getGraphs()
      .then(response => {
        setGraphs(response.data);
      })
      .catch(err => {
        console.error("Failed to fetch graphs:", err);
        setError("Could not load graphs. Is the backend running?");
      })
      .finally(() => {
        setLoadingGraphs(false);
      });
  }, []); // Empty dependency array means run once on mount

  const handleGraphSelect = (graphId) => {
    setSelectedGraphId(graphId);
  };

  const handleBackToGraphs = () => {
    setSelectedGraphId(null); // Go back to graph selection
  };

  return (
    <div className="App">
      <h1>Graph Editor</h1>
      {error && <div className="error-message">{error}</div>}

      {loadingGraphs ? (
        <p>Loading graphs...</p>
      ) : selectedGraphId === null ? (
         // Show GraphSelector only if no graph is selected
         <GraphSelector
             graphs={graphs}
             onSelectGraph={handleGraphSelect}
             isLoading={loadingGraphs}
         />
      ) : (
         // Show EditorView when a graph is selected
         <EditorView
             graphId={selectedGraphId}
             graphName={graphs.find(g => g.id === selectedGraphId)?.name || 'Unknown Graph'}
             onBack={handleBackToGraphs}
         />
      )}
    </div>
  );
}

export default App;