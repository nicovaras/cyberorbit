// src/App.jsx
import React, { useState, useEffect } from 'react';
import GraphSelector from './components/GraphSelector';
import EditorView from './components/EditorView';
import * as api from './api';
import './App.css'; // Ensure this is imported

function App() {
  const [graphs, setGraphs] = useState([]);
  const [selectedGraphId, setSelectedGraphId] = useState(null);
  const [loadingGraphs, setLoadingGraphs] = useState(true);
  const [error, setError] = useState(null);

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
  }, []);

  const handleGraphSelect = (graphId) => {
    setSelectedGraphId(graphId);
  };

  const handleBackToGraphs = () => {
    setSelectedGraphId(null);
  };

  return (
    // Updated structure
    <div className="App">
      <header className="app-header">
        <h1>Graph Editor</h1>
      </header>
      <main className="app-content">
        {error && <div className="error-message">{error}</div>}

        {loadingGraphs ? (
          <div className="loading-indicator">Loading graphs...</div>
        ) : selectedGraphId === null ? (
          <GraphSelector
             graphs={graphs}
             onSelectGraph={handleGraphSelect}
             isLoading={loadingGraphs} // Though handled above, pass for completeness
          />
        ) : (
          <EditorView
             graphId={selectedGraphId}
             graphName={graphs.find(g => g.id === selectedGraphId)?.name || 'Unknown Graph'}
             onBack={handleBackToGraphs}
          />
        )}
      </main>
    </div>
  );
}

export default App;