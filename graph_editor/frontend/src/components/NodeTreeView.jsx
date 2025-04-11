// src/components/NodeTreeView.jsx
import React, { useState, useMemo } from 'react';
// --- IMPORT ICONS ---
import { FiFolder, FiFileText, FiChevronRight, FiChevronDown } from 'react-icons/fi';

// buildTree helper function remains the same...
const buildTree = (nodes) => {
  const nodeMap = {};
  const roots = [];

  nodes.forEach(node => {
    nodeMap[node.id] = { ...node, children: [] };
    if (node.parent_id === null || node.parent_id === undefined) {
      roots.push(nodeMap[node.id]);
    }
  });

  nodes.forEach(node => {
    if (node.parent_id !== null && node.parent_id !== undefined) {
      const parent = nodeMap[node.parent_id];
      if (parent) {
        if (!parent.children.some(child => child.id === node.id)) {
             parent.children.push(nodeMap[node.id]);
        }
      } else {
         if (!roots.some(root => root.id === node.id)) {
             console.warn(`Node ${node.id} has parent ${node.parent_id} which was not found. Treating as root.`);
             roots.push(nodeMap[node.id]);
         }
      }
    }
  });

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


const TreeNode = ({ node, onSelectNode, selectedNodeId }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const hasChildren = node.children && node.children.length > 0;

  const handleToggle = (e) => {
    e.stopPropagation();
    setIsExpanded(!isExpanded);
  };

  const handleSelect = () => {
    onSelectNode(node.id);
  };

  const isSelected = node.id === selectedNodeId;

  return (
    <div className="tree-node">
      <div className={`node-item ${isSelected ? 'selected' : ''}`} onClick={handleSelect}>
        {hasChildren ? (
          <div className="toggle-area" onClick={handleToggle}>
            {isExpanded ? '▼' : '▶'}
          </div>
        ) : (
          <div className="toggle-placeholder"></div>
        )}
        <div className={`node-title ${node.type}`}>
          {node.title}
        </div>
      </div>
      {hasChildren && (
        <div
          className="node-children"
          style={{ display: isExpanded ? 'block' : 'none' }}
        >
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
  const treeData = useMemo(() => buildTree(nodes), [nodes]);

  // More engaging placeholder
  if (!nodes || nodes.length === 0) {
      return <div className="placeholder-message"><FiFileText/> No nodes found for this graph.</div>;
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