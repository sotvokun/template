import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import pages from 'vite-plugin-pages'
import unocss from 'unocss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    pages(),
    unocss(),
    react(),
  ],
})
