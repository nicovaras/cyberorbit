export function setupCtfHandlers(/* ctfs parameter might not be needed if using global state */) {

  // Make updateCtf globally available
  window.updateCtf = function(ctfIndex, delta) {

    // --- START MODIFIED LOGIC ---
    // Get current CTF data from the global state
    if (!window.currentAppState || !Array.isArray(window.currentAppState.ctfs)) {
        console.error("Error: currentAppState or CTFs not available.");
        alert("Error: Could not get current CTF data.");
        return;
    }

    // Create a deep copy of the CTFs array from the global state to modify
    const updatedCtfs = JSON.parse(JSON.stringify(window.currentAppState.ctfs));

    // Check if index is valid and modify the copied list
    if (ctfIndex >= 0 && ctfIndex < updatedCtfs.length) {
        const currentCount = updatedCtfs[ctfIndex].completed || 0;
        updatedCtfs[ctfIndex].completed = Math.max(0, currentCount + delta); // Ensure count >= 0

        // Get current graph selection for the POST context
        const urlParams = new URLSearchParams(window.location.search);
        let selectedGraph = urlParams.get('graph') || 'x';
        if (!['x', 'y'].includes(selectedGraph)) { selectedGraph = 'x'; }

        // Send ONLY the updated CTFs array list to the /ctfs endpoint
        // No initial GET /data is needed.
        fetch(`/ctfs?graph=${selectedGraph}`, { // Add graph param if backend needs context
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updatedCtfs) // Send the modified full list
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
            console.log("Dispatching appDataUpdated event after CTF update.");
            document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
            // No automatic modal close needed here unless called from a modal context
        })
        .catch(error => {
            console.error('Error updating CTF:', error);
            alert(`Error saving CTF status: ${error.message}`);
            // Optionally revert UI changes if possible
        });

    } else {
         console.error(`Invalid CTF index: ${ctfIndex}`);
         alert(`Error: Invalid CTF index provided.`);
    }
    // --- END MODIFIED LOGIC ---
  }; // End of window.updateCtf function definition
} // End of setupCtfHandlers
