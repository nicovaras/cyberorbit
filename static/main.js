// Import necessary functions
import { initGraph, updateGraph } from './graph.js'; // Import both init and update
import { initModal } from './modal.js';
import { handleBadges, renderBadgeGallery } from './badges.js';
import { setupCtfHandlers } from './ctf.js';
import { updateSidebar, renderOrUpdateHexChart } from './sidebar.js';

// --- Global state (within module scope) ---
let currentAppState = {
    nodes: [],
    links: [],
    unlocked: {},
    discovered: new Set(),
    streak: {},
    ctfs: [],
    badges: []
};
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
    console.log("Updating UI with new state...", newState); // Log for debugging

    // Validate newState structure if needed
    if (!newState || !Array.isArray(newState.nodes) || !newState.unlocked || !newState.discovered) {
        console.error("Received invalid state for UI update:", newState);
        return;
    }

    // Update the global state
    currentAppState = {
        ...newState,
        discovered: new Set(newState.discovered || []) // Ensure discovered is a Set
    };

    // Update the graph visuals
    updateGraph(
        currentAppState.nodes,
        currentAppState.links, // Pass links if they might change
        currentAppState.unlocked,
        currentAppState.discovered
    );

    // Update the sidebar content
    updateSidebar(
        currentAppState.nodes,
        currentAppState.streak,
        currentAppState.ctfs
    );

    // Update badges (assuming these functions handle updates)
    handleBadges(currentAppState.badges);
    renderBadgeGallery(currentAppState.badges);

    // Re-initialize modal listeners for potentially new/updated nodes if necessary
    // (Current initModal adds listeners once, might need adjustments if nodes are added/removed dynamically)
    // initModal(currentAppState.nodes, currentAppState.unlocked); // Be cautious re-adding listeners

    console.log("UI Update complete.");
}


// --- Fetch Initial Data and Initialize ---
fetch('/data')
  .then(res => {
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  })
  .then((initialData) => {
    // Store initial state
     currentAppState = {
        ...initialData,
        discovered: new Set(initialData.discovered || []),
        unlocked: initialData.unlocked || {}
    };

    // Initial rendering
    initGraph(
        currentAppState.nodes,
        currentAppState.links,
        currentAppState.unlocked,
        currentAppState.discovered
    );
    initModal( // Attaches click listeners to graph nodes
        currentAppState.nodes,
        currentAppState.unlocked
    );
    updateSidebar( // Renders sidebar content
        currentAppState.nodes,
        currentAppState.streak,
        currentAppState.ctfs
    );
    handleBadges(currentAppState.badges);
    renderBadgeGallery(currentAppState.badges);
    setupCtfHandlers(currentAppState.ctfs); // Sets up window.updateCtf

    // --- Add Global Event Listener for Data Updates ---
    document.addEventListener('appDataUpdated', (event) => {
        console.log("Event 'appDataUpdated' received.");
        if (event.detail) {
            updateUI(event.detail); // Call the central update function
        } else {
             console.warn("'appDataUpdated' event received without detail (newState).");
             // Optionally re-fetch data as a fallback
             // fetch('/data').then(res => res.json()).then(updateUI);
        }
    });

  })
  .catch(error => {
      console.error("Failed to fetch or initialize data:", error);
      document.body.innerHTML = `<div style="color: red; padding: 20px; font-family: monospace;">Error loading roadmap data. Please check the console or try again later.</div>`;
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