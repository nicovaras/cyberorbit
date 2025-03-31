export function initGraph(nodes, links, unlocked, discovered) {
  const svg = d3.select("svg");
  const width = window.innerWidth;
  const height = window.innerHeight;

  const zoomLayer = svg.append("g");
  const linkGroup = zoomLayer.append("g").attr("stroke", "#aaa").attr("stroke-opacity", 0.6);
  const nodeGroup = zoomLayer.append("g").attr("stroke", "#fff").attr("stroke-width", 1.5);

  svg.call(d3.zoom().scaleExtent([0.1, 3]).on("zoom", ({ transform }) => {
    zoomLayer.attr("transform", transform);
  }));

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(140))
    .force("charge", d3.forceManyBody().strength(-500))
    .force("collision", d3.forceCollide().radius(d => d.type === "main" ? 170 : 40))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = linkGroup.selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", 1.5)
    .attr("class", d => {
      const sourceUnlocked = unlocked[d.source.id || d.source];
      const targetUnlocked = unlocked[d.target.id || d.target];
      return (!sourceUnlocked || !targetUnlocked) ? "link dashed" : "link solid";
    });

  const node = nodeGroup.selectAll("g")
    .data(nodes)
    .join("g")
    .attr("class", d => {
      if (!discovered.has(d.id)) return "node undiscovered";
      if (d.id === "Start") return "node start";
      if (d.type === "main") return "node mainColor";
      const ex = d.popup?.exercises || [];
      const hasIncompleteOptionals = ex.some(e => e.optional && !e.completed);
      return (d.percent < 100 || hasIncompleteOptionals) ? "node sub done" : "node sub";
    })
    .classed("locked", d => !unlocked[d.id] && d.id !== "Start");

  node.append("circle")
    .attr("r", d => (d.type === "main" || d.type === "start") ? 38 : 20);

  node.append("text")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    .attr("dy", 4)
    .text(d => discovered.has(d.id) ? d.title : '');

  node.append("text")
    .attr("class", "percent")
    .attr("text-anchor", "middle")
    .attr("dy", 20)
    .text(d => discovered.has(d.id) ? `${d.percent}% complete` : '');

  simulation.on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });
}
