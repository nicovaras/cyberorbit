export function updateSidebar(nodes, streak, ctfs) {
  const mainProgress = document.getElementById("mainProgress");
  const levelDisplay = document.getElementById("levelDisplay");
  const xpBar = document.getElementById("xpBar");
  const streakDisplay = document.getElementById("streakDisplay");
  const ctfList = document.getElementById("ctfList");
  const themeSelector = document.getElementById("themeSelector");
  const themeStylesheet = document.getElementById("themeStylesheet");

  mainProgress.innerHTML = "";
  ctfList.innerHTML = "";

  nodes.filter(n => n.type === "main").forEach(n => {
    const item = document.createElement("div");
    item.className = "sidebar-item";
    item.innerHTML = `${n.title} <span>${n.percent}%</span>`;
    mainProgress.appendChild(item);
  });

  const allExercises = nodes.flatMap(n => n.popup?.exercises || []);
  const exerciseXP = allExercises.filter(e => e.completed).reduce((sum, e) => sum + (e.points ?? 10), 0);
  const ctfXP = (ctfs || []).reduce((sum, c) => sum + (c.completed * 30), 0);
  const earnedXP = exerciseXP + ctfXP;

  let levelThresholds = [0];
  let sum = 50;
  for (let i = 1; i < 25; i++) {
    levelThresholds.push(sum);
    sum += 50 + i * 10;
  }
  let currentLevel = levelThresholds.findIndex((xp, i) => earnedXP < levelThresholds[i + 1]);
  if (currentLevel === -1) currentLevel = levelThresholds.length - 1;

  const prevXP = levelThresholds[currentLevel];
  const nextXP = levelThresholds[currentLevel + 1] ?? prevXP + 1;
  const progress = Math.min(100, Math.round(((earnedXP - prevXP) / (nextXP - prevXP)) * 100));

  levelDisplay.textContent = `Level ${currentLevel + 1}`;
  xpBar.style.width = `${progress}%`;
  xpBar.textContent = `${earnedXP}/${nextXP}`;
  streakDisplay.innerHTML = ` <strong>${streak.streak} day${streak.streak === 1 ? '' : 's'}</strong>`;

  const savedTheme = localStorage.getItem('selectedTheme');
  if (savedTheme) {
    themeStylesheet.href = `/static/${savedTheme}`;
    themeSelector.value = savedTheme;
  }
  themeSelector.addEventListener('change', () => {
    themeStylesheet.href = `/static/${themeSelector.value}`;
    localStorage.setItem('selectedTheme', themeSelector.value);
  });

  if (ctfs?.length) {
    ctfs.forEach((ctf, index) => {
      const item = document.createElement("div");
      item.className = "sidebar-item ctf-link";
      item.textContent = `🟢 ${ctf.title} – ${ctf.completed * 30} points`;
      item.onclick = () => showCtfModal(ctf, index);
      ctfList.appendChild(item);
    });
  }

  const abilities = {
    "Scripting and Automation": 0,
    "System Analysis": 0,
    "CTFs": (ctfs || []).reduce((sum, c) => sum + c.completed, 0),
    "Defensive Techniques": 0,
    "Offensive Techniques": 0,
    "Web and Network Analysis": 0
  };

  nodes.forEach(n => {
    (n.popup?.exercises || []).forEach(e => {
      if (e.completed && Array.isArray(e.categories)) {
        e.categories.forEach(cat => {
          if (abilities.hasOwnProperty(cat)) {
            abilities[cat] += 1;
          }
        });
      }
    });
  });

  const ctx = document.getElementById("hexagonChart").getContext("2d");
  new Chart(ctx, {
    type: "radar",
    data: {
      labels: Object.keys(abilities),
      datasets: [{
        label: "Your Skills",
        data: Object.values(abilities).map(v => Math.min(60, Math.round(v))),
        fill: true,
        borderColor: "#00ffff",
        backgroundColor: "rgba(0, 255, 255, 0.2)",
        pointBackgroundColor: "#00ffff",
      }]
    },
    options: {
      responsive: false,
      scales: {
        r: {
          beginAtZero: true,
          max: 60,
          angleLines: { color: '#333' },
          grid: { color: '#333' },
          pointLabels: {
            color: '#00ffff',
            font: { size: 16 }
          },
          ticks: { display: false }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
}
function showCtfModal(ctf, index) {
  const modal = document.getElementById("modal");
  const modalContent = document.getElementById("modalContent");
  modalContent.innerHTML = "";

  const tpl = document.getElementById("ctfModalTemplate");
  const clone = tpl.content.cloneNode(true);

  clone.getElementById("ctfDescription").textContent = ctf.description;
  clone.getElementById("ctfLink").href = ctf.link;
  clone.getElementById("ctfCompleted").textContent = ctf.completed;

  clone.getElementById("closeCtfModal").onclick = () => {
    modal.style.display = "none";
  };

  clone.getElementById("decreaseCtf").onclick = () => {
    updateCtf(index, -1);
    modal.style.display = "none";
  };

  clone.getElementById("increaseCtf").onclick = () => {
    updateCtf(index, 1);
    modal.style.display = "none";
  };

  modalContent.appendChild(clone);
  document.getElementById("ctfTitle").textContent = ctf.title;
  modal.style.display = "flex";
}
