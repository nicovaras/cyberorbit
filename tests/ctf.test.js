import { describe, it, expect, vi } from 'vitest'
import { setupCtfHandlers } from '../static/ctf.js'

global.fetch = vi.fn(() => Promise.resolve({
  json: () => Promise.resolve({ ctfs: [{ title: 'test', completed: 1 }] })
}))

describe('setupCtfHandlers', () => {
  it('defines updateCtf globally', () => {
    setupCtfHandlers([{ title: 'test', completed: 1 }])
    expect(typeof window.updateCtf).toBe('function')
  })
})
