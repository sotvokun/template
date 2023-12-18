import React from 'react'
import ReactDOM from 'react-dom/client'

import routes from 'virtual:generated-pages-react'
import { createBrowserRouter } from 'react-router-dom'
import 'virtual:uno.css'

import App from './App'


const router = createBrowserRouter(routes)

ReactDOM.createRoot(document.getElementById('root')!).render(
  import.meta.env.DEV ? (
    <React.StrictMode>
      <App router={router} />
    </React.StrictMode>
  ) : (
    <App router={router} />
  ),
)
