import { initGraph } from './graph.js';
import { updateSidebar } from './sidebar.js';
import { initModal } from './modal.js';
import { handleBadges, renderBadgeGallery } from './badges.js';
import { setupCtfHandlers } from './ctf.js';

// --- Fetch Initial Data and Initialize ---
fetch('/data')
  .then(res => {
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  })
  .then(({ nodes, links, unlocked, discovered, streak, ctfs, badges }) => {
    // Ensure discovered is a Set
    const discoveredSet = new Set(discovered || []);
    // Ensure unlocked is an object
    const unlockedMap = unlocked || {};

    initGraph(nodes, links, unlockedMap, discoveredSet);
    initModal(nodes, unlockedMap); // Pass unlockedMap here
    updateSidebar(nodes, streak, ctfs);
    handleBadges(badges);
    renderBadgeGallery(badges);
    setupCtfHandlers(ctfs);
  })
  .catch(error => {
      console.error("Failed to fetch or initialize data:", error);
      // Display a user-friendly error message on the page
      document.body.innerHTML = `<div style="color: red; padding: 20px; font-family: monospace;">Error loading roadmap data. Please check the console or try again later.</div>`;
  });


// --- Event Listener for Stats Modal ---
const openStatsButton = document.getElementById('openStats');
const statsModalElement = document.getElementById('statsModal');

if (openStatsButton && statsModalElement) {
    openStatsButton.addEventListener('click', () => {
      statsModalElement.style.display = 'block';
      // Optionally re-render chart or update data here if needed when opened
    });
} else {
    console.warn("Stats modal button or container not found.");
}

// --- Event Listener for Sidebar Toggle ---
const toggleSidebarButton = document.getElementById('toggleSidebar');
const sidebarElement = document.getElementById('sidebar');

if (toggleSidebarButton && sidebarElement) {
    toggleSidebarButton.addEventListener('click', () => {
      // *** FIX: Toggle the '.visible' class instead of '.hidden' ***
      sidebarElement.classList.toggle('visible');
      // No need to manually adjust button position; CSS handles it now.
    });
} else {
    console.warn("Sidebar toggle button or sidebar element not found.");
}


// --- Theme Selector Logic (DOMContentLoaded ensures elements exist) ---
document.addEventListener('DOMContentLoaded', () => {
  const select = document.querySelector('.custom-select');
  // Check if theme selector elements exist before adding listeners
  if (!select) {
      console.warn("Theme selector not found.");
      return; // Exit if selector is missing
  }
  const selected = select.querySelector('.selected');
  const optionsContainer = select.querySelector('.options');
  const optionsList = select.querySelectorAll('.option');
  const themeStylesheet = document.getElementById('themeStylesheet'); // Get stylesheet link

  if (!selected || !optionsContainer || !optionsList.length || !themeStylesheet) {
      console.warn("Theme selector parts or stylesheet link not found.");
      return; // Exit if parts are missing
  }


  // Function to update theme based on selected option
  function updateSelectedTheme(optionElement) {
    if (!optionElement) return;

    // Visually update the dropdown
    optionsList.forEach(opt => {
        opt.classList.remove('selected');
        opt.textContent = opt.textContent.replace('✔', '').trim(); // Remove checkmark
    });
    optionElement.classList.add('selected');
    optionElement.textContent = `✔ ${optionElement.textContent}`; // Add checkmark
    selected.textContent = optionElement.textContent.replace('✔', '').trim(); // Update displayed text

    // Apply the theme
    const theme = optionElement.getAttribute('data-value');
    if (theme) {
        themeStylesheet.href = `/static/${theme}`;
        try {
            localStorage.setItem('selectedTheme', theme);
        } catch (e) {
            console.warn("Could not save theme preference to localStorage:", e);
        }
    }
  }

  // Event listener for dropdown toggle
  selected.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent click from immediately closing via document listener
      const currentDisplay = window.getComputedStyle(optionsContainer).display;
      optionsContainer.style.display = currentDisplay === 'block' ? 'none' : 'block';
  });

  // Event listeners for option selection
  optionsList.forEach(o => {
    o.addEventListener('click', () => {
      updateSelectedTheme(o);
      optionsContainer.style.display = 'none'; // Close dropdown after selection
    });
  });

  // Close dropdown if clicking outside
  document.addEventListener('click', (e) => {
    if (!select.contains(e.target)) {
        if (window.getComputedStyle(optionsContainer).display === 'block') {
             optionsContainer.style.display = 'none';
        }
    }
  });

  // Initialize theme on load
  let savedTheme = 'dracula.css'; // Default to dracula
   try {
       savedTheme = localStorage.getItem('selectedTheme') || 'dracula.css';
   } catch (e) {
       console.warn("Could not read theme preference from localStorage:", e);
   }
  const initialOption = Array.from(optionsList).find(opt => opt.getAttribute('data-value') === savedTheme);
  updateSelectedTheme(initialOption || optionsList[0]); // Fallback to first option if saved theme isn't found

}); // End DOMContentLoaded