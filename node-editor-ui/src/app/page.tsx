"use client";

import React, { useState, useMemo, useRef, useCallback, useEffect } from "react";
import { useTheme } from "next-themes";
import { ModeToggle } from "@/components/theme-toggle"; // Assuming this exists
import {
  Card,
  CardContent,
  CardHeader,
  CardFooter, // Added CardFooter for Save button
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
    AlertDialog, // For discard confirmation
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import {
  ChevronDown, ChevronRight, Download, Upload, Plus, Trash2, Star, GitBranch,
  FileJson, X, Settings2, Save, // Added Save icon
  AlertTriangle // For warnings/errors
} from "lucide-react";

// Helper to compare if editing node differs from original
const haveNodesChanged = (originalNode, editingNode) => {
    if (!originalNode && !editingNode) return false;
    if (!originalNode || !editingNode) return true;
    // Simple comparison, consider deep comparison library for complex cases
    return JSON.stringify(originalNode) !== JSON.stringify(editingNode);
};


const categoryOptions = [
  "Scripting and Automation", "System Analysis", "Web and Network Analysis",
  "Defensive Techniques", "Offensive Techniques",
];

const generateId = () => `node_${Math.random().toString(36).substring(2, 9)}`;

export default function NodeEditorApp() {
  const [nodes, setNodes] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [collapsed, setCollapsed] = useState({});
  const fileInputRef = useRef(null);

  // --- Local State for Editing ---
  const [editingNode, setEditingNode] = useState(null); // Holds the node currently being edited
  const [isDirty, setIsDirty] = useState(false); // Track if changes have been made
  const [errorMessages, setErrorMessages] = useState({ id: '', general: '' }); // For validation feedback

  // --- Get the originally selected node ---
  const originalSelectedNode = useMemo(() => nodes.find((n) => n.id === selectedId), [nodes, selectedId]);

  // --- Effect to update editingNode when selection changes ---
  useEffect(() => {
    if (originalSelectedNode) {
      // Deep copy to avoid modifying original state indirectly
      setEditingNode(JSON.parse(JSON.stringify(originalSelectedNode)));
      setIsDirty(false); // Reset dirty state on new selection
      setErrorMessages({ id: '', general: '' }); // Clear errors
    } else {
      setEditingNode(null); // Clear editing state if no node is selected
      setIsDirty(false);
      setErrorMessages({ id: '', general: '' });
    }
  }, [originalSelectedNode]); // Depend only on the original node from global state


  // --- Effect to track if editingNode has changed ---
   useEffect(() => {
      setIsDirty(haveNodesChanged(originalSelectedNode, editingNode));
   }, [editingNode, originalSelectedNode]);


   // --- Handlers for Input Changes (Update Local editingNode) ---

   const handleEditingChange = useCallback((field, value) => {
       setEditingNode(prev => {
           if (!prev) return null;
           // Clear ID error when user types in ID field
            if (field === 'id') {
                setErrorMessages(prevErrors => ({...prevErrors, id: ''}));
            }
           return { ...prev, [field]: value };
       });
   }, []);

   const handleNestedEditingChange = useCallback((path, value) => {
       setEditingNode(prev => {
           if (!prev) return null;
           // Use immutable update helper or manual deep copy for nested state
           const updated = JSON.parse(JSON.stringify(prev)); // Simple deep copy for now
           let current = updated;
           try {
               for (let i = 0; i < path.length - 1; i++) {
                   if (current[path[i]] === undefined || current[path[i]] === null) {
                       current[path[i]] = {};
                   }
                   current = current[path[i]];
               }
               current[path[path.length - 1]] = value;
               return updated;
           } catch (error) {
               console.error("Failed to update nested editing state:", error, path, value);
               setErrorMessages(prevErrors => ({...prevErrors, general: 'Error updating nested field.'}));
               return prev; // Return previous state on error
           }
       });
   }, []);


   // Specific handler for exercise changes within editingNode
   const handleEditingExerciseChange = useCallback((exerciseId, key, value) => {
       setEditingNode(prev => {
           if (!prev || !prev.popup?.exercises) return prev;
            const updatedPopup = { ...prev.popup };
            updatedPopup.exercises = updatedPopup.exercises.map(ex =>
                ex.id === exerciseId ? { ...ex, [key]: value } : ex
            );
            return { ...prev, popup: updatedPopup };
       });
   }, []);

    // Handler for toggling category within editingNode
   const handleEditingToggleCategory = useCallback((exerciseId, category) => {
        setEditingNode(prev => {
             if (!prev || !prev.popup?.exercises) return prev;
             const updatedPopup = { ...prev.popup };
             updatedPopup.exercises = updatedPopup.exercises.map(ex => {
                 if (ex.id === exerciseId) {
                     const updatedEx = { ...ex };
                     const catSet = new Set(updatedEx.categories || []);
                     catSet.has(category) ? catSet.delete(category) : catSet.add(category);
                     updatedEx.categories = Array.from(catSet);
                     return updatedEx;
                 }
                 return ex;
             });
             return { ...prev, popup: updatedPopup };
         });
   }, []);

   // Handler for adding exercise within editingNode
   const handleEditingAddExercise = useCallback(() => {
        setEditingNode(prev => {
            if (!prev) return null;
            const updated = JSON.parse(JSON.stringify(prev)); // Deep copy
            if (!updated.popup) updated.popup = { text: '', exercises: [] };
            if (!updated.popup.exercises) updated.popup.exercises = [];
            updated.popup.exercises.push({
                id: `ex_${generateId()}`,
                label: "", categories: [], completed: false, optional: false, points: 0
            });
            return updated;
        });
   }, []);

   // Handler for deleting exercise within editingNode
   const handleEditingDeleteExercise = useCallback((exerciseId) => {
        setEditingNode(prev => {
            if (!prev || !prev.popup?.exercises) return prev;
            const updatedPopup = { ...prev.popup };
            updatedPopup.exercises = updatedPopup.exercises.filter(ex => ex.id !== exerciseId);
            return { ...prev, popup: updatedPopup };
        });
   }, []);


  // --- Save Handler (Updates Global nodes state) ---
  const handleSaveNode = useCallback(() => {
    if (!editingNode || !selectedId) return;
    setErrorMessages({ id: '', general: '' }); // Clear previous errors

    // *** Validation ***
    const trimmedId = editingNode.id.trim();
    if (!trimmedId) {
        setErrorMessages({ id: 'Node ID cannot be empty.', general: '' });
        return;
    }
    // Check for duplicates against original nodes, excluding the original selectedId
    const isDuplicate = nodes.some(n => n.id === trimmedId && n.id !== selectedId);
    if (isDuplicate) {
        setErrorMessages({ id: `Node ID "${trimmedId}" already exists.`, general: '' });
        return;
    }

    // --- Proceed with Update ---
    setNodes(prevNodes => {
        let oldPrerequisiteId = null;
        let newPrerequisiteId = editingNode.prerequisites?.[0]; // From editingNode

        // Find the original version of the node being saved in prevNodes
        const originalNodeInPrev = prevNodes.find(n => n.id === selectedId);
         if (originalNodeInPrev) {
            oldPrerequisiteId = originalNodeInPrev.prerequisites?.[0];
         }

         // 1. Map and update/replace the node
         let updatedNodes = prevNodes.map(n =>
             n.id === selectedId ? { ...editingNode, id: trimmedId } : n // Use editing data, ensure trimmed ID
         );

         // 2. If ID changed, update references in other nodes (prerequisites and children arrays)
         if (trimmedId !== selectedId) {
             updatedNodes = updatedNodes.map(n => {
                 // Don't modify the node we just updated in step 1 if it's iterated over again
                 if (n.id === trimmedId && n !== editingNode) return n; // Skip if it's the *already updated* node

                 let changed = false;
                 const copy = { ...n }; // Work on a copy

                 // Update prerequisites pointing to the old ID
                 if (copy.prerequisites?.includes(selectedId)) {
                     copy.prerequisites = copy.prerequisites.map(p => p === selectedId ? trimmedId : p);
                     changed = true;
                 }
                 // Update children pointing to the old ID
                 if (copy.children?.includes(selectedId)) {
                     copy.children = copy.children.map(c => c === selectedId ? trimmedId : c);
                     changed = true;
                 }
                 return changed ? copy : n;
             });
         }


         // 3. Update parent's children array if prerequisite changed
         if (oldPrerequisiteId !== newPrerequisiteId) {
             updatedNodes = updatedNodes.map(n => {
                 let nodeChanged = false;
                 let updatedN = { ...n };

                 // Remove from old parent's children
                 if (oldPrerequisiteId && n.id === oldPrerequisiteId) {
                     const currentChildren = updatedN.children || [];
                     // Use `trimmedId` if ID changed, otherwise `selectedId`
                     const idToRemove = trimmedId !== selectedId ? trimmedId : selectedId;
                     const newChildren = currentChildren.filter(childId => childId !== idToRemove);
                     if (newChildren.length !== currentChildren.length) {
                         updatedN = { ...updatedN, children: newChildren };
                         nodeChanged = true;
                     }
                 }
                 // Add to new parent's children
                 if (newPrerequisiteId && n.id === newPrerequisiteId) {
                     const childrenSet = new Set(updatedN.children || []);
                     const idToAdd = trimmedId; // Always use the final (potentially new) ID
                     if (!childrenSet.has(idToAdd)) {
                         childrenSet.add(idToAdd);
                         updatedN = { ...updatedN, children: Array.from(childrenSet) };
                         nodeChanged = true;
                     }
                 }
                 return nodeChanged ? updatedN : n;
             });
         }

        return updatedNodes;
    });

    // If the ID was changed, update the global selectedId state as well
    if (trimmedId !== selectedId) {
        setSelectedId(trimmedId);
        // Note: The useEffect dependency on originalSelectedNode will handle updating editingNode
    } else {
        // If ID didn't change, force reset dirty state after successful save
         setIsDirty(false);
    }
     console.log("Node saved successfully!");
     // Potentially show a success toast message here
  }, [editingNode, selectedId, nodes]); // Dependencies needed for validation and update logic


  // --- Discard Changes ---
  const handleDiscardChanges = () => {
      if (originalSelectedNode) {
          setEditingNode(JSON.parse(JSON.stringify(originalSelectedNode))); // Reset local state
          setIsDirty(false);
          setErrorMessages({ id: '', general: '' });
      }
  };

  // --- Node Selection Logic (with Dirty Check) ---
  const handleSelectNode = (nodeIdToSelect) => {
      if (isDirty) {
          // If dirty, trigger the alert dialog confirmation
          // The actual selection change will happen in the dialog's "Confirm" action
          document.getElementById('discard-changes-trigger')?.setAttribute('data-new-selection', nodeIdToSelect);
          document.getElementById('discard-changes-trigger')?.click();
      } else {
          // If not dirty, select immediately
          setSelectedId(nodeIdToSelect);
      }
  };

  const confirmDiscardAndSelect = (triggerButton) => {
      const nodeIdToSelect = triggerButton?.getAttribute('data-new-selection');
      handleDiscardChanges(); // Discard changes first
      if (nodeIdToSelect) {
         setSelectedId(nodeIdToSelect); // Then select the new node
      }
  }


  // --- Other Handlers (Add, Delete, Upload, Download) - Mostly Unchanged, but use `setNodes` ---

  const addNode = useCallback(() => {
    const newId = generateId();
    const newNode = {
      id: newId, title: `New Node ${nodes.length + 1}`, type: "main",
      prerequisites: [], children: [], popup: { text: "", exercises: [] },
    };
    // Check for dirty state before adding and potentially switching selection
    if (isDirty) {
         // Trigger confirmation dialog, but store the action to perform on confirm
         // For simplicity here, let's just log a warning or prevent adding if dirty.
         // A better UX would use the AlertDialog similar to handleSelectNode.
         console.warn("Cannot add node while there are unsaved changes. Save or discard first.");
         setErrorMessages(prev => ({...prev, general: "Save or discard changes before adding a new node."}));
         return;
    }
    setNodes((prev) => [...prev, newNode]);
    setSelectedId(newId); // Select the new node
    setCollapsed(prev => ({...prev, [newId]: false}));
  }, [nodes, isDirty]); // Added isDirty dependency

   const deleteNode = useCallback((idToDelete) => {
       // Consider asking for confirmation before deleting
      setNodes((prev) => {
        const remainingNodes = prev.filter((n) => n.id !== idToDelete);
        return remainingNodes.map(n => {
          let changed = false;
          const updatedNode = { ...n };
          if (updatedNode.prerequisites?.includes(idToDelete)) {
            updatedNode.prerequisites = updatedNode.prerequisites.filter(p => p !== idToDelete);
            changed = true;
          }
          if (updatedNode.children?.includes(idToDelete)) {
            updatedNode.children = updatedNode.children.filter(c => c !== idToDelete);
            changed = true;
          }
          return changed ? updatedNode : n;
        });
      });
      // If the deleted node was selected, clear selection and editing state
      if (selectedId === idToDelete) {
          setSelectedId(null);
          setEditingNode(null);
          setIsDirty(false);
          setErrorMessages({ id: '', general: '' });
      }
   }, [selectedId]); // Added selectedId dependency

   const downloadJson = useCallback(() => {
    if (nodes.length === 0) {
       console.warn("No nodes to download.");
       // Consider adding a user-facing notification here
       return;
    }
    try {
       const blob = new Blob([JSON.stringify(nodes, null, 2)], {
         type: "application/json",
       });
       const a = document.createElement("a");
       a.href = URL.createObjectURL(blob);
       a.download = "nodes-config.json";
       document.body.appendChild(a);
       a.click();
       document.body.removeChild(a);
       URL.revokeObjectURL(a.href);
    } catch (error) {
        console.error("Failed to create or download JSON:", error);
        // Add user notification for failure
    }
  }, [nodes]);

 const uploadJson = useCallback((event) => {
   const file = event.target.files?.[0];
   if (!file) return;

   const reader = new FileReader();
   reader.onload = (e) => {
     try {
       const jsonContent = e.target?.result;
       if (typeof jsonContent === 'string') {
         let parsedNodes = JSON.parse(jsonContent); // Use 'let'

         if (Array.isArray(parsedNodes)) {

           // *** START: Add missing IDs to exercises ***
           parsedNodes = parsedNodes.map(node => {
             // Check if popup and exercises exist and exercises is an array
             if (node?.popup?.exercises && Array.isArray(node.popup.exercises)) {
               const updatedExercises = node.popup.exercises.map((ex, index) => {
                 // Check if 'ex' is an object and lacks a valid 'id'
                 if (typeof ex === 'object' && ex !== null && (!ex.id || String(ex.id).trim() === '')) {
                   const newId = `ex_${generateId()}_${index}`; // Add index for extra uniqueness guarantee
                   console.warn(`Adding missing ID '${newId}' to exercise: ${ex.label || `(index ${index})`}`);
                   return { ...ex, id: newId };
                 }
                 // Ensure existing IDs are strings if they aren't (optional, but good practice)
                 if (ex && typeof ex.id !== 'string') {
                    ex.id = String(ex.id);
                 }
                 return ex; // Return exercise as is (or with string ID)
               });
               // Return node with potentially updated exercises
               // Ensure popup object is copied immutably
               return { ...node, popup: { ...(node.popup || {}), exercises: updatedExercises } };
             }
             return node; // Return node as-is if no exercises to process
           });
           // *** END: Add missing IDs to exercises ***

           // Basic validation on node structure
           const isValid = parsedNodes.every(n => typeof n.id === 'string' && n.id && n.title !== undefined && typeof n.type === 'string');

           if (isValid) {
             setNodes(parsedNodes); // Set state with nodes guaranteed to have exercise IDs
             setSelectedId(null);
             setEditingNode(null);
             setIsDirty(false);
             setCollapsed({});
             console.log("Nodes loaded successfully from JSON.");
             // Add user notification (success)
           } else {
             console.error("Invalid node structure in JSON file after processing.");
             // Add user notification (invalid structure)
           }
         } else {
           console.error("Uploaded JSON is not an array.");
           // Add user notification (not an array)
         }
       }
     } catch (error) {
       console.error("Failed to parse or process JSON file:", error);
       // Add user notification (parse error)
     }
   };
   reader.onerror = (error) => {
     console.error("Failed to read file:", error);
     // Add user notification (read error)
   }
   reader.readAsText(file);
   // Reset file input value to allow uploading the same file again if needed
   event.target.value = '';
 }, []); // No dependencies needed for this setup

 const handleUploadClick = () => {
   fileInputRef.current?.click();
 };
  // --- Tree Structure Logic ---
  const tree = useMemo(() => {
    if (!Array.isArray(nodes) || nodes.length === 0) return [];
    const nodeMap = new Map();
    const validNodes = nodes.filter(n => n && typeof n.id === 'string' && n.id); // Filter invalid nodes first
    if (validNodes.length !== nodes.length) {
        console.warn("Some nodes had invalid structure (missing/invalid ID) and were filtered out.");
    }
     // Check for duplicate IDs - this might be the source of key warnings
     const ids = validNodes.map(n => n.id);
     const duplicateIds = ids.filter((id, index) => ids.indexOf(id) !== index);
     if (duplicateIds.length > 0) {
         console.error("Duplicate Node IDs found, this will cause rendering issues:", duplicateIds);
         // Potentially alert the user or try to resolve, but logging is essential
     }

    validNodes.forEach(n => nodeMap.set(n.id, { ...n, childrenObj: [] }));

    nodeMap.forEach((node) => {
      const prerequisites = Array.isArray(node.prerequisites) ? node.prerequisites : [];
      prerequisites.forEach((pid) => {
        if (pid && nodeMap.has(pid)) {
            const parentNode = nodeMap.get(pid);
            if (parentNode) {
                 const childNode = nodeMap.get(node.id); // Already checked node.id is valid
                 if (childNode) { // Child node must also be valid
                     // Ensure childrenObj exists
                     if (!parentNode.childrenObj) parentNode.childrenObj = [];
                     parentNode.childrenObj.push(childNode);
                 }
            }
        }
      });
    });

    const childNodeIds = new Set();
    nodeMap.forEach(node => {
        const prerequisites = Array.isArray(node.prerequisites) ? node.prerequisites : [];
        prerequisites.forEach(pid => { if (pid) childNodeIds.add(node.id); });
    });

    return Array.from(nodeMap.values()).filter(n => !childNodeIds.has(n.id));
  }, [nodes]);

  // --- Tree View Component (Fix Key Warning) ---
   const TreeView = ({ node, depth = 0 }) => {
       // The key prop is applied where TreeView is *used* in the map.
       // Ensure internal maps also have keys.
      if (!node || !node.id) return null;
      const isCollapsed = !!collapsed[node.id];
      const hasChildren = node.childrenObj && node.childrenObj.length > 0;

      const toggleCollapse = (e) => { e.stopPropagation(); setCollapsed(prev => ({ ...prev, [node.id]: !prev[node.id] })); };

      return (
        // Key is provided by the parent mapping over the tree/childrenObj
        <div className="text-sm select-none">
          <div
            className={`flex items-center rounded-md cursor-pointer group transition-colors duration-100 ${
              selectedId === node.id
                ? "bg-primary text-primary-foreground" // Selected style
                : "text-foreground hover:bg-accent hover:text-accent-foreground" // Default/hover style
            }`}
            // Use the new handler to check for dirty state before selecting
            onClick={() => handleSelectNode(node.id)}
            style={{ paddingLeft: `${depth * 1.25}rem` }}
          >
            <div className="flex-shrink-0 w-7 h-7 flex items-center justify-center">
              {hasChildren && (
                <Button variant="ghost" size="icon" className="w-6 h-6 rounded-md hover:bg-muted/50 data-[selected=true]:hover:bg-primary-foreground/20" onClick={toggleCollapse} aria-label={isCollapsed ? "Expand" : "Collapse"} data-selected={selectedId === node.id}>
                  {isCollapsed ? <ChevronRight size={16} className="text-muted-foreground group-hover:text-accent-foreground group-data-[selected=true]:text-primary-foreground" /> : <ChevronDown size={16} className="text-muted-foreground group-hover:text-accent-foreground group-data-[selected=true]:text-primary-foreground" />}
                </Button>
              )}
            </div>
            <div className="mr-1.5 flex-shrink-0">
               {/* Icons adjust color based on selection */}
              {node.type === "main" ? <Star size={14} className={selectedId === node.id ? "text-primary-foreground/90" : "text-yellow-500 dark:text-yellow-400"} /> : <GitBranch size={14} className={selectedId === node.id ? "text-primary-foreground/90" : "text-blue-500 dark:text-blue-400"} />}
            </div>
            <span className="truncate flex-grow py-1.5 pr-2 font-medium" title={node.title || node.id}>
              {node.title || node.id}
            </span>
          </div>
          {!isCollapsed && hasChildren && (
            <div className="mt-0.5">
              {/* Ensure childrenObj is an array and map over it */}
              {Array.isArray(node.childrenObj) && node.childrenObj.map((child) => (
                 // **Crucial:** Add key prop here for internal mapping!
                 child && child.id ? <TreeView key={`tree-${child.id}`} node={child} depth={depth + 1} /> : null
              ))}
            </div>
          )}
        </div>
      );
   };


  // --- Render ---
  return (
    // Ensure outer div allows sidebar height to be set correctly
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar - FIX: Added overflow-hidden and explicit h-screen */}
      <aside className="w-80 lg:w-96 border-r border-border flex flex-col bg-card text-card-foreground h-screen overflow-hidden">
        {/* Sidebar Header */}
        <div className="p-4 flex justify-between items-center border-b border-border flex-shrink-0"> {/* Prevent header from shrinking */}
           <h2 className="text-lg font-semibold">Node Editor</h2>
           <ModeToggle />
        </div>

         {/* Sidebar Actions */}
        <div className="p-4 space-y-2 border-b border-border flex-shrink-0"> {/* Prevent actions section from shrinking */}
          <Button onClick={downloadJson} className="w-full justify-start" variant="ghost" disabled={nodes.length === 0}> <Download className="mr-2 h-4 w-4" /> Download JSON </Button>
           <Button onClick={handleUploadClick} className="w-full justify-start" variant="ghost"> <Upload className="mr-2 h-4 w-4" /> Upload JSON </Button>
           <Input ref={fileInputRef} type="file" accept=".json" onChange={uploadJson} className="hidden" />
          <Button onClick={addNode} className="w-full justify-start" variant="ghost"> <Plus className="mr-2 h-4 w-4" /> Add New Node </Button>
        </div>

        {/* Node Tree - SCROLLABLE AREA FIX */}
        {/* ScrollArea needs to be the element that grows and handles overflow */}
        <ScrollArea className="flex-1 min-h-0 py-2"> {/* Allow shrinking, take remaining space, and enable internal scrolling */}
           <div className="space-y-0.5 p-2">
             {/* **Fix**: Added key prop to the map here as well */}
             {tree.length === 0 && <p className="text-muted-foreground text-sm p-4 text-center">No nodes yet.</p>}
             {tree.map((n) => (
               // Ensure node 'n' is valid and has an ID before rendering TreeView
               n && n.id ? <TreeView key={`root-${n.id}`} node={n} /> : null
             ))}
           </div>
        </ScrollArea>

         {/* Sidebar Footer */}
        <div className="p-3 border-t border-border text-xs text-muted-foreground flex-shrink-0"> {/* Prevent footer from shrinking */}
            {nodes.length} {nodes.length === 1 ? 'node' : 'nodes'} loaded.
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-6 lg:p-10 bg-muted/30 dark:bg-muted/10">
         {/* Use editingNode for display/input values */}
        {editingNode ? (
          <Card className="max-w-4xl mx-auto shadow-lg border-border bg-card text-card-foreground">
            <CardHeader>
               {/* General Error Message Area */}
               {errorMessages.general && (
                    <div className="mb-4 p-3 bg-destructive/10 border border-destructive/30 text-destructive text-sm rounded-md flex items-center gap-2">
                        <AlertTriangle size={16} /> {errorMessages.general}
                    </div>
                )}
              <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
                 <div className="flex-grow space-y-1">
                     {/* ID Input - Uses local editingNode state */}
                     <Label htmlFor={`node-id-${editingNode.id}`}>Node ID</Label>
                    <Input
                       id={`node-id-${editingNode.id}`}
                       value={editingNode.id || ''}
                       onChange={(e) => handleEditingChange('id', e.target.value)}
                       placeholder="Unique Node ID"
                       // Styling for error state
                       className={`text-sm focus:text-foreground mb-1 h-8 w-full sm:w-auto ${errorMessages.id ? 'border-destructive focus-visible:ring-destructive' : 'text-muted-foreground'}`}
                       aria-label="Node ID"
                       aria-invalid={!!errorMessages.id}
                       aria-describedby={errorMessages.id ? `id-error-${editingNode.id}` : undefined}
                     />
                     {errorMessages.id && <p id={`id-error-${editingNode.id}`} className="text-xs text-destructive mt-1">{errorMessages.id}</p>}

                     <Label htmlFor={`node-title-${editingNode.id}`} className="!mt-3 block">Node Title</Label>
                    <Input
                       id={`node-title-${editingNode.id}`}
                       value={editingNode.title || ''}
                       onChange={(e) => handleEditingChange('title', e.target.value)}
                       placeholder="Node Title"
                       className="text-2xl font-semibold tracking-tight border-0 shadow-none focus-visible:ring-0 focus-visible:ring-offset-0 px-0 h-auto"
                       aria-label="Node Title"
                     />
                 </div>
                 <div className="flex items-center gap-2 flex-shrink-0 w-full sm:w-auto justify-end sm:justify-start">
                    {/* Type Select - Uses local editingNode state */}
                   <Select value={editingNode.type} onValueChange={(value) => handleEditingChange("type", value)}>
                     <SelectTrigger className="w-[120px]"> <SelectValue placeholder="Type" /> </SelectTrigger>
                     <SelectContent>
                       <SelectItem value="main"> <span className="flex items-center"><Star size={14} className="mr-2 text-yellow-500 dark:text-yellow-400"/> Main</span> </SelectItem>
                       <SelectItem value="sub"> <span className="flex items-center"><GitBranch size={14} className="mr-2 text-blue-500 dark:text-blue-400"/> Sub</span> </SelectItem>
                     </SelectContent>
                   </Select>
                   {/* Delete button - Operates on original selectedId */}
                  <Button variant="destructive" size="icon" onClick={() => deleteNode(selectedId)} title="Delete Node"> <Trash2 size={16} /> <span className="sr-only">Delete Node</span> </Button>
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-6 pt-0">
               {/* Description - Uses local editingNode state */}
              <div className="space-y-2">
                <Label htmlFor={`desc-${editingNode.id}`}>Description</Label>
                <Textarea
                  id={`desc-${editingNode.id}`}
                  value={editingNode.popup?.text || ""}
                  onChange={(e) => handleNestedEditingChange(["popup", "text"], e.target.value)}
                  placeholder="Enter node description or content..."
                  className="min-h-[120px] text-base"
                />
              </div>

               {/* Prerequisite - Uses local editingNode state */}
              <div className="space-y-2">
                <Label>Prerequisite (Parent)</Label>
                 <Select
                   value={editingNode.prerequisites?.[0] || "none"}
                   onValueChange={(val) => handleEditingChange("prerequisites", val === "none" ? [] : [val])}
                 >
                  <SelectTrigger className="w-full"> <SelectValue placeholder="Select prerequisite..." /> </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">None</SelectItem>
                    {nodes // Show list of original nodes for selection
                      .filter((n) => n.id !== editingNode.id) // Exclude self (use editingNode.id here)
                      .sort((a, b) => (a.title || a.id).localeCompare(b.title || b.id))
                      .map((n) => (<SelectItem key={n.id} value={n.id}> {n.title || n.id} {n.type === 'main' ? '(★)' : ''} </SelectItem>))}
                  </SelectContent>
                </Select>
              </div>

               {/* Children Display (Read-only, reflects saved state) */}
              <div className="space-y-2">
                 <Label>Children (Linked Nodes)</Label>
                 <div className="flex gap-2 flex-wrap pt-1">
                    {/* Display children based on the *original* selected node's state */}
                   {(originalSelectedNode?.children || []).length > 0 ? (
                     (originalSelectedNode.children || []).map((childId) => {
                       const childNode = nodes.find(n => n.id === childId); // Find in global state
                       return (<Badge key={childId} variant="secondary">{childNode?.title || childId}</Badge>);
                     })
                   ) : ( <p className="text-sm text-muted-foreground">No nodes list this as a prerequisite.</p> )}
                 </div>
              </div>

               {/* Exercises - Uses local editingNode state */}
              <div className="space-y-4 pt-4 border-t border-border">
                 <div className="flex justify-between items-center">
                    <h3 className="text-lg font-medium">Exercises</h3>
                    <Button onClick={handleEditingAddExercise} size="sm"> <Plus className="mr-2 h-4 w-4" /> Add Exercise </Button>
                 </div>
                 {(editingNode.popup?.exercises || []).length === 0 && ( <p className="text-muted-foreground text-sm py-4 text-center italic">No exercises added.</p> )}
                 {(editingNode.popup?.exercises || []).map((ex) => (
                   <Card key={ex.id} className="bg-muted/40 dark:bg-muted/20 border-border shadow-sm overflow-hidden">
                     <CardContent className="p-4 space-y-4">
                         {/* Exercise Inputs use handleEditingExerciseChange */}
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                           <Input value={ex.label} onChange={(e) => handleEditingExerciseChange(ex.id, "label", e.target.value)} placeholder="Exercise Label" className="flex-grow"/>
                           <Input type="number" value={ex.points} onChange={(e) => handleEditingExerciseChange(ex.id, "points", parseInt(e.target.value) || 0)} placeholder="Pts" min="0" className="w-full sm:w-20"/>
                         </div>
                         {/* Categories use handleEditingToggleCategory */}
                         <div>
                            <Label className="text-xs text-muted-foreground mb-2 block">Categories</Label>
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-2">
                               {categoryOptions.map((category) => (
                                 <div key={category} className="flex items-center space-x-2">
                                   <Checkbox id={`cat-${editingNode.id}-${ex.id}-${category.replace(/\s/g, '-')}`} checked={(ex.categories || []).includes(category)} onCheckedChange={() => handleEditingToggleCategory(ex.id, category)}/>
                                   <Label htmlFor={`cat-${editingNode.id}-${ex.id}-${category.replace(/\s/g, '-')}`} className="text-sm font-normal cursor-pointer hover:text-primary">{category}</Label>
                                 </div> ))}
                           </div>
                         </div>
                         {/* Optional & Delete use relevant handlers */}
                         <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pt-2 gap-4">
                            <div className="flex items-center space-x-2">
                               <Checkbox id={`opt-${editingNode.id}-${ex.id}`} checked={!!ex.optional} onCheckedChange={(checked) => handleEditingExerciseChange(ex.id, "optional", checked === true)} />
                               <Label htmlFor={`opt-${editingNode.id}-${ex.id}`} className="text-sm font-normal cursor-pointer">Optional Exercise</Label>
                            </div>
                            <Button variant="outline" size="sm" className="text-destructive hover:bg-destructive/10 hover:text-destructive border-destructive/50 w-full sm:w-auto" onClick={() => handleEditingDeleteExercise(ex.id)}> <Trash2 size={14} className="mr-1.5" /> Delete Exercise </Button>
                         </div>
                     </CardContent>
                   </Card>
                 ))}
              </div>
            </CardContent>

            {/* Save/Discard Footer */}
             <CardFooter className="flex justify-end gap-2 border-t pt-4">
                 <Button variant="ghost" onClick={handleDiscardChanges} disabled={!isDirty}>Discard Changes</Button>
                 <Button onClick={handleSaveNode} disabled={!isDirty}>
                     <Save size={16} className="mr-2"/> Save Node
                 </Button>
             </CardFooter>

          </Card>
        ) : (
           // Placeholder when no node is selected
          <div className="flex flex-col items-center justify-center h-full text-center p-8">
             <Settings2 size={64} className="text-muted-foreground/30 mb-6" />
            <h2 className="text-xl font-semibold text-muted-foreground">Select or Create a Node</h2>
            <p className="text-muted-foreground max-w-md mx-auto mt-2"> Choose a node from the sidebar tree view to edit its details and exercises, or use the 'Add New Node' button to start building your structure. </p>
             <p className="mt-6"> <Button onClick={addNode} variant="default" size="lg"> <Plus className="mr-2 h-5 w-5" /> Add Your First Node </Button> </p>
          </div>
        )}
      </main>

        {/* Alert Dialog for Discard Confirmation */}
        <AlertDialog>
            {/* Hidden trigger, activated programmatically */}
            <AlertDialogTrigger asChild>
                <button id="discard-changes-trigger" className="hidden">Open Dialog</button>
            </AlertDialogTrigger>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Unsaved Changes</AlertDialogTitle>
                    <AlertDialogDescription>
                        You have unsaved changes. Are you sure you want to discard them and switch nodes?
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel onClick={() => {
                        // Clear the attribute if cancelled
                        document.getElementById('discard-changes-trigger')?.removeAttribute('data-new-selection');
                    }}>Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={(e) => confirmDiscardAndSelect(e.currentTarget.closest('div[role="dialog"]')?.querySelector('#discard-changes-trigger'))}>
                        Discard & Switch
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>

    </div>
  );
}