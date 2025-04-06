// src/components/AddNodeForm.jsx
import React, { useState } from 'react';
import { FiSave, FiXCircle } from 'react-icons/fi';

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

  return (
        // Apply overlay and content classes
        <div className="add-node-modal-overlay" onClick={onClose}>
          <div className="add-node-modal-content" onClick={e => e.stopPropagation()}>
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
           <button type="button" onClick={onClose} disabled={isProcessing} className="button button-secondary cancel-button">
               <FiXCircle /> Cancel
           </button>
           <button type="submit" disabled={isProcessing} className="button button-primary">
               <FiSave /> {isProcessing ? 'Creating...' : 'Create Node'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddNodeForm;