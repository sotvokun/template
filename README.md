hono-starter
-----------

This project is a starter template to create a fullstack hono application with
nodejs server.

## File-based routing
The project implements a file-based routing system for better developer experience.
The default routes directory is `src/routes`, and there has a `index.ts` file in
it as an example.

```
routes
 |- index.ts            -> /
 |- version.ts          -> /version
 |- api/
    |- index.ts         -> /api
    |- user.ts          -> /api/user
```

The file-based routing system is a little bit different from the next.js style.
Each file is a router - a collection of routes. That means you can define complex
path pattern like `/api/user/:id/:action/settings` without deep nesting.

To define a router is simple, just export the return of `createFileRouter` function
that defined in `src/utils/file-router.ts`.

```typescript
import { createFileRouter } from '../utils/file-router'
export default createFileRouter(r => {
  r.get('/', c => c.text('Hello, world!'))
})
```

You can see implementations in the `src/utils/file-router.ts`.
