export function initModal(nodes, unlocked) {
  document.querySelectorAll("g").forEach(g => {
    g.addEventListener("click", () => {}); // prevent D3 click leaks
  });

  d3.selectAll("g").on("click", (event, d) => {
    if (!unlocked[d.id]) return;

    const popup = d.popup;
    document.getElementById("modalTitle").textContent = d.title;
    let html = `<p>${popup.text}</p>`;

    if (popup.pdf_link) {
      html += `<a href="${popup.pdf_link}" target="_blank">📄 Open Exercise</a><br/><br/>`;
    }

    if (popup.exercises) {
      popup.exercises.forEach((ex, i) => {
        const optional = ex.optional ? " (optional)" : "";
        const points = ex.points ?? 10;
        const checked = ex.completed ? "checked" : "";
        html += `
          <label style="opacity: ${ex.optional ? 0.6 : 1}; font-style: ${ex.optional ? 'italic' : 'normal'}">
            <input type="checkbox" data-node-id="${d.id}" data-ex-index="${i}" ${checked}/>
            ${ex.label} (${points} points)${optional}
          </label><br/>
        `;
      });
    }

    document.getElementById("modalBody").innerHTML = html;
    document.getElementById("modal").style.display = "flex";

    setTimeout(() => {
      document.querySelectorAll('#modalBody input[type=checkbox]').forEach(input => {
        input.addEventListener('change', (e) => {
          const nodeId = e.target.dataset.nodeId;
          const i = +e.target.dataset.exIndex;

          fetch('/data')
            .then(res => res.json())
            .then(full => {
              const data = full.nodes.filter(n => n.id !== "Start");
              const nodeInData = data.find(n => n.id === nodeId);
              nodeInData.popup.exercises[i].completed = e.target.checked;

              fetch('/data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
              }).then(() => location.reload());
            });
        });
      });
    }, 10);
  });
}
