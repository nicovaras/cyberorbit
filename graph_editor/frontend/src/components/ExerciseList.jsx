// src/components/ExerciseList.jsx
import React, { useState } from 'react';
import ExerciseItem from './ExerciseItem';
import ExerciseForm from './ExerciseForm';
import * as api from '../api'; // Import API functions

// Receive onDataChange prop which is the refresh function from EditorView
function ExerciseList({ nodeId, exercises = [], isProcessing, onDataChange }) {
    const [showAddForm, setShowAddForm] = useState(false);
    const [editingExercise, setEditingExercise] = useState(null);
    const [exerciseError, setExerciseError] = useState(null); // Local error state for exercises
    const [isSubmittingExercise, setIsSubmittingExercise] = useState(false); // Local processing state

    const handleApiCall = async (apiFunction, successMessage, errorMessagePrefix) => {
        setIsSubmittingExercise(true);
        setExerciseError(null);
        try {
            await apiFunction();
            alert(successMessage);
            onDataChange(); // Trigger refresh of node details (including exercises)
            // Reset local form states
            setShowAddForm(false);
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

    const handleEditClick = (exercise) => {
        setEditingExercise(exercise);
        setShowAddForm(false); // Close add form if open
        setExerciseError(null); // Clear errors when opening edit form
    };

    const handleCancelForm = () => {
         setShowAddForm(false);
         setEditingExercise(null);
         setExerciseError(null);
    }

    // Combine processing states for disabling buttons
    const isBusy = isProcessing || isSubmittingExercise;

  return (
    <div className="exercises-section">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px'}}>
        <h3>Exercises</h3>
        <button
            type="button"
            onClick={() => { setEditingExercise(null); setShowAddForm(true); setExerciseError(null); }}
            disabled={isBusy || showAddForm || !!editingExercise} // Disable if already adding/editing
            className="add-exercise-button"
         >
             + Add Exercise
         </button>
      </div>

      {/* Display Exercise-specific Errors */}
      {exerciseError && <div className="error-message" style={{fontSize: '0.9em', marginBottom: '10px'}}>{exerciseError}</div>}


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


      {/* List of Exercises */}
      {exercises.length === 0 ? (
        <p>No exercises added for this node yet.</p>
      ) : (
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
      )}
    </div>
  );
}

export default ExerciseList;