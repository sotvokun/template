import { RouterProvider } from 'react-router'
import { createBrowserRouter } from 'react-router-dom'


type Props = {
    router: ReturnType<typeof createBrowserRouter>
}

export default function App(props: Props) {
  return <RouterProvider router={props.router} />
}