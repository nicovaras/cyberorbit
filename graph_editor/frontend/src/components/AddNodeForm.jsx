// src/components/AddNodeForm.jsx
import React, { useState } from 'react';

function AddNodeForm({ onClose, onCreate, allNodes = [], isProcessing }) {
  const [title, setTitle] = useState('');
  const [type, setType] = useState('sub'); // Default type
  const [parentId, setParentId] = useState(''); // Default to root

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) {
        alert("Node title cannot be empty.");
        return;
    }
    onCreate({
      title: title.trim(),
      type: type,
      parent_id: parentId === '' ? null : parentId // Convert empty string to null
    });
  };

  // Basic modal styling (add to App.css or use a library)
  const modalStyle = {
    position: 'fixed', top: '50%', left: '50%',
    transform: 'translate(-50%, -50%)',
    backgroundColor: '#2a2a2e', border: '1px solid #4a4a4a',
    padding: '25px', zIndex: 1000, borderRadius: '5px',
    minWidth: '350px', boxShadow: '0 5px 15px rgba(0,0,0,0.4)'
  };
  const overlayStyle = {
    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.6)', zIndex: 999
  };

  return (
    <div style={overlayStyle} onClick={onClose}> {/* Close on overlay click */}
      <div style={modalStyle} onClick={e => e.stopPropagation()}> {/* Prevent closing when clicking inside modal */}
        <h2>Add New Node</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="newTitle">Node Title</label>
            <input
              type="text" id="newTitle" value={title}
              onChange={(e) => setTitle(e.target.value)}
              required autoFocus
              disabled={isProcessing}
            />
          </div>
          <div className="form-group">
            <label htmlFor="newType">Node Type</label>
            <select id="newType" value={type} onChange={(e) => setType(e.target.value)} disabled={isProcessing}>
              <option value="main">Main</option>
              <option value="sub">Sub</option>
            </select>
          </div>
           <div className="form-group">
            <label htmlFor="newParentId">Parent Node (Optional)</label>
            <select id="newParentId" value={parentId} onChange={(e) => setParentId(e.target.value)} disabled={isProcessing}>
                <option value="">-- No Parent (Root Node) --</option>
                {allNodes.map(node => (
                    <option key={node.id} value={node.id}>{node.title} ({node.id})</option>
                ))}
            </select>
          </div>
          <div className="form-actions">
            <button type="submit" disabled={isProcessing}>
                {isProcessing ? 'Creating...' : 'Create Node'}
            </button>
            <button type="button" onClick={onClose} disabled={isProcessing} className="cancel-button">
                Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddNodeForm;