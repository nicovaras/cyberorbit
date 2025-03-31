import { initGraph } from './graph.js';
import { updateSidebar } from './sidebar.js';
import { initModal } from './modal.js';
import { handleBadges, renderBadgeGallery } from './badges.js';
import { setupCtfHandlers } from './ctf.js';

fetch('/data')
  .then(res => res.json())
  .then(({ nodes, links, unlocked, discovered, streak, ctfs, badges,  }) => {
    initGraph(nodes, links, unlocked, new Set(discovered));
    initModal(nodes, unlocked);
    updateSidebar(nodes, streak, ctfs);
    handleBadges(badges);
    renderBadgeGallery(badges);
    setupCtfHandlers(ctfs);
  });
  

document.getElementById('openStats').addEventListener('click', () => {
  document.getElementById('statsModal').style.display = 'block';
});

document.getElementById('toggleSidebar').addEventListener('click', () => {
  const sidebar = document.getElementById('sidebar')
  const hidden = sidebar.classList.toggle('hidden')
  document.getElementById('toggleSidebar').style.right = hidden ? '0px' : '290px'
})

document.addEventListener('DOMContentLoaded', () => {
  const select = document.querySelector('.custom-select');
  const selected = select.querySelector('.selected');
  const optionsContainer = select.querySelector('.options');
  const optionsList = select.querySelectorAll('.option');

  selected.addEventListener('click', () => {
    optionsContainer.style.display = optionsContainer.style.display === 'block' ? 'none' : 'block';
  });

  function updateSelected(optionElement) {
    optionsList.forEach(opt => opt.classList.remove('selected'));
    optionsList.forEach(opt => {
      opt.textContent = opt.textContent.replace('✔', '').trim();
    });

    optionElement.classList.add('selected');
    optionElement.textContent = `✔ ${optionElement.textContent}`;
    selected.textContent = optionElement.textContent.replace('✔', '').trim();

    const theme = optionElement.getAttribute('data-value');
    document.getElementById('themeStylesheet').href = `/static/${theme}`;
    localStorage.setItem('selectedTheme', theme);
  }

  optionsList.forEach(o => {
    o.addEventListener('click', () => {
      updateSelected(o);
      optionsContainer.style.display = 'none';
    });
  });

  document.addEventListener('click', (e) => {
    if (!select.contains(e.target)) {
      optionsContainer.style.display = 'none';
    }
  });

  // Initialize the correct selected option on load
  const savedTheme = localStorage.getItem('selectedTheme') || 'green.css';
  const initialOption = Array.from(optionsList).find(opt => opt.getAttribute('data-value') === savedTheme);
  if (initialOption) updateSelected(initialOption);
});



