import { describe, it, expect, beforeEach } from 'vitest'
import { initGraph } from '../static/graph.js'
import * as d3 from 'd3'

global.d3 = d3

document.body.innerHTML = `<svg width="800" height="600"></svg>`

describe('initGraph', () => {
  it('renders nodes and links', () => {
    const nodes = [{ id: 'A', type: 'main', title: 'Node A', percent: 100, popup: { exercises: [] } }]
    const links = []
    const unlocked = { A: true }
    initGraph(nodes, links, unlocked)
    const rendered = document.querySelectorAll('circle')
    expect(rendered.length).toBe(1)
  })
})
