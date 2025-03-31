import { describe, it, expect } from 'vitest'
import { updateSidebar } from '../static/sidebar.js'

document.body.innerHTML = `
<div id="sidebar"></div>
<canvas id="hexagonChart"></canvas>
`
global.Chart = class {
    constructor(ctx, config) {
      this.ctx = ctx
      this.config = config
    }
  }
  HTMLCanvasElement.prototype.getContext = () => ({
    fillRect: () => {},
    beginPath: () => {},
    moveTo: () => {},
    lineTo: () => {},
    stroke: () => {},
    arc: () => {},
    fill: () => {},
    closePath: () => {},
  });
  
describe('updateSidebar', () => {
  it('renders main nodes, XP and CTFs', () => {
    const nodes = [
      { id: 'a', type: 'main', title: 'Node A', percent: 60, popup: { exercises: [] } },
      { id: 'b', type: 'sub', title: 'Node B', percent: 80, popup: { exercises: [] } }
    ]
    const ctfs = [{ title: 'ctf1', completed: 2 }]
    const streak = { streak: 3 }

    updateSidebar(nodes, streak, ctfs)
    const html = document.getElementById('sidebar').innerHTML
    expect(html).toContain('Node A')
    expect(html).toContain('CTF')
    expect(html).toContain('Streak')
  })
})
