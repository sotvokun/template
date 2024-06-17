import fs from 'node:fs';
import path from 'node:path';
import { builtinModules } from 'node:module';
import type { Plugin } from 'vite';

type Options = {
  minify?: boolean;
  type?: 'module' | 'commonjs';
  virtualEntryFilePath?: string;
};

export const honoxNodeServer = (opts?: Options): Plugin => {
  const name = '@hono/vite-node-server';
  const virtualEntryId = 'virtual:node-server-entry-module';
  const resolvedVirtualEntryId = `\0${virtualEntryId}`;
  const virtualEntryFilePath =
    opts?.virtualEntryFilePath ??
    path.join(import.meta.dirname, 'honox-node-server-template.ts.template');
  return {
    name,
    resolveId: (id) => {
      if (id !== virtualEntryId) {
        return;
      }
      return resolvedVirtualEntryId;
    },
    load: async (id) => {
      if (id !== resolvedVirtualEntryId) {
        return;
      }
      const templateContent = fs.readFileSync(virtualEntryFilePath).toString();
      return templateContent;
    },
    config: async () => ({
      ssr: {
        external: [],
        noExternal: true,
      },
      build: {
        outDir: './dist',
        emptyOutDir: false,
        minify: opts?.minify ?? true,
        ssr: true,
        rollupOptions: {
          external: [...builtinModules, /^node:/],
          input: virtualEntryId,
          output: {
            entryFileNames: opts?.type === 'module' ? '_server.mjs' : '_server.js',
          },
        },
      },
    }),
  };
};
