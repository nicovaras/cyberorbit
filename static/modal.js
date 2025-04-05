const urlParams = new URLSearchParams(window.location.search);
let selectedGraph = urlParams.get('graph') || 'x'; // Get from URL or default to 'x'
// Basic validation
if (!['x', 'y'].includes(selectedGraph)) { // Add other valid graph codes here (e.g., 'z')
    selectedGraph = 'x';
}
console.log(`Loading graph: ${selectedGraph}.json`);

export function initModal(/* Remove nodes, unlocked params if relying on global */) {
  d3.selectAll("g.node")
    .on("click", function(event, d) {

      // --- START MODIFIED LOGIC ---
      // Check lock status using the GLOBAL state fetched initially/updated via events
      // Check if window.currentAppState and its properties exist
      if (!window.currentAppState || !window.currentAppState.unlocked) {
          console.error("Error: currentAppState or unlocked status not available.");
          // Optionally show a message to the user
          return;
      }

      const isNodeUnlocked = window.currentAppState.unlocked[d.id];

      if (!isNodeUnlocked && d.id !== 'Start') { // Allow clicking Start node
          console.log(`Node ${d.id} is locked.`);
          // Optionally provide visual feedback that node is locked
          return; // Exit if node is locked
      }

      // Node is unlocked, proceed to build and show modal using existing data
      console.log(`Opening exercise modal for unlocked node: ${d.id}`);

      // Find the full node data (including exercises) from the current state
      const nodeDataFromState = window.currentAppState.nodes.find(n => n.id === d.id);
      if (!nodeDataFromState) {
          console.error(`Node data for ${d.id} not found in currentAppState.`);
          return;
      }

      const modal = document.getElementById("modal");
      const modalTitle = document.getElementById("modalTitle");
      const modalDynamicBody = document.getElementById("modalDynamicBody");
      const closeModalBtn = document.getElementById("closeModalBtn");

      if (!modal || !modalTitle || !modalDynamicBody || !closeModalBtn) {
           console.error("Core modal elements not found!"); return;
      }

      // Use nodeDataFromState instead of 'd' if 'd' only has partial data from d3
      const popup = nodeDataFromState.popup; // Use data from the state
      const currentNodeId = nodeDataFromState.id;

      modalTitle.textContent = nodeDataFromState.title || "Node Details";

      // Build HTML using nodeDataFromState.popup
      let dynamicHtml = '';
      // ... (rest of HTML building logic using 'popup' variable) ...
       // Description (optional)
       if (popup?.text && popup.text.trim() !== '') { dynamicHtml += `<p>${popup.text}</p>`; }
       // PDF Link (optional)
       if (popup?.pdf_link) { if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`; dynamicHtml += `<p><a href="${popup.pdf_link}" target="_blank" rel="noopener noreferrer">📄 Open Exercise Details</a></p>`; }
      // Exercises (optional)
      if (popup?.exercises && popup.exercises.length > 0) {
           if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`;
           dynamicHtml += "<h4>Exercises:</h4>";
           popup.exercises.forEach((ex, i) => {
                const exerciseId = ex.id || `ex-${i}`;
                const optional = ex.optional ? " (optional)" : "";
                const points = ex.points ?? 10;
                // Use ex.completed directly from the state
                const checked = ex.completed ? "checked" : "";
                dynamicHtml += `
                 <div style="margin-bottom: 8px;">
                     <label style="opacity: ${ex.optional ? 0.7 : 1}; font-style: ${ex.optional ? 'italic' : 'normal'}; display: flex; align-items: center;">
                       <input type="checkbox" data-node-id="${currentNodeId}" data-ex-id="${exerciseId}" data-ex-index="${i}" ${checked} style="margin-right: 8px;"/>
                       <span>${ex.label} (${points} points)${optional}</span>
                     </label>
                 </div>
               `;
           });
       }
      // User Notes Section
      if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`;
      dynamicHtml += `
          <div id="userNotesSection" style="margin-top: 15px;">
              <h4>My Notes:</h4>
              <textarea id="userNotesArea" rows="5" style="width: 98%; ...">${popup?.userNotes || ''}</textarea>
              <div style="text-align: right; margin-top: 8px;">
                  <button id="saveNotesBtn" class="modal-save-button">Save Notes</button>
                  <span id="notesSaveStatus" style="margin-left: 10px; ..."></span>
               </div>
          </div>
      `;
      // --- END MODIFIED LOGIC ---


      modalDynamicBody.innerHTML = dynamicHtml;

      // Populate notes and add listeners (keep this part)
      const notesTextArea = modalDynamicBody.querySelector('#userNotesArea');
      // notesTextArea.value = popup?.userNotes || ''; // Already set in template string above

      closeModalBtn.onclick = () => { modal.style.display = "none"; };
      modal.style.display = "block";
      modalDynamicBody.querySelectorAll('input[type=checkbox]').forEach(input => {
        input.addEventListener('change', handleCheckboxChange);
      });
      const saveNotesButton = modalDynamicBody.querySelector('#saveNotesBtn');
      const notesSaveStatus = modalDynamicBody.querySelector('#notesSaveStatus');
      if (saveNotesButton && notesTextArea) {
           saveNotesButton.onclick = () => { // Keep notes saving logic
                // ... (logic to construct notesPayload and fetch POST /data) ...
                const currentNotes = notesTextArea.value;
                const notesPayload = { notes_update: { node_id: currentNodeId, notes: currentNotes } };
                const urlParams = new URLSearchParams(window.location.search);
                let selectedGraph = urlParams.get('graph') || 'x';
                if (!['x', 'y'].includes(selectedGraph)) { selectedGraph = 'x'; }

                notesSaveStatus.textContent = "Saving...";
                fetch(`/data?graph=${selectedGraph}`, {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(notesPayload) })
                .then(res => { if (!res.ok) throw new Error(`Save error: ${res.statusText}`); return res.json();})
                .then(newState => {
                     console.log("Notes saved. Dispatching update.");
                     notesSaveStatus.textContent = "Saved!";
                     document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
                     setTimeout(() => { notesSaveStatus.textContent = ""; }, 2000);
                 })
                 .catch(error => { console.error('Error saving notes:', error); notesSaveStatus.textContent = "Error!";});
           };
      }

    }); // End D3 click listener
}

// Handler function for checkbox changes (remains the same logic)
function handleCheckboxChange(event) {
  const checkbox = event.target;
  const nodeId = checkbox.dataset.nodeId;
  const exerciseIndex = parseInt(checkbox.dataset.exIndex, 10);
  const isCompleted = checkbox.checked;
  const exerciseId = checkbox.dataset.exId; // Get exerciseId

  // Check if exerciseId was retrieved
  if (!exerciseId) {
      console.error("Error: Could not retrieve exerciseId from checkbox dataset.", checkbox);
      alert("Error: Could not identify the exercise. Cannot save status.");
      checkbox.checked = !isCompleted; // Revert UI change
      return; // Stop execution
  }

  console.log(`Checkbox change: Node ${nodeId}, Exercise ${exerciseId}, Index ${exerciseIndex}, Completed: ${isCompleted}`);

  // Get current graph selection
  const urlParams = new URLSearchParams(window.location.search);
  let selectedGraph = urlParams.get('graph') || 'x';
  if (!['x', 'y'].includes(selectedGraph)) { selectedGraph = 'x'; }

  // Construct the specific update payload
  const updatePayload = {
      exercise_update: {
          exercise_id: exerciseId, // Use the retrieved exerciseId
          completed: isCompleted
      }
  };

  // Directly POST the update payload
  fetch(`/data?graph=${selectedGraph}`, { // ONLY a POST request happens here
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatePayload)
  })
  .then(res => {
      if (!res.ok) {
          // Try to get error message from backend if possible
          return res.json().then(errData => {
              throw new Error(`POST error! Status: ${res.status}. ${errData.error || res.statusText}`);
          }).catch(() => {
              // Fallback if response wasn't JSON
              throw new Error(`POST error! Status: ${res.status} ${res.statusText}`);
          });
      }
      return res.json(); // Parse the JSON response containing the new state
  })
  .then(newState => {
      // Backend successfully processed POST and returned the updated state
      console.log("Dispatching appDataUpdated event after exercise update.");
      document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
      document.getElementById("modal").style.display = "none"; // Close modal on success
  })
  .catch(error => {
      // Handle network errors or errors thrown from the .then block
      console.error('Error updating exercise:', error);
      alert(`Error saving exercise status: ${error.message}`);
      checkbox.checked = !isCompleted; // Revert UI on error
  });
} // End of handleCheckboxChange