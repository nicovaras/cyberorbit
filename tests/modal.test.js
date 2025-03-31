import { describe, it, expect, beforeEach } from 'vitest'
import { initModal } from '../static/modal.js'
import * as d3 from 'd3'
global.d3 = d3

document.body.innerHTML = `
<div id="modalTitle"></div>
<div id="modalBody"></div>
<div id="modal" style="display: none;"></div>
<svg><g></g></svg>
`

describe('initModal', () => {
  it('renders modal on click if unlocked', () => {
    const nodes = [{
      id: 'node1',
      title: 'Node 1',
      popup: { text: 'Hello', exercises: [{ label: 'ex1', completed: false }] }
    }]
    const unlocked = { node1: true }
    initModal(nodes, unlocked)
    const event = new Event('click')
    const g = document.querySelector('g')
    g.__data__ = nodes[0]
    g.dispatchEvent(event)
    expect(document.getElementById('modal').style.display).toBe('flex')
    expect(document.getElementById('modalTitle').textContent).toContain('Node 1')
  })
})
