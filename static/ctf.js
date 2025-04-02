export function setupCtfHandlers(ctfs) {
  // Make updateCtf globally available (consider better module interaction later)
  window.updateCtf = function(index, delta) {

    // Fetch current full state first
    fetch('/data')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
        })
      .then(currentState => {
        const updatedCtfs = currentState.ctfs ? [...currentState.ctfs] : []; // Work with a copy

        // Check if index is valid
        if (index >= 0 && index < updatedCtfs.length) {
            updatedCtfs[index].completed = Math.max(0, (updatedCtfs[index].completed || 0) + delta);

            // Send ONLY the updated CTFs array to the /ctfs endpoint
            return fetch('/ctfs', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(updatedCtfs) // Send updated ctfs list
            });
        } else {
             throw new Error(`Invalid CTF index: ${index}`);
        }
      })
      .then(res => {
          if (!res.ok) throw new Error(`POST error! Status: ${res.status}`);
           // *** Assume backend response to /ctfs POST also contains the FULL UPDATED state ***
           // This might require backend changes to the /ctfs endpoint
           return res.json();
       })
      .then(newState => {
          // *** Dispatch event with the new state ***
          console.log("Dispatching appDataUpdated event after CTF update.");
          document.dispatchEvent(new CustomEvent('appDataUpdated', { detail: newState }));

          // No reload needed
      })
      .catch(error => {
          console.error('Error updating CTF:', error);
          alert(`Error saving CTF status: ${error.message}`);
      });
  };
}