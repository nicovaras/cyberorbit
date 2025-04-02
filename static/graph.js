export function initGraph(nodes, links, unlocked, discovered) {
  const svg = d3.select("svg");
  const width = window.innerWidth;
  const height = window.innerHeight;

  svg.selectAll("*").remove(); // Clear previous graph elements if any

  const zoomLayer = svg.append("g");
  const linkGroup = zoomLayer.append("g").attr("class", "links");
  const nodeGroup = zoomLayer.append("g").attr("class", "nodes");

  svg.call(d3.zoom().scaleExtent([0.1, 3]).on("zoom", ({ transform }) => {
    zoomLayer.attr("transform", transform);
  }));

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

  // --- Simulation Setup ---
  // D3 force simulation ignores initial x, y, vx, vy in the data objects by default.
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(150))
    .force("charge", d3.forceManyBody().strength(-600))
    .force("collision", d3.forceCollide().radius(d => (d.type === "main" || d.type === "start") ? 45 : 25))
    .force("center", d3.forceCenter(width / 2, height / 2));

  // --- Link Elements ---
  const link = linkGroup.selectAll("line")
    .data(links)
    .join("line")
    .attr("data-source-id", d => typeof d.source === 'object' ? d.source.id : d.source)
    .attr("data-target-id", d => typeof d.target === 'object' ? d.target.id : d.target)
    .attr("class", d => {
        const sourceId = typeof d.source === 'object' ? d.source.id : d.source;
        const targetId = typeof d.target === 'object' ? d.target.id : d.target;
        const sourceUnlocked = unlocked[sourceId];
        const targetUnlocked = unlocked[targetId];
        return (sourceUnlocked && targetUnlocked) ? "link solid" : "link dashed";
    });

  // --- Node Elements (Group) ---
  const node = nodeGroup.selectAll("g.node")
    .data(nodes, d => d.id) // Use key function
    .join("g")
    .attr("class", d => { // Set classes based on node state
      let classes = "node";
      if (!discovered.has(d.id)) classes += " undiscovered";
      else if (d.id === "Start") classes += " start";
      else if (d.type === "main") classes += " mainColor";
      else { // Sub nodes
          classes += " sub";
          const ex = d.popup?.exercises || [];
          // Check if there are exercises AND if ALL of them are completed === true
          const allExercisesComplete = ex.length > 0 && ex.every(e => e.completed === true);
           if (allExercisesComplete) {
               classes += " done"; // Apply .done only if ALL exercises are complete
           }
      }
       if (!unlocked[d.id] && d.id !== "Start") {
            classes += " locked";
       }
      return classes;
    });

   // --- Node Shape (Hexagon) ---
   node.append("polygon")
       .attr("points", d => getHexagonPoints((d.type === "main" || d.type === "start") ? 38 : 20))
       .attr("class", "node-shape");

  // --- Node Label Text ---
  node.append("text")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    .attr("dy", ".35em") // Vertical centering
    .text(d => discovered.has(d.id) ? d.title : '')
    .style("font-size", d => (d.type === "main" || d.type === "start") ? "13px" : "10px");

  // --- Node Percentage Text ---
  node.append("text")
    .attr("class", "percent")
    .attr("text-anchor", "middle")
    .attr("dy", d => (d.type === "main" || d.type === "start") ? 48 : 30) // Position below hexagon
    .text(d => {
        // Show percentage only for discovered, non-start, non-main nodes that have a percentage
        if (discovered.has(d.id) && d.type !== "start" && d.type !== "main" && typeof d.percent === 'number') {
            let percentText = `${d.percent}%`;
            // *** ADDED LOGIC: Check for asterisk ***
            if (d.percent === 100) {
                const exercises = d.popup?.exercises || [];
                // Check if there's at least one optional exercise that is NOT completed
                const hasIncompleteOptionals = exercises.some(ex => ex.optional === true && ex.completed === false);
                if (hasIncompleteOptionals) {
                    percentText += "*"; // Append asterisk
                }
            }
            return percentText;
        }
        return ''; // Return empty string otherwise
    });

  // --- Simulation Tick Handler ---
  simulation.on("tick", () => {
    // Update link positions
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);
    // Update node group positions
    node
      .attr("transform", d => `translate(${d.x},${d.y})`);
  });

  // Drag functions remain defined but are not attached to nodes
  function dragstarted(event, d) { /* ... */ }
  function dragged(event, d) { /* ... */ }
  function dragended(event, d) { /* ... */ }

  return { simulation, node, link }; // Return elements if needed
}