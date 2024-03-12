import { serve } from '@hono/node-server'

import App from '@/app.js'

serve({
  fetch: App.fetch,
  port: 8080,
})
