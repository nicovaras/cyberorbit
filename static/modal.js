const urlParams = new URLSearchParams(window.location.search);
let selectedGraph = urlParams.get('graph') || 'x'; // Get from URL or default to 'x'
// Basic validation
if (!['x', 'y', 'z'].includes(selectedGraph)) { // Add other valid graph codes here (e.g., 'z')
    selectedGraph = 'x';
}
console.log(`Loading graph: ${selectedGraph}.json`);

export function initModal(/* Remove nodes, unlocked params if relying on global */) {
  d3.selectAll("g.node")
    .on("click", function(event, d) {

      // --- Check lock status using GLOBAL state ---
      if (!window.currentAppState || !window.currentAppState.unlocked) {
          console.error("Error: currentAppState or unlocked status not available.");
          return;
      }
      const isNodeUnlocked = window.currentAppState.unlocked[d.id];
      if (!isNodeUnlocked && d.id !== 'Start') {
          console.log(`Node ${d.id} is locked.`);
          return; // Exit if node is locked
      }
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

      const popup = nodeDataFromState.popup;
      const currentNodeId = nodeDataFromState.id;
      modalTitle.textContent = nodeDataFromState.title || "Node Details";

      // --- Build HTML using nodeDataFromState ---
      let dynamicHtml = '';
      if (popup?.text && popup.text.trim() !== '') { dynamicHtml += `<p>${popup.text}</p>`; }
      if (popup?.pdf_link) { if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`; dynamicHtml += `<p><a href="${popup.pdf_link}" target="_blank" rel="noopener noreferrer">📄 Open Exercise Details</a></p>`; }
      if (popup?.exercises && popup.exercises.length > 0) {
           if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`;
           dynamicHtml += "<h4>Exercises:</h4>";
           // Use the exercise data directly from the current global state
           popup.exercises.forEach((ex, i) => {
                const exerciseId = ex.id || `ex-${i}`; // Ensure consistent ID usage
                const optional = ex.optional ? " (optional)" : "";
                const points = ex.points ?? 10;
                const checked = ex.completed ? "checked" : ""; // Reflects current state
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
      if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`;
      dynamicHtml += `
          <div id="userNotesSection" style="margin-top: 15px;">
              <h4>My Notes:</h4>
              <textarea id="userNotesArea" rows="5" style="width: 98%;">${popup?.userNotes || ''}</textarea>
              <div style="text-align: right; margin-top: 8px;">
                  <button id="saveNotesBtn" class="modal-save-button">Save Notes</button>
                  <span id="notesSaveStatus" style="margin-left: 10px;"></span>
               </div>
          </div>
      `;

      modalDynamicBody.innerHTML = dynamicHtml;

      // --- Add Listeners ---
      closeModalBtn.onclick = () => { modal.style.display = "none"; };
      modal.style.display = "block";

      modalDynamicBody.querySelectorAll('input[type=checkbox]').forEach(input => {
        input.addEventListener('change', handleCheckboxChange); // Use updated handler
      });

      const notesTextArea = modalDynamicBody.querySelector('#userNotesArea');
      const saveNotesButton = modalDynamicBody.querySelector('#saveNotesBtn');
      const notesSaveStatus = modalDynamicBody.querySelector('#notesSaveStatus');

      if (saveNotesButton && notesTextArea) {
           saveNotesButton.onclick = () => { // --- Notes Saving Logic ---
                const currentNotes = notesTextArea.value;
                const notesPayload = { notes_update: { node_id: currentNodeId, notes: currentNotes } };
                const urlParams = new URLSearchParams(window.location.search);
                let selectedGraph = urlParams.get('graph') || 'x';
                if (!['x', 'y', 'z'].includes(selectedGraph)) { selectedGraph = 'x'; }

                notesSaveStatus.textContent = "Saving...";

                // --- Step 1: POST the update ---
                fetch(`/data?graph=${selectedGraph}`, {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(notesPayload)
                })
                .then(res => {
                    if (!res.ok) { throw new Error(`Save error: ${res.statusText}`); }
                    return res.json();
                })
                .then(data => {
                    if (data.status === 'ok') {
                        // --- Step 2: POST successful, now GET the updated state ---
                        console.log("Notes update confirmed. Fetching updated state...");
                        notesSaveStatus.textContent = "Refreshing..."; // Indicate refresh
                        return fetch(`/data?graph=${selectedGraph}`); // Chain the GET request
                    } else {
                        throw new Error(data.error || "Unknown error saving notes");
                    }
                 })
                 .then(res => { // Handle the response from the GET request
                     if (!res.ok) { throw new Error(`State refresh error: ${res.statusText}`); }
                     return res.json();
                 })
                 .then(newState => { // newState is the full state from the GET request
                     console.log("Updated state received after notes save. Dispatching update.");
                     notesSaveStatus.textContent = "Saved!";
                     // Dispatch event with the NEW state from the GET request
                     document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
                     setTimeout(() => { notesSaveStatus.textContent = ""; }, 2000);
                 })
                 .catch(error => { // Catch errors from POST or GET
                    console.error('Error saving notes or refreshing state:', error);
                    notesSaveStatus.textContent = "Error!";
                    // No optimistic update to revert here for notes
                 });
           }; // End onclick
      } // End if saveNotesButton

    }); // End D3 click listener
} // End initModal

// --- Updated Checkbox Handler ---
function handleCheckboxChange(event) {
  const checkbox = event.target;
  const nodeId = checkbox.dataset.nodeId;
  const exerciseId = checkbox.dataset.exId;
  const isCompleted = checkbox.checked; // The desired *new* state

  if (!exerciseId) {
      console.error("Error: Could not retrieve exerciseId from checkbox dataset.", checkbox);
      alert("Error: Could not identify the exercise. Cannot save status.");
      checkbox.checked = !isCompleted; // Revert UI checkbox change immediately
      return;
  }

  console.log(`Checkbox change: Node ${nodeId}, Exercise ${exerciseId}, Completed: ${isCompleted}`);

  // Disable checkbox temporarily to prevent rapid changes
  checkbox.disabled = true;

  const updatePayload = {
      exercise_update: { exercise_id: exerciseId, completed: isCompleted }
  };

  const urlParams = new URLSearchParams(window.location.search);
  let selectedGraph = urlParams.get('graph') || 'x';
  if (!['x', 'y', 'z'].includes(selectedGraph)) { selectedGraph = 'x'; }

  // --- Step 1: POST the update ---
  fetch(`/data?graph=${selectedGraph}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatePayload)
  })
  .then(res => {
      if (!res.ok) {
          return res.json().then(errData => { throw new Error(`POST error! Status: ${res.status}. ${errData.error || res.statusText}`); })
                         .catch(() => { throw new Error(`POST error! Status: ${res.status} ${res.statusText}`); });
      }
      return res.json(); // Expect {"status": "ok"}
  })
  .then(data => {
      if (data.status === 'ok') {
          // --- Step 2: POST successful, now GET the updated state ---
          console.log(`Exercise ${exerciseId} update confirmed. Fetching updated state...`);
          return fetch(`/data?graph=${selectedGraph}`); // Chain the GET request
      } else {
          throw new Error(data.error || "Unknown error saving exercise status");
      }
  })
  .then(res => { // Handle the response from the GET request
      if (!res.ok) { throw new Error(`State refresh error: ${res.statusText}`); }
      return res.json();
  })
  .then(newState => { // newState is the full state from the GET request
      // Backend successfully processed POST and returned the updated state via GET
      console.log("Updated state received. Dispatching appDataUpdated event.");
      // Dispatch event with the NEW state from the GET request
      document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
      document.getElementById("modal").style.display = "none"; // Close modal on success
  })
  .catch(error => {
      // Handle network errors or errors thrown from POST or GET
      console.error('Error updating exercise or refreshing state:', error);
      alert(`Error saving exercise status: ${error.message}`);
      // Revert UI checkbox on error
      checkbox.checked = !isCompleted;
  })
  .finally(() => {
      // Re-enable checkbox regardless of success or failure
      checkbox.disabled = false;
  });
} // End of handleCheckboxChange