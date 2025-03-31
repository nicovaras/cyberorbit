export function handleBadges(badges) {
  const queue = [...badges.filter(b => !b.shown)]
  if (!queue.length) return

  const showNext = () => {
    const badge = queue.shift()
    if (!badge) return

    const tpl = document.getElementById('badgeTemplate')
    const popup = tpl.content.firstElementChild.cloneNode(true)

    popup.querySelector('img').src = badge.image
    popup.querySelector('img').alt = badge.title
    popup.querySelector('.badge-title').textContent = badge.title
    popup.querySelector('.badge-desc').textContent = badge.description

    document.body.appendChild(popup)

    popup.querySelector('#closeBadgePopup').addEventListener('click', () => {
      popup.remove()
      fetch('/update_badges', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ badgeIds: [badge.id] })
      }).then(() => {
        setTimeout(showNext, 200)
      })
    })
  }

  showNext()
}

export function renderBadgeGallery(badges) {
  const container = document.getElementById('badgesDisplay')
  container.innerHTML = '' // clear old

  badges.forEach(badge => {
    const div = document.createElement('div')
    div.className = 'badge-item'
    div.innerHTML = `
      <img src="${badge.image}" alt="${badge.title}" class="badge-icon" />
      <div class="badge-label">${badge.title}</div>
    `
    container.appendChild(div)
  })
}
