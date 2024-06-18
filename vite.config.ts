import { defineConfig } from 'vite';
import honox from 'honox/vite';

import { honoxNodeServer } from './vendor/vite/honox-node-server-plugin';
import client from 'honox/vite/client';

export default defineConfig(({ mode }) => ({
  build: {
    assetsDir: 'static',
    ssrEmitAssets: true,
  },
  plugins:
    mode === 'client'
      ? [client()]
      : [
          honox({
            devServer: {
              entry: 'app/server.ts',
            },
          }),
          honoxNodeServer({
            minify: false,
          }),
        ],
}));
