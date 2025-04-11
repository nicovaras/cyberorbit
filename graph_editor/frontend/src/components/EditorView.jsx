// src/components/EditorView.jsx
import React, { useState, useEffect, useCallback } from 'react';
import NodeTreeView from './NodeTreeView';
import NodeEditorForm from './NodeEditorForm';
import AddNodeForm from './AddNodeForm'; // Assuming AddNodeForm is styled via CSS now
import * as api from '../api';
// --- IMPORT ICONS ---
import { FiArrowLeft, FiPlusCircle, FiAlertCircle, FiInfo } from 'react-icons/fi';


function EditorView({ graphId, graphName, onBack }) {
  const [nodes, setNodes] = useState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [selectedNodeDetails, setSelectedNodeDetails] = useState(null);
  const [isLoadingNodes, setIsLoadingNodes] = useState(false);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [showAddNodeForm, setShowAddNodeForm] = useState(false);

  // Fetching logic remains the same...
  const fetchNodes = useCallback(() => {
    if (!graphId) return;
    setIsLoadingNodes(true); setError(null);
    api.getGraphNodes(graphId)
      .then(response => { setNodes(response.data || []); })
      .catch(err => {
        console.error(`Failed to fetch nodes for graph ${graphId}:`, err);
        setError(`Could not load nodes: ${err.message}`); setNodes([]);
      })
      .finally(() => { setIsLoadingNodes(false); });
  }, [graphId]);

  useEffect(() => { fetchNodes(); setSelectedNodeId(null); setSelectedNodeDetails(null); }, [fetchNodes]);

  const fetchNodeDetails = useCallback((nodeId) => {
      if (!nodeId) { setSelectedNodeDetails(null); return; }
      setIsLoadingDetails(true); setError(null);
      api.getNodeDetails(nodeId)
          .then(response => { setSelectedNodeDetails(response.data); })
          .catch(err => {
              console.error(`Failed to fetch details for node ${nodeId}:`, err);
              setError(`Could not load node details: ${err.message}`); setSelectedNodeDetails(null);
          })
          .finally(() => { setIsLoadingDetails(false); });
  }, []);

  useEffect(() => { fetchNodeDetails(selectedNodeId); }, [selectedNodeId, fetchNodeDetails]);


  const handleNodeSelect = (nodeId) => {
    if (selectedNodeId !== nodeId) { setSelectedNodeId(nodeId); }
  };

  // CRUD operation handlers remain the same logic, just ensure alerts/confirmations are fine
  const handleNodeUpdate = async (nodeDataToSave) => {
    if (!selectedNodeId) return;
    setIsProcessing(true); setError(null);
    try {
      const response = await api.updateNode(selectedNodeId, nodeDataToSave);
      setSelectedNodeDetails(response.data); // Update details locally
      // Optimistic UI update for title/parent change in tree
      setNodes(prevNodes => prevNodes.map(n => n.id === selectedNodeId ? {...n, ...response.data} : n));
      // fetchNodes(); // Or refetch all if complex parent changes occur often
    } catch (err) { setError(`Update failed: ${err.message}`); }
    finally { setIsProcessing(false); }
  };

   const handleNodeDelete = async () => {
    if (!selectedNodeId || !selectedNodeDetails) return;
    if (window.confirm(`Are you sure you want to delete node "${selectedNodeDetails.title}" (ID: ${selectedNodeId})? Its children may become root nodes.`)) {
        setIsProcessing(true); setError(null);
        try {
            await api.deleteNode(selectedNodeId);
            setSelectedNodeId(null);
            setSelectedNodeDetails(null);
            fetchNodes(); // Must refetch after delete
        } catch (err) { setError(`Delete failed: ${err.message}`); }
        finally { setIsProcessing(false); }
    }
   };

   const handleNodeCreate = async (newNodeData) => {
       setIsProcessing(true); setError(null); setShowAddNodeForm(false);
       try {
           const response = await api.createNode(graphId, newNodeData);
           fetchNodes(); // Refetch nodes to include the new one
           // Optionally select the new node
           // setSelectedNodeId(response.data.id);
       } catch (err) {
           setError(`Create failed: ${err.message}`);
           setShowAddNodeForm(true); // Reopen form on failure
       } finally {
           setIsProcessing(false);
       }
   };

  const refreshNodeDetails = () => {
      if(selectedNodeId) { fetchNodeDetails(selectedNodeId); }
  }

  const isBusy = isLoadingDetails || isLoadingNodes || isProcessing;

  return (
    <div className="editor-view">
         {/* Header within Editor View */}
         <div className="editor-header">
            <h2>Editing Graph: {graphName} (ID: {graphId})</h2>
            <button onClick={onBack} className="back-button" disabled={isBusy}>
                <FiArrowLeft /> Back to Selection
            </button>
         </div>

        {error && <div className="error-message"><FiAlertCircle/> {error}</div>}
        {isBusy && <div className="loading-indicator">Processing...</div>}

        <div className="editor-layout">
            {/* --- Tree Pane --- */}
            <div className="tree-pane">
                <div className="pane-header">
                    <h3>Nodes</h3>
                    <button onClick={() => setShowAddNodeForm(true)} className="add-node-button" disabled={isBusy}>
                        <FiPlusCircle /> Add Node
                    </button>
                </div>
                <div className="pane-content"> {/* Scrollable content area */}
                    {isLoadingNodes ? ( <div className="loading-indicator">Loading nodes...</div> ) : (
                        <NodeTreeView nodes={nodes} onSelectNode={handleNodeSelect} selectedNodeId={selectedNodeId} />
                    )}
                </div>
            </div>

            {/* --- Form Pane --- */}
            <div className="form-pane">
                <div className="pane-header">
                    <h3>Node Details</h3>
                    {/* Placeholder for potential form-level actions */}
                </div>
                 {/* Form content will handle its own scrolling via NodeEditorForm structure */}
                 {selectedNodeId ? (
                    isLoadingDetails ? ( <div className="loading-indicator">Loading details...</div> ) :
                    selectedNodeDetails ? (
                        <NodeEditorForm
                            key={selectedNodeId} // Ensure form remounts on node change
                            nodeData={selectedNodeDetails}
                            allNodes={nodes}
                            onSave={handleNodeUpdate}
                            onDelete={handleNodeDelete}
                            isProcessing={isProcessing}
                            onRefreshNeeded={refreshNodeDetails}
                        />
                    ) : ( <div className="placeholder-message"><FiAlertCircle/> Could not load details for node {selectedNodeId}.</div> )
                ) : ( <div className="placeholder-message"><FiInfo/> Select a node from the tree to view/edit details or add a new node.</div> )}
            </div>
        </div>

        {/* --- Add Node Modal --- */}
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