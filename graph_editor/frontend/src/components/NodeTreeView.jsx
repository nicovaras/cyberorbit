// src/components/NodeTreeView.jsx
import React, { useState } from 'react';

// Helper function to build the tree structure
const buildTree = (nodes) => {
  const nodeMap = {};
  const roots = [];

  // First pass: Create a map and identify potential roots
  nodes.forEach(node => {
    nodeMap[node.id] = { ...node, children: [] };
    if (node.parent_id === null || node.parent_id === undefined) {
      roots.push(nodeMap[node.id]);
    }
  });

  // Second pass: Link children to their parents
  nodes.forEach(node => {
    if (node.parent_id !== null && node.parent_id !== undefined) {
      const parent = nodeMap[node.parent_id];
      if (parent) {
        // Check if child already exists to prevent duplicates if data is inconsistent
        if (!parent.children.some(child => child.id === node.id)) {
             parent.children.push(nodeMap[node.id]);
        }
      } else {
        // Orphan node (parent specified but not found in the list), treat as root
         if (!roots.some(root => root.id === node.id)) {
             console.warn(`Node ${node.id} has parent ${node.parent_id} which was not found. Treating as root.`);
             roots.push(nodeMap[node.id]);
         }
      }
    }
  });

  // Sort roots and children alphabetically by title
  const sortNodes = (nodeList) => {
     nodeList.sort((a, b) => a.title.localeCompare(b.title));
     nodeList.forEach(node => {
         if (node.children.length > 0) {
             sortNodes(node.children);
         }
     });
  };

  sortNodes(roots);


  return roots;
};


// Recursive component to render a single node and its children
const TreeNode = ({ node, onSelectNode, selectedNodeId }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const hasChildren = node.children && node.children.length > 0;

  const handleToggle = (e) => {
      e.stopPropagation(); // Prevent selecting node when toggling expand
      setIsExpanded(!isExpanded);
  };

  const handleSelect = () => {
      onSelectNode(node.id);
  };

  const isSelected = node.id === selectedNodeId;

  return (
    <div className="tree-node">
      <div className={`node-item ${isSelected ? 'selected' : ''}`} onClick={handleSelect}>
        {hasChildren && (
          <span className="toggle" onClick={handleToggle}>
            {isExpanded ? '▼' : '▶'}
          </span>
        )}
        {!hasChildren && <span className="toggle-placeholder"></span>} {/* Placeholder for alignment */}
        <span className="node-title">{node.title}</span>
        {/* Optionally display type or ID: ({node.type || 'N/A'} / {node.id}) */}
      </div>
      {hasChildren && isExpanded && (
        <div className="node-children">
          {node.children.map(child => (
            <TreeNode
                key={child.id}
                node={child}
                onSelectNode={onSelectNode}
                selectedNodeId={selectedNodeId}
            />
          ))}
        </div>
      )}
    </div>
  );
};


function NodeTreeView({ nodes = [], onSelectNode, selectedNodeId }) {
  const treeData = React.useMemo(() => buildTree(nodes), [nodes]);

  if (!nodes || nodes.length === 0) {
      return <p>No nodes found for this graph.</p>;
  }

  return (
    <div className="node-tree-view">
      {treeData.map(rootNode => (
        <TreeNode
            key={rootNode.id}
            node={rootNode}
            onSelectNode={onSelectNode}
            selectedNodeId={selectedNodeId}
        />
      ))}
    </div>
  );
}

export default NodeTreeView;