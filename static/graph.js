// Store selections and simulation globally within the module
let nodeSelection = null;
let linkSelection = null;
let currentSimulation = null;
let currentZoomTransform = d3.zoomIdentity; // Store current zoom transform

// Function to calculate hexagon points (flat top/bottom)
function getHexagonPoints(radius) {
    const angle = Math.PI / 3; // 60 degrees
    let points = "";
    for (let i = 0; i < 6; i++) {
        let currentAngle = angle * i + Math.PI / 6; // Start rotated by 30deg
        points += `${radius * Math.cos(currentAngle)},${radius * Math.sin(currentAngle)} `;
    }
    return points.trim();
}

// Function to determine node classes based on data
function getNodeClasses(d, unlocked, discovered) {
    let classes = "node";
    if (!d || !d.id) return classes; // Handle invalid data

    if (!discovered.has(d.id)) classes += " undiscovered";
    else if (d.id === "Start") classes += " start";
    else if (d.type === "main") classes += " mainColor";
    else { // Sub nodes
        classes += " sub";
        const ex = d.popup?.exercises || [];
        const allExercisesComplete = ex.length > 0 && ex.every(e => e.completed === true);
        if (allExercisesComplete) {
            classes += " done";
        }
    }
    if (!unlocked[d.id] && d.id !== "Start") {
        classes += " locked";
    }
    return classes;
}

// Function to determine percentage text
function getPercentText(d, discovered) {
    if (discovered.has(d.id) && d.type !== "start" && d.type !== "main" && typeof d.percent === 'number') {
        let percentText = `${d.percent}%`;
        if (d.percent === 100) {
            const exercises = d.popup?.exercises || [];
            const hasIncompleteOptionals = exercises.some(ex => ex.optional === true && ex.completed === false);
            if (hasIncompleteOptionals) {
                percentText += "*";
            }
        }
        return percentText;
    }
    return '';
}



// --- Function to Apply Updates to Graph Elements ---
export function updateGraph(updatedNodes, updatedLinks, updatedUnlocked, updatedDiscovered) {
    if (!nodeSelection || !linkSelection || !currentSimulation) {
        console.error("Graph selections or simulation not initialized for update.");
        return;
    }
    console.log("Updating graph...");

    // *** FIX: Update simulation nodes data without replacing objects ***
    const simulationNodes = currentSimulation.nodes(); // Get current simulation node objects
    const newNodeDataMap = new Map(updatedNodes.map(n => [n.id, n])); // Map new data by ID

    // Merge new data properties into existing simulation node objects
    simulationNodes.forEach(simNode => {
        const newData = newNodeDataMap.get(simNode.id);
        if (newData) {
            // Copy relevant properties from newData to simNode
            // Exclude simulation properties (x, y, vx, vy, fx, fy, index)
            Object.keys(newData).forEach(key => {
                if (!['x', 'y', 'vx', 'vy', 'fx', 'fy', 'index'].includes(key)) {
                    simNode[key] = newData[key];
                }
            });
        } else {
             console.warn(`Node data for ID ${simNode.id} not found in update.`);
             // Optionally handle nodes that might have been removed in the backend data
        }
    });

    // Update the links in the simulation's link force
    currentSimulation.force("link").links(updatedLinks);

    // --- Update Link Visuals ---
    // Re-bind the new links data. Use a key function.
    linkSelection = linkSelection
        .data(updatedLinks, d => `${d.source.id || d.source}-${d.target.id || d.target}`)
        .join("line") // Handle enter/exit if link structure changes
        .attr("data-source-id", d => typeof d.source === 'object' ? d.source.id : d.source)
        .attr("data-target-id", d => typeof d.target === 'object' ? d.target.id : d.target)
        .attr("class", d => { // Update link class based on new unlocked status
            const sourceId = typeof d.source === 'object' ? d.source.id : d.source;
            const targetId = typeof d.target === 'object' ? d.target.id : d.target;
            // Use the UPDATED unlocked status
            const sourceUnlocked = updatedUnlocked[sourceId];
            const targetUnlocked = updatedUnlocked[targetId];
            return (sourceUnlocked && targetUnlocked) ? "link solid" : "link dashed";
        });


    // --- Update Node Visuals ---
    // Re-select nodes and bind the *updated simulation nodes* using the ID key function.
    // This ensures D3 updates elements based on data objects that have coordinates.
    nodeSelection = nodeSelection
        .data(simulationNodes, d => d.id);

    // Update classes and text for existing nodes based on the merged data
    nodeSelection
        .attr("class", d => getNodeClasses(d, updatedUnlocked, updatedDiscovered)); // Use updated data

    nodeSelection.select("text.percent")
        .text(d => getPercentText(d, updatedDiscovered)); // Use updated data

    nodeSelection.select("text.label")
        .text(d => updatedDiscovered.has(d.id) ? d.title : ''); // Use updated data


    // Optional: Handle entering/exiting nodes if nodes can be added/removed dynamically
    // nodeSelection.enter().append('g')...
    // nodeSelection.exit().remove()...

    // Restart simulation gently to update positions
    currentSimulation.alpha(0.3).restart(); // Adjust alpha as needed
    console.log("Graph update applied.");
}


// --- Initialize the graph (runs once on load) ---
export function initGraph(initialNodes, initialLinks, initialUnlocked, initialDiscovered) {
  const svg = d3.select("svg");
  const width = window.innerWidth;
  const height = window.innerHeight;

  svg.selectAll("*").remove(); // Clear previous graph

  const zoomLayer = svg.append("g");
  const linkGroup = zoomLayer.append("g").attr("class", "links");
  const nodeGroup = zoomLayer.append("g").attr("class", "nodes");

  // Store zoom behavior to re-apply transform later if needed
  const zoomBehavior = d3.zoom()
      .scaleExtent([0.1, 3])
      .on("zoom", (event) => {
          currentZoomTransform = event.transform; // Store current transform
          zoomLayer.attr("transform", currentZoomTransform);
      });
  svg.call(zoomBehavior);

  const discoveredNodes = new Set();
  const unlockedMap = initialUnlocked || {};
  const unlockedNodeIds = new Set(Object.keys(unlockedMap).filter(id => unlockedMap[id]));
  unlockedNodeIds.forEach(id => discoveredNodes.add(id));
  initialLinks.forEach(link => {
      const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
      const targetId = typeof link.target === 'object' ? link.target.id : link.target;
      if (unlockedNodeIds.has(sourceId)) discoveredNodes.add(targetId);
      if (unlockedNodeIds.has(targetId)) discoveredNodes.add(sourceId);
  });
  discoveredNodes.add("Start");

  // --- Simulation Setup ---
  currentSimulation = d3.forceSimulation(initialNodes) // Use initialNodes
    .force("link", d3.forceLink(initialLinks).id(d => d.id).distance(150))
    .force("charge", d3.forceManyBody().strength(-700))
    .force("collision", d3.forceCollide().radius(d => (d.type === "main" || d.type === "start") ? 45 : 25))
    .force("center", d3.forceCenter(width / 2, height / 2));

  // --- Link Elements (Initial Draw) ---
  linkSelection = linkGroup.selectAll("line")
    .data(initialLinks, d => `${d.source.id || d.source}-${d.target.id || d.target}`)
    .join("line")
    .attr("data-source-id", d => typeof d.source === 'object' ? d.source.id : d.source)
    .attr("data-target-id", d => typeof d.target === 'object' ? d.target.id : d.target)
    .attr("class", d => {
        const sourceId = typeof d.source === 'object' ? d.source.id : d.source;
        const targetId = typeof d.target === 'object' ? d.target.id : d.target;
        return (initialUnlocked[sourceId] && initialUnlocked[targetId]) ? "link solid" : "link dashed";
    });

  // --- Node Elements (Initial Draw) ---
  nodeSelection = nodeGroup.selectAll("g.node")
    .data(initialNodes, d => d.id)
    .join("g")
    .attr("class", d => getNodeClasses(d, initialUnlocked, initialDiscovered));

   nodeSelection.append("polygon")
       .attr("points", d => getHexagonPoints((d.type === "main" || d.type === "start") ? 38 : 20))
       .attr("class", "node-shape");

  nodeSelection.append("text")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    .attr("dy", ".35em")
    .text(d => initialDiscovered.has(d.id) ? d.title : '')
    .style("font-size", d => (d.type === "main" || d.type === "start") ? "13px" : "10px");

  nodeSelection.append("text")
    .attr("class", "percent")
    .attr("text-anchor", "middle")
    .attr("dy", d => (d.type === "main" || d.type === "start") ? 48 : 30)
    .text(d => getPercentText(d, initialDiscovered));

  // --- Simulation Tick Handler ---
  currentSimulation.on("tick", () => {
    // Use selections stored in module scope
    if(linkSelection) {
        linkSelection
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
    }
    if(nodeSelection) {
        nodeSelection
          .attr("transform", d => `translate(${d.x},${d.y})`);
    }
  });
  console.log("Graph initialized.");
  return discoveredNodes;

}