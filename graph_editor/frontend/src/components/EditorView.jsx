// src/components/EditorView.jsx
import React, { useState, useEffect, useCallback } from 'react';
import NodeTreeView from './NodeTreeView';
import NodeEditorForm from './NodeEditorForm';
import AddNodeForm from './AddNodeForm';
import * as api from '../api';

function EditorView({ graphId, graphName, onBack }) {
  const [nodes, setNodes] = useState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [selectedNodeDetails, setSelectedNodeDetails] = useState(null);
  const [isLoadingNodes, setIsLoadingNodes] = useState(false);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [showAddNodeForm, setShowAddNodeForm] = useState(false);

  // --- Fetch nodes (no change needed here) ---
  const fetchNodes = useCallback(() => {
    if (!graphId) return;
    console.log("Fetching nodes for graph:", graphId);
    setIsLoadingNodes(true);
    setError(null);
    api.getGraphNodes(graphId)
      .then(response => { setNodes(response.data || []); })
      .catch(err => {
        console.error(`Failed to fetch nodes for graph ${graphId}:`, err);
        setError(`Could not load nodes: ${err.message}`);
        setNodes([]);
      })
      .finally(() => { setIsLoadingNodes(false); });
  }, [graphId]);

  useEffect(() => {
    fetchNodes();
    setSelectedNodeId(null);
    setSelectedNodeDetails(null);
  }, [fetchNodes]);

  // --- Fetch node details (no change needed here) ---
  const fetchNodeDetails = useCallback((nodeId) => {
      if (!nodeId) {
          setSelectedNodeDetails(null);
          return;
      }
      console.log("Fetching details for node:", nodeId);
      setIsLoadingDetails(true);
      setError(null);
      api.getNodeDetails(nodeId)
          .then(response => { setSelectedNodeDetails(response.data); })
          .catch(err => {
              console.error(`Failed to fetch details for node ${nodeId}:`, err);
              setError(`Could not load node details: ${err.message}`);
              setSelectedNodeDetails(null);
          })
          .finally(() => { setIsLoadingDetails(false); });
  }, []); // No dependency on selectedNodeId here, it's passed as argument

  useEffect(() => {
    fetchNodeDetails(selectedNodeId);
  }, [selectedNodeId, fetchNodeDetails]); // Run when selectedNodeId changes


  const handleNodeSelect = (nodeId) => {
    console.log("Node selected:", nodeId);
    if (selectedNodeId !== nodeId) {
        setSelectedNodeId(nodeId);
    }
  };

  // --- Node Update Handler (no change needed) ---
  const handleNodeUpdate = async (nodeDataToSave) => {
    if (!selectedNodeId) return;
    setIsProcessing(true); setError(null);
    try {
      const response = await api.updateNode(selectedNodeId, nodeDataToSave);
      setSelectedNodeDetails(response.data);
      fetchNodes(); // Refresh tree in case title/parent changed
      alert("Node updated successfully!");
    } catch (err) {
      setError(`Update failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // --- Node Delete Handler (no change needed) ---
   const handleNodeDelete = async () => {
    if (!selectedNodeId || !selectedNodeDetails) return;
    if (window.confirm(`Are you sure you want to delete node "${selectedNodeDetails.title}" (ID: ${selectedNodeId})? Its children will become root nodes.`)) {
        setIsProcessing(true); setError(null);
        try {
            await api.deleteNode(selectedNodeId);
            setSelectedNodeId(null);
            setSelectedNodeDetails(null);
            fetchNodes();
            alert("Node deleted successfully!");
        } catch (err) {
            setError(`Delete failed: ${err.message}`);
        } finally {
            setIsProcessing(false);
        }
    }
   };

  // --- Node Create Handler (no change needed) ---
   const handleNodeCreate = async (newNodeData) => {
       setIsProcessing(true); setError(null); setShowAddNodeForm(false);
       try {
           const response = await api.createNode(graphId, newNodeData);
           fetchNodes();
           // Important: Select AFTER fetchNodes completes if possible, or rely on user click
           // For simplicity, just log it - user can click the new node.
           console.log("Node created, selecting:", response.data.id);
           // setSelectedNodeId(response.data.id); // Select the new node
           alert("Node created successfully! Select it from the tree to edit.");
       } catch (err) {
           setError(`Create failed: ${err.message}`);
           setShowAddNodeForm(true); // Optionally reopen form
       } finally {
           setIsProcessing(false);
       }
   };

  // --- Function to refresh details (for exercises) ---
  const refreshNodeDetails = () => {
      if(selectedNodeId) {
          console.log("Refreshing node details for:", selectedNodeId);
          // Re-use the fetch function
          fetchNodeDetails(selectedNodeId);
      }
  }

  const isBusy = isLoadingDetails || isLoadingNodes || isProcessing;

  return (
    <div className="editor-view">
        {/* Keep Back Button, Title, Error, Loading Indicator */}
         <button onClick={onBack} style={{ marginBottom: '1rem' }} disabled={isBusy}>
            &larr; Back to Graph Selection
        </button>
        <h2>Editing Graph: {graphName} (ID: {graphId})</h2>
        {error && <div className="error-message">{error}</div>}
        {isBusy && <div className="loading-indicator">Processing...</div>}

        <div className="editor-layout">
            {/* --- Tree Pane (Keep Add Node Button) --- */}
            <div className="tree-pane">
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px'}}>
                    <h3>Nodes</h3>
                    <button onClick={() => setShowAddNodeForm(true)} disabled={isBusy} className="add-node-button">
                        + Add Node
                    </button>
                </div>
                {isLoadingNodes ? ( <p>Loading nodes...</p> ) : (
                    <NodeTreeView nodes={nodes} onSelectNode={handleNodeSelect} selectedNodeId={selectedNodeId} />
                )}
            </div>

            {/* --- Form Pane --- */}
            <div className="form-pane">
                <h3>Node Details</h3>
                {selectedNodeId ? (
                    isLoadingDetails ? ( <p>Loading node details...</p> ) :
                    selectedNodeDetails ? (
                        <NodeEditorForm
                            key={selectedNodeId}
                            nodeData={selectedNodeDetails}
                            allNodes={nodes}
                            onSave={handleNodeUpdate}
                            onDelete={handleNodeDelete}
                            isProcessing={isProcessing}
                            onRefreshNeeded={refreshNodeDetails} // Pass the refresh function
                        />
                    ) : ( <p>Could not load details for node {selectedNodeId}.</p> )
                ) : ( <p>Select a node from the tree or add a new node.</p> )}
            </div>
        </div>

        {/* --- Add Node Modal/Form (Keep as is) --- */}
        {showAddNodeForm && (
            <AddNodeForm
                onClose={() => setShowAddNodeForm(false)}
                onCreate={handleNodeCreate}
                allNodes={nodes}
                isProcessing={isProcessing}
            />
        )}
    </div>
  );
}

export default EditorView;