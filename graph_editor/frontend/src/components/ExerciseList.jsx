// src/components/ExerciseList.jsx
import React, { useState } from 'react';
import ExerciseItem from './ExerciseItem';
import ExerciseForm from './ExerciseForm';
import * as api from '../api'; // Import API functions
// --- IMPORT ICONS ---
import { FiPlusCircle, FiInfo, FiAlertCircle, FiUploadCloud, FiX, FiCheckCircle } from 'react-icons/fi';

// Receive onDataChange prop which is the refresh function from EditorView
// Rename isProcessing to isProcessingParent to avoid conflict
function ExerciseList({ nodeId, exercises = [], isProcessingParent, onDataChange }) {
    const [showAddForm, setShowAddForm] = useState(false);
    const [showBulkAddForm, setShowBulkAddForm] = useState(false); // State for bulk add form
    const [bulkTitles, setBulkTitles] = useState(''); // State for textarea content
    const [editingExercise, setEditingExercise] = useState(null);
    const [exerciseError, setExerciseError] = useState(null); // Local error state for exercises
    const [isSubmittingExercise, setIsSubmittingExercise] = useState(false); // Local processing state
    const [bulkAddMessage, setBulkAddMessage] = useState(null); // Feedback for bulk add

    const handleApiCall = async (apiFunction, successMessage, errorMessagePrefix) => {
        setIsSubmittingExercise(true);
        setExerciseError(null);
        setBulkAddMessage(null); // Clear bulk message on any action
        try {
            await apiFunction();
            // Don't show alert for single add/update/delete if bulk message is shown
            // Maybe use a more robust notification system later
            // if (!bulkAddMessage) alert(successMessage);
            onDataChange(); // Trigger refresh of node details (including exercises)
            // Reset local form states
            setShowAddForm(false);
            setShowBulkAddForm(false); // Close bulk add form on success too
            setEditingExercise(null);
        } catch (err) {
            console.error(`${errorMessagePrefix}:`, err);
            setExerciseError(`${errorMessagePrefix}: ${err.message}`);
            // Keep the form open on error so user can see the issue/retry
        } finally {
            setIsSubmittingExercise(false);
        }
    };

    const handleAddExercise = (exerciseData) => {
        handleApiCall(
            () => api.addExercise(nodeId, exerciseData),
            'Exercise added successfully!',
            'Failed to add exercise'
        );
    };

    const handleUpdateExercise = (exerciseData) => {
        if (!editingExercise) return;
        handleApiCall(
            () => api.updateExercise(editingExercise.id, exerciseData),
            'Exercise updated successfully!',
            'Failed to update exercise'
        );
    };

    const handleDeleteExercise = (exerciseId) => {
         if (window.confirm("Are you sure you want to delete this exercise?")) {
            handleApiCall(
                () => api.deleteExercise(exerciseId),
                'Exercise deleted successfully!',
                'Failed to delete exercise'
            );
         }
    };

    const handleBulkAddSubmit = async () => {
        const titles = bulkTitles.split('\n').map(t => t.trim()).filter(t => t.length > 0);
        if (titles.length === 0) {
            setExerciseError("Please enter at least one exercise title.");
            return;
        }

        setIsSubmittingExercise(true);
        setExerciseError(null);
        setBulkAddMessage(null);

        // Default data for each new exercise
        const defaultExerciseData = {
            points: 10, // Or your preferred default
            optional: false,
            categories: []
        };

        const promises = titles.map(title =>
            api.addExercise(nodeId, { ...defaultExerciseData, label: title })
        );

        // Execute all add requests
        const results = await Promise.allSettled(promises);

        const addedCount = results.filter(r => r.status === 'fulfilled').length;
        const failedCount = results.length - addedCount;

        // Provide feedback
        if (addedCount > 0) {
             setBulkAddMessage({ type: 'success', text: `Successfully added ${addedCount} exercise(s).` });
             onDataChange(); // Refresh list if any succeeded
        }
        if (failedCount > 0) {
            // Combine error message if success message also exists
            const existingError = exerciseError ? `${exerciseError}\n` : '';
            setExerciseError(`${existingError}Failed to add ${failedCount} exercise(s). Check console for details.`);
            console.error("Bulk add failures:", results.filter(r => r.status === 'rejected'));
        }

        setIsSubmittingExercise(false);
        setBulkTitles(''); // Clear textarea
        setShowBulkAddForm(false); // Hide form
        // Note: Success/error messages will persist until the next action clears them
    };


    const handleEditClick = (exercise) => {
        setEditingExercise(exercise);
        setShowAddForm(false); // Close add form if open
        setShowBulkAddForm(false); // Close bulk add form if open
        setExerciseError(null); // Clear errors when opening edit form
        setBulkAddMessage(null);
    };

    const handleCancelForm = () => {
         setShowAddForm(false);
         setShowBulkAddForm(false);
         setEditingExercise(null);
         setExerciseError(null);
         setBulkAddMessage(null);
         setBulkTitles(''); // Clear textarea on cancel
    }

    // Combine processing states for disabling buttons
    // Use isProcessingParent passed from NodeEditorForm
    const isBusy = isProcessingParent || isSubmittingExercise;

  return (
    <div className="exercises-section">
      {/* Use pane-header style for consistency */}
      <div className="pane-header">
        <h3>Exercises</h3>
        <div style={{ display: 'flex', gap: 'var(--space-2)' }}> {/* Group buttons */}
            <button
                type="button"
                onClick={() => { setEditingExercise(null); setShowAddForm(false); setShowBulkAddForm(true); setExerciseError(null); setBulkAddMessage(null); }}
                disabled={isBusy || showBulkAddForm || showAddForm || !!editingExercise}
                className="button button-secondary" // Secondary style for bulk add
                title="Add multiple exercises by title"
            >
                 <FiUploadCloud/> Bulk Add
            </button>
            <button
                type="button"
                onClick={() => { setEditingExercise(null); setShowAddForm(true); setShowBulkAddForm(false); setExerciseError(null); setBulkAddMessage(null); }}
                disabled={isBusy || showAddForm || showBulkAddForm || !!editingExercise}
                className="button button-primary add-exercise-button" // Apply new classes
            >
                <FiPlusCircle /> Add Exercise
            </button>
        </div>
      </div>

      {/* Display Exercise-specific Errors */}
      {exerciseError && <div className="error-message"><FiAlertCircle/> {exerciseError}</div>}

      {/* Display Bulk Add Success/Info Message */}
      {bulkAddMessage && <div className={`message ${bulkAddMessage.type}`}><FiCheckCircle/> {bulkAddMessage.text}</div>}


      {/* Conditional Form Rendering */}
       {showAddForm && !editingExercise && (
            <ExerciseForm
                nodeId={nodeId}
                onSave={handleAddExercise}
                onCancel={handleCancelForm}
                isProcessing={isSubmittingExercise} // Use local state for form submission
            />
       )}
       {editingExercise && (
            <ExerciseForm
                nodeId={nodeId}
                exerciseData={editingExercise}
                onSave={handleUpdateExercise}
                onCancel={handleCancelForm}
                isProcessing={isSubmittingExercise} // Use local state for form submission
            />
       )}

        {/* Bulk Add Form */}
       {showBulkAddForm && !editingExercise && !showAddForm && (
            <div className="bulk-add-form">
                <h4>Bulk Add Exercises</h4>
                <p className="instructions">Enter one exercise title per line. Default values (points, optional, etc.) will be used.</p>
                <textarea
                    rows="8"
                    value={bulkTitles}
                    onChange={(e) => setBulkTitles(e.target.value)}
                    placeholder="Exercise Title 1&#10;Another Exercise Title&#10;Exercise 3..."
                    disabled={isSubmittingExercise}
                />
                <div className="form-actions">
                    <button type="button" onClick={handleCancelForm} disabled={isSubmittingExercise} className="button button-secondary"><FiX/> Cancel</button>
                    <button type="button" onClick={handleBulkAddSubmit} disabled={isSubmittingExercise} className="button button-primary"><FiUploadCloud/> {isSubmittingExercise ? 'Adding...' : 'Add All Titles'}</button>
                </div>
            </div>
       )}

      {/* List of Exercises */}
      {!showAddForm && !showBulkAddForm && !editingExercise && exercises.length === 0 ? (
        // Use placeholder style
        <div className="placeholder-message"><FiInfo/> No exercises added for this node yet. Click "+ Add Exercise".</div>
      ) : (
        // Only render the list if no forms are active OR if exercises exist
         (!showAddForm && !showBulkAddForm && !editingExercise && exercises.length > 0) || exercises.length > 0 ? (
            <ul className="exercise-list">
              {exercises.map(ex => (
                <ExerciseItem
                  key={ex.id}
                  exercise={ex}
                  onEdit={() => handleEditClick(ex)}
                  onDelete={() => handleDeleteExercise(ex.id)}
                  isProcessing={isBusy} // Disable buttons if any operation is happening
                  isEditing={editingExercise?.id === ex.id}
                />
              ))}
            </ul>
         ) : null // Don't render list placeholder if a form is showing
      )}
    </div>
  );
}

export default ExerciseList;