// src/components/ExerciseItem.jsx
import React from 'react';
import { FiEdit, FiTrash2 } from 'react-icons/fi';


function ExerciseItem({ exercise, onEdit, onDelete, isProcessing, isEditing }) {

  // Display comma-separated categories
  const categories = exercise.categories || [];

  return (
    <li className={`exercise-item ${isEditing ? 'editing' : ''}`}>
      <div className="exercise-details">
             <span className="exercise-label">{exercise.label || 'Unnamed Exercise'}</span>
       <div className="exercise-meta">
           <span className="exercise-points">{exercise.points || 0} pts</span>
           {exercise.optional && <span className="exercise-optional">Optional</span>}
       </div>
       {categories.length > 0 && (
           <div className="exercise-categories">
               {/* Use category-badge */}
               {categories.map(cat => <span key={cat} className="category-badge">{cat}</span>)}
           </div>
       )}
      </div>
      <div className="exercise-actions">
              <button onClick={onEdit} disabled={isProcessing || isEditing} className="button button-ghost edit-button" title="Edit Exercise">
                  <FiEdit />
        </button>
               <button onClick={onDelete} disabled={isProcessing || isEditing} className="button button-ghost delete-button" title="Delete Exercise">
            <FiTrash2 />
        </button>
      </div>
    </li>
  );
}

export default ExerciseItem;