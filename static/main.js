// Import necessary functions
import { initGraph, updateGraph } from './graph.js';
import { initModal } from './modal.js';
import { handleBadges, renderBadgeGallery } from './badges.js';
import { setupCtfHandlers } from './ctf.js';
import { updateSidebar, renderOrUpdateHexChart } from './sidebar.js';

// --- Global state (within module scope) ---
window.currentAppState = { 
    nodes: [], links: [], unlocked: {}, discovered: new Set(),
    streak: {}, ctfs: [], badges: [], current_graph: 'x.json'
};

const urlParams = new URLSearchParams(window.location.search);
let selectedGraph = urlParams.get('graph') || 'x'; // Get from URL or default to 'x'

console.log(`Loading graph: ${selectedGraph}.json`);

function calculateAbilities(nodes, ctfs) {
  const abilities = {
      "Scripting and Automation": 0, "System Analysis": 0, "CTFs": 0,
      "Defensive Techniques": 0, "Offensive Techniques": 0, "Web and Network Analysis": 0
  };
  if (ctfs) { abilities["CTFs"] = ctfs.reduce((sum, c) => sum + (c.completed || 0), 0); }
  if (nodes) {
      nodes.forEach(n => {
          (n.popup?.exercises || []).forEach(e => {
              if (e.completed && Array.isArray(e.categories)) {
                  e.categories.forEach(cat => {
                      if (abilities.hasOwnProperty(cat)) { abilities[cat] += 1; }
                  });
              }
          });
      });
  }
  return abilities;
}

// --- Function to Update All UI Components ---
function updateUI(newState) {
    console.log("Updating UI with new state...", newState);

    // Validate newState structure
    if (!newState || !Array.isArray(newState.nodes) || !newState.unlocked) {
        console.error("Received invalid state for UI update:", newState);
        return;
    }

    // Ensure discovered is a Set for internal logic that might expect it
    const discoveredSet = new Set(newState.discovered || []);

    // Update the graph visuals using data directly from newState
    // Ensure updateGraph receives nodes, links, unlocked status, and the discovered Set
    updateGraph(
        newState.nodes,
        newState.links,         // Assuming links are part of the state now
        newState.unlocked,      // Pass the unlocked map {node_id: boolean}
        discoveredSet           // Pass the discovered Set
    );

    // Update the sidebar content using data from newState
    updateSidebar(
        newState.nodes,
        newState.streak,
        newState.ctfs,
        discoveredSet           // Pass the discovered Set
    );

    // Update badges (check if they need the full state or just the badges list)
    // These functions likely only need the badges array from the state
    handleBadges(newState.badges);
    renderBadgeGallery(newState.badges);

    // Update the hexagon chart in the sidebar/stats modal
    // Ensure calculateAbilities is called if needed, or use abilities from state
    // Assuming newState contains an 'abilities' object calculated by the backend:
    if (newState.abilities) {
        renderOrUpdateHexChart(newState.abilities);
    } else {
        // Fallback or recalculate if needed, though backend should provide it
        console.warn("Abilities data missing from new state for chart update.");
        const currentAbilities = calculateAbilities(newState.nodes, newState.ctfs); // Recalculate as fallback
        renderOrUpdateHexChart(currentAbilities);
    }


    // Re-initialize modal listeners IF nodes might be dynamically added/removed.
    // If the node structure is static per graph, calling initModal once initially might be sufficient.
    // If you call it here, ensure it doesn't create duplicate listeners.
    // initModal(); // Call without args if relying on global state


    console.log("UI Update complete.");
}


// --- Fetch Initial Data and Initialize ---
fetch(`/data?graph=${selectedGraph}`)
  .then(res => {
    if (res.redirected && res.url.includes('/login')) {
        // If fetch was redirected to the login page, redirect the whole window
        console.log("User not authenticated, redirecting to login.");
        window.location.href = '/login';
        return null; // Stop processing this response chain
      }

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  })
  .then((initialData) => {
    if (initialData === null) {
        return; // Exit if we were redirected
    }
    // Store initial state
    window.currentAppState = {
        ...initialData,
        discovered: new Set(initialData.discovered || []),
        unlocked: initialData.unlocked || {},
        abilities: initialData.abilities || calculateAbilities(initialData.nodes, initialData.ctfs) // Ensure abilities are present initially
    };

    // Initial rendering
    const discoveredNodes = initGraph(
        window.currentAppState.nodes,
        window.currentAppState.links,
        window.currentAppState.unlocked,
        window.currentAppState.discovered
    );
    initModal( // Attaches click listeners to graph nodes
        window.currentAppState.nodes,
        window.currentAppState.unlocked
    );
    updateSidebar( // Renders sidebar content
        window.currentAppState.nodes,
        window.currentAppState.streak,
        window.currentAppState.ctfs,
        discoveredNodes
    );
    handleBadges(window.currentAppState.badges);
    renderBadgeGallery(window.currentAppState.badges);
    setupCtfHandlers(window.currentAppState.ctfs); // Sets up window.updateCtf
    
    const graphSelector = document.getElementById('graphSelector');
    if (graphSelector) {
        graphSelector.value = selectedGraph; // Set dropdown to reflect loaded graph
    }

    // --- Add Global Event Listener for Data Updates ---
    document.addEventListener('appDataUpdated', (event) => {
        console.log("Event 'appDataUpdated' received.");

        // Check if the event came with a full state update (e.g., initial load, or future GET refresh)
        if (event.detail) {
            console.log("Event received with detail (full state update). Updating global state.");
            // Update the global state first
            window.currentAppState = {
               ...event.detail,
               // Ensure correct types if needed
               unlocked: event.detail.unlocked || {},
               discovered: new Set(event.detail.discovered || []),
               // Ensure abilities are recalculated or taken from detail
               abilities: event.detail.abilities || calculateAbilities(event.detail.nodes, event.detail.ctfs)
            };
        } else {
            // This case handles the optimistic updates from modal.js/ctf.js
            // The global state (window.currentAppState) was *already updated* optimistically.
            console.log("Event received without detail (optimistic update). UI will use current global state.");
            // We might need to recalculate abilities based on the optimistically updated state
            // Note: This assumes abilities change based on exercises/CTFs completions.
            window.currentAppState.abilities = calculateAbilities(window.currentAppState.nodes, window.currentAppState.ctfs);
        }

        // *** Always call updateUI with the current global state ***
        updateUI(window.currentAppState);

        // Update graph selector dropdown if graph changed
        const graphSelector = document.getElementById('graphSelector');
        if (graphSelector && window.currentAppState.current_graph) {
            const graphName = window.currentAppState.current_graph.replace('.json', '');
            if (graphSelector.value !== graphName) {
                graphSelector.value = graphName;
            }
        }
    });
  })
  .catch(error => {
    console.error("Failed to fetch or initialize data:", error);
    // Display a more user-friendly error, maybe keep login link
    document.body.innerHTML = `<div style="color: red; padding: 20px; font-family: monospace;">
        Error loading roadmap data. Please ensure you are logged in or try again later.
        <br><a href="/login">Login</a>
        <br>Details: ${error.message}
        </div>`;
});


// --- Event Listener for Stats Modal ---
const openStatsButton = document.getElementById('openStats');
const statsModalElement = document.getElementById('statsModal');
if (openStatsButton && statsModalElement) {
    openStatsButton.addEventListener('click', () => {
      console.log("Open Stats button clicked."); // Debug log
      statsModalElement.style.display = 'block';
      // *** FIX: Render/Update chart AFTER modal is displayed ***
      // Ensure abilities data is current before rendering
      // Option 1: Use state calculated during last updateUI
      // renderOrUpdateHexChart(currentAppState.abilities);
      // Option 2: Recalculate fresh abilities from current state (safer if state mgmt is complex)
      const currentAbilities = calculateAbilities(currentAppState.nodes, currentAppState.ctfs);
      renderOrUpdateHexChart(currentAbilities);
    });
} else { console.warn("Stats modal elements not found."); }

// --- Event Listener for Sidebar Toggle ---
const toggleSidebarButton = document.getElementById('toggleSidebar');
const sidebarElement = document.getElementById('sidebar');
if (toggleSidebarButton && sidebarElement) {
    toggleSidebarButton.addEventListener('click', () => {
      sidebarElement.classList.toggle('visible');
    });
} else { console.warn("Sidebar elements not found."); }

const graphSelector = document.getElementById('graphSelector');
if (graphSelector) {
    graphSelector.addEventListener('change', (event) => {
        const newGraphValue = event.target.value;
        console.log(`Graph selection changed to: ${newGraphValue}`);
        // Construct the new URL and reload the page
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('graph', newGraphValue); // Set or update the 'graph' parameter
        window.location.href = currentUrl.toString(); // Reload page with new URL
    });
} else {
    console.warn("Graph selector element (#graphSelector) not found.");
}

// --- Theme Selector Logic ---
document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM Content Loaded - Setting up theme selector"); // Log: DOM ready
  const select = document.querySelector('.custom-select');
  if (!select) { console.warn("Theme selector root (.custom-select) not found."); return; }

  const selected = select.querySelector('.selected');
  const optionsContainer = select.querySelector('.options');
  const optionsList = select.querySelectorAll('.option');
  const themeStylesheet = document.getElementById('themeStylesheet');

  if (!selected || !optionsContainer || !optionsList.length || !themeStylesheet) {
      console.warn("Theme selector parts missing:", { selected, optionsContainer, optionsList, themeStylesheet });
      return;
  }
  console.log("Theme selector elements found."); // Log: Elements found

  // Function to update theme based on selected option
  function updateSelectedTheme(optionElement) {
    if (!optionElement) {
        console.warn("updateSelectedTheme called with null optionElement");
        return;
    }
    console.log("Updating theme to:", optionElement.getAttribute('data-value')); // Log: Theme update attempt

    // Visually update the dropdown
    optionsList.forEach(opt => {
        opt.classList.remove('selected');
        opt.textContent = opt.textContent.replace('✔', '').trim();
    });
    optionElement.classList.add('selected');
    optionElement.textContent = `✔ ${optionElement.textContent}`;
    selected.textContent = optionElement.textContent.replace('✔', '').trim();

    // Apply the theme
    const theme = optionElement.getAttribute('data-value');
    if (theme) {
        themeStylesheet.href = `/static/${theme}`; // Make sure path is correct
        console.log("Stylesheet href set to:", themeStylesheet.href); // Log: Stylesheet updated
        try {
            localStorage.setItem('selectedTheme', theme);
        } catch (e) { console.warn("LS error saving theme:", e); }
    } else {
         console.warn("Selected option is missing data-value attribute:", optionElement);
    }
  }

  // Event listener for dropdown toggle
  selected.addEventListener('click', (e) => {
      e.stopPropagation();
      const currentDisplay = window.getComputedStyle(optionsContainer).display;
      const newDisplay = currentDisplay === 'block' ? 'none' : 'block';
      console.log(`Toggling theme options display to: ${newDisplay}`); // Log: Toggle options visibility
      optionsContainer.style.display = newDisplay;
  });

  // Event listeners for option selection
  optionsList.forEach(o => {
    o.addEventListener('click', (e) => {
      console.log("Theme option clicked:", e.target.textContent); // Log: Option clicked
      updateSelectedTheme(o);
      optionsContainer.style.display = 'none'; // Close dropdown after selection
    });
  });

  // Close dropdown if clicking outside
  document.addEventListener('click', (e) => {
    // Check if the options are visible AND the click was outside the select element
    if (window.getComputedStyle(optionsContainer).display === 'block' && !select.contains(e.target)) {
        console.log("Clicked outside theme selector, closing options."); // Log: Click outside
        optionsContainer.style.display = 'none';
    }
  });

  // Initialize theme on load
  let savedTheme = 'dracula.css';
   try { savedTheme = localStorage.getItem('selectedTheme') || 'dracula.css'; }
   catch (e) { console.warn("LS error reading theme:", e); }
   console.log("Initializing theme from localStorage:", savedTheme); // Log: Initial theme
  const initialOption = Array.from(optionsList).find(opt => opt.getAttribute('data-value') === savedTheme);
  updateSelectedTheme(initialOption || optionsList[0]);

}); // End DOMContentLoaded