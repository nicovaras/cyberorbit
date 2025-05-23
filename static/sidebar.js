// --- Module Scope Variable for Chart Instance ---
let hexagonChartInstance = null;

// --- CTF Modal Display Function (Defined in module scope) ---
function showCtfModal(ctf, index) {
    console.log("Showing CTF Modal for:", ctf?.title, "at index", index);
    const modal = document.getElementById("modal");
    // *** Target the main title and dynamic body elements ***
    const modalTitle = document.getElementById("modalTitle");
    const modalDynamicBody = document.getElementById("modalDynamicBody");
    const closeModalBtn = document.getElementById("closeModalBtn"); // Get main close button

    // Check if main modal elements exist
    if (!modal || !modalTitle || !modalDynamicBody || !closeModalBtn) {
        console.error("Core modal elements (#modal, #modalTitle, #modalDynamicBody, #closeModalBtn) not found!");
        return;
    }

    const tpl = document.getElementById("ctfModalTemplate");
    if (!tpl) {
        console.error("CTF modal template not found!");
        return;
    }

    try {
        // Set the main modal title
        modalTitle.textContent = ctf.title || "CTF Details";

        // Clone only the content needed for the dynamic body
        const clone = tpl.content.cloneNode(true);

        // Populate template elements within the clone
        const descriptionEl = clone.getElementById("ctfDescription");
        const linkEl = clone.getElementById("ctfLink");
        const completedEl = clone.getElementById("ctfCompleted");
        const decreaseBtn = clone.getElementById("decreaseCtf");
        const increaseBtn = clone.getElementById("increaseCtf");
        // Removed: clone.getElementById("ctfTitle"); -> Use main modal title
        // Removed: clone.getElementById("closeCtfModal"); -> Use main modal close button

        if (descriptionEl) descriptionEl.textContent = ctf.description || "No description.";
        if (linkEl) linkEl.href = ctf.link || "#";
        if (completedEl) completedEl.textContent = ctf.completed || 0;

        // Attach event listeners to buttons within the clone
        if (decreaseBtn) decreaseBtn.onclick = () => {
            if (window.updateCtf) window.updateCtf(index, -1); else console.error("updateCtf not found");
            modal.style.display = "none";
        };
        if (increaseBtn) increaseBtn.onclick = () => {
            if (window.updateCtf) window.updateCtf(index, 1); else console.error("updateCtf not found");
            modal.style.display = "none";
        };

        // Clear previous dynamic content and append new CTF content
        modalDynamicBody.innerHTML = ""; // Clear only the dynamic part
        modalDynamicBody.appendChild(clone);

        // Attach listener to the main close button
        closeModalBtn.onclick = () => { modal.style.display = "none"; };

        // Show the main modal container
        modal.style.display = "block";
    } catch (error) {
        console.error("Error populating CTF modal:", error);
    }
}
// Make showCtfModal globally accessible
window.showCtfModal = showCtfModal;

// --- Function to Update Sidebar Content (Chart Logic Removed) ---
export function updateSidebar(nodes, streak, ctfs, discoveredNodes, earnedXP, currentLevel) {
  console.log("Updating sidebar content..."); // Debug log
  const mainProgress = document.getElementById("mainProgress");
  const levelDisplay = document.getElementById("levelDisplay");
  const xpBar = document.getElementById("xpBar");
  const xpBarWrapper = document.getElementById("xpBarWrapper");
  const streakDisplay = document.getElementById("streakDisplay");
  const ctfList = document.getElementById("ctfList");

  // --- Clear existing dynamic content ---
  if (mainProgress) mainProgress.innerHTML = ""; else console.warn("mainProgress element not found");
  if (ctfList) ctfList.innerHTML = ""; else console.warn("ctfList element not found");

  // --- Populate Main Progress ---
  if (mainProgress && nodes) {
    nodes
        .filter(n => n.type === "main" && discoveredNodes.has(n.id))
        .forEach(n => {
            const item = document.createElement("div");
            item.className = "sidebar-item";
            item.innerHTML = `${n.title} <span>${n.percent ?? 0}%</span>`;
            mainProgress.appendChild(item);
        });
  }  
  
  let levelThresholds = [0]; let levelSum = 0;
  // Ensure this calculation MATCHES the one in main.js
  for (let i = 0; i < 50; i++) { levelSum += 50 + (i * 10); levelThresholds.push(levelSum); }



  // --- Calculate Level ---
  const prevLevelIndex = currentLevel - 1;
  const nextLevelIndex = currentLevel;

  const prevXP = levelThresholds[prevLevelIndex] ?? 0;
  // Calculate XP needed for the *next* level relative to the *start* (0 XP)
  const nextXPThreshold = levelThresholds[nextLevelIndex] ?? (prevXP + (50 + prevLevelIndex * 10)); // Calculate next threshold if needed

  const xpInLevel = earnedXP - prevXP; // How much XP earned within the current level range
  const xpForLevel = nextXPThreshold - prevXP; // Total XP needed to complete the current level

  // Calculate percentage progress within the current level
  const progress = xpForLevel > 0 ? Math.min(100, Math.round((xpInLevel / xpForLevel) * 100)) : (earnedXP > prevXP ? 100 : 0);

  // Update Level Display
  if (levelDisplay) levelDisplay.textContent = `Level ${currentLevel}`; else console.warn("levelDisplay element not found");
  // Update XP Bar
  if (xpBar) {
    xpBar.style.width = `${progress}%`;
    // Display XP progress within the level, e.g., "15/100 XP" or just total XP
    // Option 1: Show progress within level
     xpBar.textContent = `${xpInLevel} / ${xpForLevel} XP`;
    // Option 2: Show total XP
    // xpBar.textContent = `${earnedXP} XP Total`;
  } else console.warn("xpBar element not found");
   // Optional: Add a title attribute (tooltip) to the wrapper showing exact values
   if (xpBarWrapper) {
        xpBarWrapper.title = `Level <span class="math-inline">\{currentLevel\} \(</span>{progress}%)\nTotal XP: ${earnedXP}\nXP for next level: ${nextXPThreshold}`;
    }
  // --- Update Streak Display ---
  if (streakDisplay && streak) { streakDisplay.innerHTML = ` <strong>${streak.streak} day${streak.streak === 1 ? '' : 's'}</strong>`; } else console.warn("streakDisplay element not found");

  // --- Populate CTF List ---
   if (ctfList && ctfs?.length) {
     ctfs.forEach((ctf, index) => {
       const item = document.createElement("div");
       item.className = "sidebar-item ctf-link";
       item.textContent = `${ctf.title} – ${ctf.completed * 30} points`;
       // Use the globally exposed showCtfModal
       item.onclick = () => window.showCtfModal(ctf, index);
       ctfList.appendChild(item);
     });
   } else if (ctfList) {
        ctfList.innerHTML = '<p style="font-style: italic; font-size: 12px; color: var(--comment);">No CTFs loaded.</p>';
   }

   // --- Chart logic is now REMOVED from updateSidebar ---
   console.log("Sidebar content updated.");
}


// --- NEW Function to Render or Update Hexagon Chart ---
export function renderOrUpdateHexChart(abilities) {
    console.log("Attempting to render/update hexagon chart with abilities:", abilities); // Debug log
    const canvas = document.getElementById("hexagonChart");
    if (!canvas) {
        console.error("Canvas element #hexagonChart not found!");
        return;
    }
    // Check if canvas is visible and has dimensions
    if (canvas.offsetParent === null || canvas.width <= 0 || canvas.height <= 0) {
         console.warn("Canvas #hexagonChart is not visible or has no dimensions. Chart rendering deferred.");
         // Optionally, try again later or log this state
         return;
    }


    const ctx = canvas.getContext("2d");
    if (!ctx) {
        console.error("Failed to get 2D context for #hexagonChart");
        return;
    }

    // Destroy existing chart instance before creating new one
    if (hexagonChartInstance) {
        console.log("Destroying previous hexagon chart instance.");
        hexagonChartInstance.destroy();
        hexagonChartInstance = null;
    }

    // Ensure abilities data is in the correct format
    const labels = Object.keys(abilities || {});
    const dataValues = Object.values(abilities || {});


    if (labels.length === 0) {
         console.warn("No ability data provided for hexagon chart.");
         // Optionally display a message on the canvas
         ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
         ctx.fillStyle = 'grey';
         ctx.textAlign = 'center';
         ctx.fillText("No skill data available", canvas.width / 2, canvas.height / 2);
         return;
    }


    // Create new chart instance
    console.log("Creating new hexagon chart instance.");
    try {
        hexagonChartInstance = new Chart(ctx, {
          type: "radar",
          data: {
            labels: labels,
            datasets: [{
              label: "Skills",
              data: dataValues,
              fill: true,
            }]
          },
          options: {
            responsive: false,
            maintainAspectRatio: true,
            scales: {
              r: {
                beginAtZero: true,
                angleLines: { color: 'rgba(131, 148, 150, 0.2)' },
                grid: { color: 'rgba(131, 148, 150, 0.2)' },
                pointLabels: {
                  color: 'var(--cyan, #8be9fd)',
                  font: { size: 12 }
                },
                max:60,
                ticks: {
                    display: false,
                  }
              }
            },
            plugins: {
                legend: { display: false },
                tooltip: {}
             }
          }
        });
        console.log("Hexagon chart created/updated successfully."); // Success log
    } catch (error) {
         console.error("Error creating chart:", error);
    }
}