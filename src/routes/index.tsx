import { createFileRouter } from '@/utils/file-router.js'


export default createFileRouter(r => {
  r.get('/', c => c.html(
    <h1>Hello, World!</h1>
  ))
  r.get('/json', c => c.json({ hello: 'world' }))
})
