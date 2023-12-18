import React from 'react'
import ReactDOM from 'react-dom/client'

import routes from 'virtual:generated-pages-react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

import 'virtual:uno.css'

const router = createBrowserRouter(routes)

ReactDOM.createRoot(document.getElementById('root')!).render(
  import.meta.env.DEV ? (
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
  ) : (
    <RouterProvider router={router} />
  ),
)
