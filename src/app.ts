import { Hono } from 'hono'
import { join } from 'node:path'

import { applyFileRouters } from '@/utils/file-router.js'

const app = new Hono()

await applyFileRouters(app, {
  pattern: ['**/*.{ts,tsx,js,jsx}'],
  cwd: join(import.meta.dirname, 'routes'),
})

export default app
