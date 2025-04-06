// src/components/NodeEditorForm.jsx
import React, { useState, useEffect } from 'react';
import ExerciseList from './ExerciseList';

function NodeEditorForm({
    nodeData,
    allNodes = [],
    onSave,
    onDelete,
    isProcessing,
    onRefreshNeeded // Receive the refresh function
}) {
  // Keep form state and useEffect as before
  const [formData, setFormData] = useState({
    title: '', type: 'sub', popup_text: '', pdf_link: '', parent_id: null,
  });

  useEffect(() => {
    if (nodeData) {
      setFormData({
        title: nodeData.title || '', type: nodeData.type || 'sub',
        popup_text: nodeData.popup_text || '', pdf_link: nodeData.pdf_link || '',
        parent_id: nodeData.parent_id || '',
      });
    } else {
      setFormData({ title: '', type: 'sub', popup_text: '', pdf_link: '', parent_id: '' });
    }
  }, [nodeData]);

  const handleChange = (e) => { /* Keep as is */
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value === '' && name === 'parent_id' ? null : value
    }));
  };

  const handleSubmit = (e) => { /* Keep as is */
    e.preventDefault();
    const dataToSave = { ...formData, pdf_link: formData.pdf_link === '' ? null : formData.pdf_link };
    onSave(dataToSave);
  };

  const handleDeleteClick = () => { /* Keep as is */
      if (onDelete) { onDelete(); }
  };

  const parentOptions = allNodes.filter(n => n.id !== nodeData?.id);

  if (!nodeData) { return <p>No node selected.</p>; }

  return (
    <form onSubmit={handleSubmit} className="node-editor-form">
       {/* Keep all form groups for Node fields (ID, Title, Type, etc.) */}
        <div className="form-group"><label htmlFor="nodeId">Node ID</label><input type="text" id="nodeId" value={nodeData.id || ''} readOnly disabled /></div>
        <div className="form-group"><label htmlFor="title">Node Title</label><input type="text" id="title" name="title" value={formData.title} onChange={handleChange} required disabled={isProcessing} /></div>
        <div className="form-group"><label htmlFor="type">Node Type</label><select id="type" name="type" value={formData.type} onChange={handleChange} disabled={isProcessing}><option value="main">Main</option><option value="sub">Sub</option></select></div>
        <div className="form-group"><label htmlFor="popup_text">Description</label><textarea id="popup_text" name="popup_text" value={formData.popup_text} onChange={handleChange} rows="4" disabled={isProcessing} /></div>
        <div className="form-group"><label htmlFor="pdf_link">PDF Link (Optional)</label><input type="text" id="pdf_link" name="pdf_link" value={formData.pdf_link || ''} onChange={handleChange} placeholder="e.g., md/your_file.md or https://..." disabled={isProcessing} /></div>
        <div className="form-group"><label htmlFor="parent_id">Parent Node</label><select id="parent_id" name="parent_id" value={formData.parent_id || ''} onChange={handleChange} disabled={isProcessing}><option value="">-- No Parent (Root Node) --</option>{parentOptions.map(node => (<option key={node.id} value={node.id}>{node.title} ({node.id})</option>))}</select></div>
        <div className="form-group"><label>Children (Read-only)</label><p style={{ fontStyle: 'italic', fontSize: '0.9em' }}>Children display coming soon...</p></div>

       {/* --- Exercise Section --- */}
       <ExerciseList
           nodeId={nodeData.id}
           exercises={nodeData.exercises || []}
           isProcessing={isProcessing} // Pass down processing state
           onDataChange={onRefreshNeeded} // Pass the refresh function here
       />

      {/* --- Form Actions (Keep as is) --- */}
      <div className="form-actions">
        <button type="submit" disabled={isProcessing}>
            {isProcessing ? 'Saving...' : 'Save Node Changes'}
        </button>
        <button type="button" onClick={handleDeleteClick} disabled={isProcessing} className="delete-button">
            {isProcessing ? 'Deleting...' : 'Delete Node'}
        </button>
      </div>
    </form>
  );
}

export default NodeEditorForm;