import { describe, it, expect } from 'vitest'
import { handleBadges } from '../static/badges.js'
import { renderBadgeGallery } from '../static/badges.js'

document.body.innerHTML = ``
vi.stubGlobal('fetch', () => Promise.resolve({})) // stub backend update


describe('renderBadgeGallery', () => {
  beforeEach(() => {
    document.body.innerHTML = `<div id="badgesDisplay"></div>`
  })

  it('renders all badge images with labels', () => {
    const badges = [
      { id: 'b1', title: 'Level 5', image: 'static/badge1.png' },
      { id: 'b2', title: 'CTF 10', image: 'static/badge2.png' }
    ]

    renderBadgeGallery(badges)

    const icons = document.querySelectorAll('.badge-icon')
    const labels = document.querySelectorAll('.badge-label')

    expect(icons.length).toBe(2)
    expect(labels[0].textContent).toBe('Level 5')
    expect(labels[1].textContent).toBe('CTF 10')
  })
})


describe('handleBadges', () => {
    beforeEach(() => {
        document.body.innerHTML = `
          <template id="badgeTemplate">
            <div id="badgePopup" class="badge-popup">
              <img class="badge-image" />
              <div class="badge-info">
                <h3 class="badge-title"></h3>
                <p class="badge-desc"></p>
              </div>
              <button id="closeBadgePopup">Close</button>
            </div>
          </template>
        `
      })

  it('shows all unshown badges one after another', async () => {
    const badges = [
      { id: 'a', title: 'Badge A', description: 'A desc', shown: false, image: 'static/badge1.png' },
      { id: 'b', title: 'Badge B', description: 'B desc', shown: false, image: 'static/badge2.png' }
    ]

    handleBadges(badges)

    await new Promise(r => setTimeout(r, 50))
    expect(document.body.innerHTML).toContain('Badge A')

    document.getElementById('closeBadgePopup').click()

    await new Promise(r => setTimeout(r, 300)) // wait for queue to advance
    expect(document.body.innerHTML).toContain('Badge B')

    document.getElementById('closeBadgePopup').click()
    await new Promise(r => setTimeout(r, 100))
    expect(document.getElementById('badgePopup')).toBeNull()
  })
})


describe('handleBadges', () => {
  it('shows popup for new badge', () => {
    const badges = [{
      id: 'b1',
      title: 'Level 5',
      description: 'Nice job',
      shown: false,
      image: 'static/badge1.png'
    }]
    handleBadges(badges)
    const popup = document.getElementById('badgePopup')
    expect(popup).toBeTruthy()
    expect(popup.innerHTML).toContain('Level 5')
  })
})
