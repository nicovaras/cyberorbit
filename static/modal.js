const urlParams = new URLSearchParams(window.location.search);
let selectedGraph = urlParams.get('graph') || 'x'; // Get from URL or default to 'x'
// Basic validation
if (!['x', 'y'].includes(selectedGraph)) { // Add other valid graph codes here (e.g., 'z')
    selectedGraph = 'x';
}
console.log(`Loading graph: ${selectedGraph}.json`);

export function initModal(nodes, unlocked) {
  // Use D3 to handle node clicks consistently
  d3.selectAll("g.node")
    .on("click", function(event, d) {
      // Fetch fresh data to check lock status
      fetch(`/data?graph=${selectedGraph}`).then(res => {
           if (!res.ok) throw new Error(`HTTP error checking lock status! Status: ${res.status}`);
           return res.json();
          })
          .then(currentState => {
              const currentUnlocked = currentState.unlocked || {};
              if (!currentUnlocked[d.id]) {
                  console.log(`Node ${d.id} is locked.`);
                  return; // Exit if node is locked
              }

              // --- Open Exercise Modal ---
              console.log(`Opening exercise modal for unlocked node: ${d.id}`);
              const modal = document.getElementById("modal");
              const modalTitle = document.getElementById("modalTitle");
              const modalDynamicBody = document.getElementById("modalDynamicBody");
              const closeModalBtn = document.getElementById("closeModalBtn");

              if (!modal || !modalTitle || !modalDynamicBody || !closeModalBtn) {
                   console.error("Core modal elements not found!"); return;
              }

              const popup = d.popup;
              const currentNodeId = d.id; // Store node ID for saving notes

              // Set the main modal title
              modalTitle.textContent = d.title || "Node Details";

              // Build HTML for the dynamic body area
              let dynamicHtml = '';

              // Description (optional)
              if (popup?.text && popup.text.trim() !== '') {
                  dynamicHtml += `<p>${popup.text}</p>`;
              }

               // PDF Link (optional)
               if (popup?.pdf_link) {
                 if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`;
                 dynamicHtml += `<p><a href="${popup.pdf_link}" target="_blank" rel="noopener noreferrer">📄 Open Exercise Details</a></p>`;
               }

              // Exercises (optional)
              if (popup?.exercises && popup.exercises.length > 0) {
                if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`;
                dynamicHtml += "<h4>Exercises:</h4>";
                popup.exercises.forEach((ex, i) => {
                  // ... (exercise HTML generation - unchanged) ...
                  const exerciseId = ex.id || `ex-${i}`;
                  const optional = ex.optional ? " (optional)" : "";
                  const points = ex.points ?? 10;
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

              // *** ADDED: User Notes Section ***
              if (dynamicHtml !== '') dynamicHtml += `<hr class="modal-separator">`; // Separator before notes
              dynamicHtml += `
                  <div id="userNotesSection" style="margin-top: 15px;">
                      <h4>My Notes:</h4>
                      <textarea id="userNotesArea" rows="5" style="width: 98%; background-color: var(--base03, #1e1f1c); color: var(--base1, #f8f8f2); border: 1px solid var(--base01, #586e75); border-radius: 3px; padding: 8px; font-family: monospace;" placeholder="Add your private notes, commands, reminders here..."></textarea>
                      <div style="text-align: right; margin-top: 8px;">
                          <button id="saveNotesBtn" class="modal-save-button">Save Notes</button>
                          <span id="notesSaveStatus" style="margin-left: 10px; font-size: 0.8em; font-style: italic;"></span>
                       </div>
                  </div>
              `;
              // *** END: User Notes Section ***


              // Inject the built HTML into the dynamic body
              modalDynamicBody.innerHTML = dynamicHtml;

              // Populate the notes textarea AFTER it's added to the DOM
              const notesTextArea = modalDynamicBody.querySelector('#userNotesArea');
              if (notesTextArea) {
                  notesTextArea.value = popup?.userNotes || ''; // Populate with existing notes or empty string
              }

              // Attach listener to the main close button
              closeModalBtn.onclick = () => { modal.style.display = "none"; };

              // Show the modal
              modal.style.display = "block";

              // Add checkbox listeners
              modalDynamicBody.querySelectorAll('input[type=checkbox]').forEach(input => {
                // input.replaceWith(input.cloneNode(true));
                input.addEventListener('change', handleCheckboxChange);
              });

              // *** ADDED: Add Save Notes button listener ***
              const saveNotesButton = modalDynamicBody.querySelector('#saveNotesBtn');
              const notesSaveStatus = modalDynamicBody.querySelector('#notesSaveStatus');
              if (saveNotesButton && notesTextArea) {
                  saveNotesButton.onclick = () => {
                      const currentNotes = notesTextArea.value;
                      console.log(`Saving notes for node ${currentNodeId}`);
                      saveNotesButton.disabled = true; // Disable button during save
                      notesSaveStatus.textContent = "Saving...";
                      notesSaveStatus.style.color = "var(--yellow, #b58900)";


                      // Fetch current state, update notes, POST back
                      fetch(`/data?graph=${selectedGraph}`)
                          .then(res => { if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`); return res.json(); })
                          .then(currentState => {
                              const nodeToUpdate = currentState.nodes.find(n => n.id === currentNodeId);
                              if (nodeToUpdate) {
                                  // Ensure popup object exists
                                  if (!nodeToUpdate.popup) nodeToUpdate.popup = {};
                                  // Update userNotes field
                                  nodeToUpdate.popup.userNotes = currentNotes;

                                  // Send the ENTIRE updated nodes list back
                                  return fetch(`/data?graph=${selectedGraph}`, {
                                      method: 'POST',
                                      headers: { 'Content-Type': 'application/json' },
                                      body: JSON.stringify(currentState.nodes)
                                  });
                              } else {
                                  throw new Error(`Node with ID ${currentNodeId} not found in current state.`);
                              }
                          })
                          .then(res => { if (!res.ok) throw new Error(`POST error! Status: ${res.status}`); return res.json(); })
                          .then(newState => {
                              console.log("Notes saved successfully. Dispatching update.");
                              notesSaveStatus.textContent = "Saved!";
                              notesSaveStatus.style.color = "var(--green, #859900)";
                              saveNotesButton.disabled = false;
                              // Dispatch event to potentially update UI if notes were displayed elsewhere (optional)
                              document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
                              // Clear status message after a delay
                              setTimeout(() => { notesSaveStatus.textContent = ""; }, 2000);
                          })
                          .catch(error => {
                              console.error('Error saving notes:', error);
                              notesSaveStatus.textContent = "Error saving!";
                              notesSaveStatus.style.color = "var(--red, #dc322f)";
                              saveNotesButton.disabled = false;
                              alert(`Error saving notes: ${error.message}`);
                          });
                  };
              } else {
                   console.warn("Save Notes button or textarea not found.");
              }

      }).catch(err => console.error("Error checking node lock status or building modal:", err));

    }); // End D3 click listener
}

// Handler function for checkbox changes (remains the same logic)
function handleCheckboxChange(event) {
  const checkbox = event.target;
  const nodeId = checkbox.dataset.nodeId;
  const exerciseIndex = parseInt(checkbox.dataset.exIndex, 10);
  const isCompleted = checkbox.checked;

  console.log(`Checkbox change: Node ${nodeId}, Index ${exerciseIndex}, Completed: ${isCompleted}`);

  fetch(`/data?graph=${selectedGraph}`)
    .then(res => { if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`); return res.json(); })
    .then(currentState => {
      const nodeToUpdate = currentState.nodes.find(n => n.id === nodeId);
      if (nodeToUpdate?.popup?.exercises?.[exerciseIndex]) {
        nodeToUpdate.popup.exercises[exerciseIndex].completed = isCompleted;
        return fetch(`/data?graph=${selectedGraph}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(currentState.nodes) });
      } else { throw new Error(`Node or exercise not found for update: Node ${nodeId}, Index ${exerciseIndex}`); }
    })
    .then(res => { if (!res.ok) throw new Error(`POST error! Status: ${res.status}`); return res.json(); })
    .then(newState => {
        console.log("Dispatching appDataUpdated event after exercise update.");
        document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
        document.getElementById("modal").style.display = "none"; // Close modal on success
    })
    .catch(error => {
      console.error('Error updating exercise:', error);
      alert(`Error saving exercise status: ${error.message}`);
      // checkbox.checked = !isCompleted; // Optional: revert UI on error
    });
}