import { defineConfig } from 'vite'
import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import pages from 'vite-plugin-pages'
import tailwindcss from '@tailwindcss/vite'
import autoImport from 'unplugin-auto-import/vite'

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  plugins: [
    pages(),
    vue(),
    vueJsx(),
    tailwindcss(),
    autoImport({
      imports: [
        'vue',
      ],
      dts: 'src/types/auto-imports.d.ts',
    }),
  ],
})
