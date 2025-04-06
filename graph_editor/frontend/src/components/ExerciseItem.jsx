// src/components/ExerciseItem.jsx
import React from 'react';

// Assume fixed categories - get this from a config file or API later if needed
const ALL_CATEGORIES = [
    "Scripting and Automation", "System Analysis", "Web and Network Analysis",
    "Defensive Techniques", "Offensive Techniques"
];


function ExerciseItem({ exercise, onEdit, onDelete, isProcessing, isEditing }) {

  // Display comma-separated categories
  const categoriesString = exercise.categories?.join(', ') || 'None';

  return (
    <li className={`exercise-item ${isEditing ? 'editing' : ''}`}>
      <div className="exercise-details">
        <span className="exercise-label">{exercise.label || 'Unnamed Exercise'}</span>
        <span className="exercise-points">({exercise.points || 0} pts)</span>
        {exercise.optional && <span className="exercise-optional">[Optional]</span>}
         <div className="exercise-categories">Categories: {categoriesString}</div>
      </div>
      <div className="exercise-actions">
        <button onClick={onEdit} disabled={isProcessing || isEditing} className="edit-button">
            Edit
        </button>
        <button onClick={onDelete} disabled={isProcessing || isEditing} className="delete-button">
            Delete
        </button>
      </div>
    </li>
  );
}

export default ExerciseItem;