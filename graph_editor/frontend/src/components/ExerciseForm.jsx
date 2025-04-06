// src/components/ExerciseForm.jsx
import React, { useState, useEffect } from 'react';

// Assume fixed categories - get this from a config file or API later if needed
const ALL_CATEGORIES = [
    "Scripting and Automation", "System Analysis", "Web and Network Analysis",
    "Defensive Techniques", "Offensive Techniques"
];

function ExerciseForm({ nodeId, exerciseData, onSave, onCancel, isProcessing }) {
  const isEditMode = !!exerciseData;

  const [formData, setFormData] = useState({
    label: '', points: 10, optional: false, categories: [],
  });

  useEffect(() => {
    if (isEditMode && exerciseData) {
      setFormData({
        label: exerciseData.label || '', points: exerciseData.points || 10,
        optional: exerciseData.optional || false, categories: exerciseData.categories || [],
      });
    } else {
      setFormData({ label: '', points: 10, optional: false, categories: [] });
    }
  }, [exerciseData, isEditMode]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleCategoryChange = (e) => {
     const { value, checked } = e.target;
     setFormData(prev => {
        const currentCategories = prev.categories || [];
        if (checked) {
            return { ...prev, categories: [...new Set([...currentCategories, value])] };
        } else {
            return { ...prev, categories: currentCategories.filter(cat => cat !== value) };
        }
     });
  };

  // Renamed from handleSubmit to avoid confusion, though it performs the same logic
  const handleSaveClick = (e) => {
    // We dont need preventDefault anymore as it's not a form submit event
    // e.preventDefault();
    if (!formData.label.trim()) {
        alert("Exercise label cannot be empty.");
        return;
    }
    const pointsAsNumber = parseInt(formData.points, 10);
    if (isNaN(pointsAsNumber)) {
        alert("Points must be a number.");
        return;
    }
    // Call the actual save function passed via props
    onSave({
        ...formData,
        points: pointsAsNumber,
    });
  };

  // RENDER JSX - Notice the removal of the <form> tag
  return (
    <div className="exercise-form-container">
      <h4>{isEditMode ? 'Edit Exercise' : 'Add New Exercise'}</h4>
      {/* Removed <form onSubmit={handleSubmit}> */}
        <div className="form-group">
            <label htmlFor="exLabel">Label</label>
            <input type="text" id="exLabel" name="label" value={formData.label} onChange={handleChange} required disabled={isProcessing} />
        </div>
        <div className="form-group form-group-inline">
            <label htmlFor="exPoints">Points</label>
            <input type="number" id="exPoints" name="points" value={formData.points} onChange={handleChange} required min="0" step="1" disabled={isProcessing} style={{width: '80px'}}/>

            <label htmlFor="exOptional" style={{ marginLeft: '20px', marginRight: '5px' }}>Optional</label>
            <input type="checkbox" id="exOptional" name="optional" checked={formData.optional} onChange={handleChange} disabled={isProcessing} />
        </div>
        <div className="form-group">
            <label>Categories</label>
            <div className="category-checkbox-group">
                {ALL_CATEGORIES.map(cat => (
                    <div key={cat} className="category-checkbox-item">
                        <input type="checkbox" id={`cat-${cat.replace(/\s+/g, '-')}`} value={cat} checked={formData.categories.includes(cat)} onChange={handleCategoryChange} disabled={isProcessing}/>
                        <label htmlFor={`cat-${cat.replace(/\s+/g, '-')}`}>{cat}</label>
                    </div>
                ))}
            </div>
        </div>
        <div className="form-actions">
            {/* Changed type="submit" to type="button" and added onClick */}
            <button type="button" onClick={handleSaveClick} disabled={isProcessing}>
                {isProcessing ? 'Saving...' : (isEditMode ? 'Update Exercise' : 'Add Exercise')}
            </button>
            <button type="button" onClick={onCancel} disabled={isProcessing} className="cancel-button">
                Cancel
            </button>
        </div>
      {/* Removed </form> */}
    </div>
  );
}

export default ExerciseForm;