export function setupCtfHandlers() {

    // Make updateCtf globally available
    window.updateCtf = function(ctfIndex, delta) {
  
      // Get current CTF data from the global state (needed to calculate new count)
      if (!window.currentAppState || !Array.isArray(window.currentAppState.ctfs)) {
          console.error("Error: currentAppState or CTFs not available.");
          alert("Error: Could not get current CTF data.");
          return;
      }
      if (ctfIndex < 0 || ctfIndex >= window.currentAppState.ctfs.length) {
          console.error(`Invalid CTF index: ${ctfIndex}`);
          alert(`Error: Invalid CTF index provided.`);
          return;
      }
  
      // Calculate the *intended* new state locally only to send it
      // We don't modify window.currentAppState optimistically anymore
      const targetCtf = window.currentAppState.ctfs[ctfIndex];
      const originalCount = targetCtf.completed || 0;
      const newCount = Math.max(0, originalCount + delta); // Calculate desired new count
  
      // Create a payload representing the *intended complete state* of the CTF list
      // (because the backend /ctfs endpoint expects the full list currently)
      const ctfPayload = JSON.parse(JSON.stringify(window.currentAppState.ctfs)); // Deep copy
      ctfPayload[ctfIndex].completed = newCount; // Apply the single change to the copied list
  
      // Get current graph selection
      const urlParams = new URLSearchParams(window.location.search);
      let selectedGraph = urlParams.get('graph') || 'x';
  
      console.log(`Attempting to update CTF ${targetCtf.id} count to ${newCount}`);
  
      // --- Step 1: POST the intended update (full list) ---
      fetch(`/ctfs?graph=${selectedGraph}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ctfPayload) // Send the calculated intended state
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
              console.log(`CTF update for index ${ctfIndex} confirmed. Fetching updated state...`);
              return fetch(`/data?graph=${selectedGraph}`); // Chain the GET request
          } else {
              throw new Error(data.error || "Unknown error saving CTF status");
          }
      })
      .then(res => { // Handle the response from the GET request
          if (!res.ok) { throw new Error(`State refresh error: ${res.statusText}`); }
          return res.json();
      })
      .then(newState => { // newState is the full state from the GET request
          console.log(`Updated state received after CTF update. Dispatching appDataUpdated.`);
          // Dispatch event with the NEW state from the GET request
          new Audio('/static/check.mp3').play();
          document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));
      })
      .catch(error => {
          console.error('Error updating CTF or refreshing state:', error);
          alert(`Error saving CTF status: ${error.message}`);
          // Since we didn't change the UI optimistically, no revert is needed here
          // The UI will still reflect the state before the failed update attempt.
      });
  
    }; // End of window.updateCtf function definition
  } // End of setupCtfHandlers