export function initModal(nodes, unlocked) {

  // Use D3 to handle node clicks consistently
  d3.selectAll("g.node")
    .on("click", function(event, d) {
      // Fetch fresh data to check lock status
      fetch('/data').then(res => {
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
              // *** Use the new dynamic body container ***
              const modalDynamicBody = document.getElementById("modalDynamicBody");
              const closeModalBtn = document.getElementById("closeModalBtn"); // Get close button

              if (!modal || !modalTitle || !modalDynamicBody || !closeModalBtn) {
                   console.error("Core modal elements (#modal, #modalTitle, #modalDynamicBody, #closeModalBtn) not found!");
                   return;
              }

              const popup = d.popup;

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
                if (dynamicHtml !== '') dynamicHtml += `<hr style="border: none; border-top: 1px solid #444; margin: 15px 0;">`;
                dynamicHtml += `<p><a href="${popup.pdf_link}" target="_blank" rel="noopener noreferrer">📄 Open Exercise Details</a></p>`;
              }

              // Exercises (optional)
              if (popup?.exercises && popup.exercises.length > 0) {
                if (dynamicHtml !== '') dynamicHtml += `<hr style="border: none; border-top: 1px solid #444; margin: 15px 0;">`;
                dynamicHtml += "<h4>Exercises:</h4>";
                popup.exercises.forEach((ex, i) => {
                  const exerciseId = ex.id || `ex-${i}`;
                  const optional = ex.optional ? " (optional)" : "";
                  const points = ex.points ?? 10;
                  const checked = ex.completed ? "checked" : "";
                  dynamicHtml += `
                    <div style="margin-bottom: 8px;">
                        <label style="opacity: ${ex.optional ? 0.7 : 1}; font-style: ${ex.optional ? 'italic' : 'normal'}; display: flex; align-items: center;">
                          <input type="checkbox" data-node-id="${d.id}" data-ex-id="${exerciseId}" data-ex-index="${i}" ${checked} style="margin-right: 8px;"/>
                          <span>${ex.label} (${points} points)${optional}</span>
                        </label>
                    </div>
                  `;
                });
              }

              // Inject the built HTML into the dynamic body
              modalDynamicBody.innerHTML = dynamicHtml;

              // Attach listener to the main close button
              closeModalBtn.onclick = () => { modal.style.display = "none"; };

              // Show the modal
              modal.style.display = "block";

              // Add checkbox listeners AFTER content is set
              modalDynamicBody.querySelectorAll('input[type=checkbox]').forEach(input => {
                input.replaceWith(input.cloneNode(true)); // Clear old listeners
              });
              modalDynamicBody.querySelectorAll('input[type=checkbox]').forEach(input => {
                   input.addEventListener('change', handleCheckboxChange); // Attach new listener
              });

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

  fetch('/data')
    .then(res => { if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`); return res.json(); })
    .then(currentState => {
      const nodeToUpdate = currentState.nodes.find(n => n.id === nodeId);
      if (nodeToUpdate?.popup?.exercises?.[exerciseIndex]) {
        nodeToUpdate.popup.exercises[exerciseIndex].completed = isCompleted;
        return fetch('/data', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(currentState.nodes) });
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